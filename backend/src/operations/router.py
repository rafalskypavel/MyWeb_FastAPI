import json
import time

from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
from fastapi_cache.decorator import cache
from sqlalchemy import update, delete, and_, insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_async_session
from operations.exceptions import handle_error
from operations.models import product, product_group
from operations.schemas import ProductCreate, ProductUpdate

router = APIRouter(
    prefix="/operations",
    tags=["Operations"]
)


@router.get("/")
async def get_all_products(
        limit: int = Query(5, description="Limit the number of products per page"),
        offset: int = Query(0, description="Offset for pagination"),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        # Проверка и обработка случая с пустыми значениями limit и offset
        if limit <= 0:
            limit = 5  # Значение по умолчанию или другое подходящее
        if offset < 0:
            offset = 0  # Значение по умолчанию или другое подходящее

        query = select(product)
        query = query.limit(limit).offset(offset)
        result = await session.execute(query)
        products = result.fetchall()

        products_data = [{
            "Id": product_row[0],
            "Name": product_row[1],
            "Brand": product_row[2],
            "Price": product_row[4],
            "Сurrency": product_row[6],
            "Availability": product_row[7],
            "Photo": product_row[8],
        } for product_row in products]

        total_products = await session.execute(select(func.count(product.c.id)))
        total_count = total_products.scalar()

        return {"products_data": products_data, "total_count": total_count}
    except Exception as e:
        await handle_error(session, e)


@router.get("/filter")
async def get_filtered_products(
        ids: str = Query(None, description="Filter products by IDs, separated by comma"),
        brands: str = Query(None, description="Filter products by brands, separated by comma"),
        availabilities: str = Query(None, description="Filter products by availabilities, separated by comma"),
        session: AsyncSession = Depends(get_async_session)
):
    if not ids and not brands and not availabilities:
        raise HTTPException(status_code=400,
                            detail="At least one filter parameter (ids, brands, availabilities) must be provided.")

    try:
        products = await fetch_products(ids, brands, availabilities, session)
        if not products:
            error_message = (f"The requested products with IDs: '{ids}', "
                             f"Brands: '{brands}', "
                             f"Availabilities: '{availabilities}' were not found.")
            raise HTTPException(status_code=404, detail=error_message)

        products_data = [{
            "Id": product_row[0],
            "Name": product_row[1],
            "Brand": product_row[2],
            "Price": product_row[4],
            "Сurrency": product_row[6],
            "Availability": product_row[7],
            "Photo": product_row[8],
        } for product_row in products]

        return products_data
    except Exception as e:
        await handle_error(session, e)


async def fetch_products(ids: str, brands: str, availabilities: str, session: AsyncSession):
    id_list = [int(id.strip()) for id in ids.split(",")] if ids else []
    brand_list = [brand.strip() for brand in brands.split(",")] if brands else []
    availability_list = [availability.strip() for availability in availabilities.split(",")] if availabilities else []
    filters = []
    if id_list:
        filters.append(product.c.id.in_(id_list))
    if brand_list:
        filters.append(product.c.brand.in_(brand_list))
    if availability_list:
        filters.append(product.c.availability.in_(availability_list))
    query = select(product)
    if filters:
        query = query.where(and_(*filters))
    result = await session.execute(query)
    return result.fetchall()


@router.post("/")
async def add_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        # Проверка наличия продукта с таким же именем
        existing_product = await session.execute(select(product).where(product.c.name == new_product.name))
        if existing_product.scalar() is not None:
            raise HTTPException(status_code=400, detail="Product with this name already exists")

        product_data = new_product.dict()
        stmt = product.insert().values(**product_data)
        await session.execute(stmt)

        # Добавление группы и подгруппы товаров
        group_id = new_product.group_id
        subgroup_id = new_product.subgroup_id
        if group_id is not None:
            stmt = insert(product_group).values(id=group_id, name="Group Name", parent_id=None)
            await session.execute(stmt)
        if subgroup_id is not None:
            stmt = insert(product_group).values(id=subgroup_id, name="Subgroup Name", parent_id=group_id)
            await session.execute(stmt)

        await session.commit()
        return {"status": "success",
                "data": product_data,
                "details": "Product added successfully"}
    except Exception as e:
        await handle_error(session, e)


@router.put("/{product_id}")
async def update_product(product_id: int, updated_product: ProductUpdate,
                         session: AsyncSession = Depends(get_async_session)):
    try:
        # Проверка наличия продукта
        existing_product = await session.execute(select(product).where(product.c.id == product_id))
        if not existing_product.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Product not found")

        product_data = updated_product.dict(exclude_unset=True)
        stmt = (
            update(product)
            .where(product.c.id == product_id)
            .values(**product_data)
        )
        await session.execute(stmt)
        await session.commit()
        return {"status": "success",
                "data": product_data,
                "details": "Product updated successfully"}
    except Exception as e:
        await handle_error(session, e)


@router.delete("/")
async def delete_product(product_ids: list[int], session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(product).where(product.c.id.in_(product_ids))
        await session.execute(stmt)
        await session.commit()
        return {"status": "success",
                "data": product_ids,
                "details": "Products deleted successfully"}
    except Exception as e:
        await handle_error(session, e)


@router.post("/upload_products/")
async def upload_products(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    try:
        # Чтение данных из загруженного файла JSON
        data = await file.read()
        products_data = json.loads(data)

        # Сохранение данных в базу данных
        for product_data in products_data:
            new_product = ProductCreate(**product_data)
            stmt = insert(product).values(**new_product.dict())
            await session.execute(stmt)
        await session.commit()

        return {"status": "success", "details": "Products uploaded successfully"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in uploaded file")
    except Exception as e:
        await handle_error(session, e)


@router.post("/assign_product_group/{product_id}")
async def assign_product_group(
        product_id: int,
        group_id: int,
        subgroup_id: int = None,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        # Проверяем существование товара
        existing_product = await session.execute(select(product).where(product.c.id == product_id))
        product_row = existing_product.scalar_one_or_none()
        if product_row is None:
            raise HTTPException(status_code=404, detail="Product not found")

        # Проверяем существование группы
        existing_group = await session.execute(select(product_group).where(product_group.c.id == group_id))
        group_row = existing_group.scalar_one_or_none()
        if group_row is None:
            raise HTTPException(status_code=404, detail="Group not found")

        # Проверяем существование подгруппы (если указана)
        if subgroup_id is not None:
            existing_subgroup = await session.execute(select(product_group).where(product_group.c.id == subgroup_id))
            subgroup_row = existing_subgroup.scalar_one_or_none()
            if subgroup_row is None:
                raise HTTPException(status_code=404, detail="Subgroup not found")

        # Обновляем запись товара с новой группой и подгруппой (если указана)
        update_values = {"group_id": group_id, "subgroup_id": subgroup_id}
        stmt = update(product).where(product.c.id == product_id).values(**update_values)
        await session.execute(stmt)
        await session.commit()

        return {"status": "success", "details": "Product group assigned successfully"}
    except HTTPException:
        raise
    except Exception as e:
        await handle_error(session, e)


router2 = APIRouter(
    prefix="/extra",
    tags=["Additional operations router (from operations)"]
)


@router2.get("/fastapi-cache2[redis]", description="Performs a long operation with caching")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return dict(message="Long operation completed")
