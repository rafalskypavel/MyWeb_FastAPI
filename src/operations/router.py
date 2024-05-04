from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, and_

from database import get_async_session
from operations.models import product
from operations.schemas import ProductCreate, ProductUpdate

router = APIRouter(
    prefix="/operations",
    tags=["Operations"]
)


@router.get("/")
async def get_all_products(
        ids: str = Query(None, description="Filter products by IDs, separated by comma"),
        brands: str = Query(None, description="Filter products by brands, separated by comma"),
        availabilities: str = Query(None, description="Filter products by availabilities, separated by comma"),
        session: AsyncSession = Depends(get_async_session)
):
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
    products = result.fetchall()  # Получаем все строки результата запроса

    # Преобразуем строки результата в словари с нужными полями каждого товара
    products_data = []
    for product_row in products:
        product_dict = {
            "Id": product_row[0],
            "Name": product_row[1],
            "Brand": product_row[2],
            "Price": product_row[4],  
            "Сurrency": product_row[6],  
            "Availability": product_row[7],  
            "Photo": product_row[8],
        }
        products_data.append(product_dict)

    return products_data


@router.post("/")
async def add_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    product_data = new_product.dict()
    stmt = product.insert().values(**product_data)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.put("/{product_id}")
async def update_product(product_id: int, updated_product: ProductUpdate, session: AsyncSession = Depends(get_async_session)):
    product_data = updated_product.dict(exclude_unset=True)
    stmt = (
        update(product)
        .where(product.c.id == product_id)
        .values(**product_data)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.delete("/")
async def delete_product(product_ids: list[int], session: AsyncSession = Depends(get_async_session)):
    stmt = delete(product).where(product.c.id.in_(product_ids))
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
