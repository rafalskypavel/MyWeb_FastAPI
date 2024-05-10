import pytest
from httpx import AsyncClient

async def test_add_product(ac: AsyncClient):
    new_product_data = {
        "id": 1,
        "name": "New Product",
        "brand": "Brand X",
        "description": "A new product",
        "price": 100.0,
        "old_price": 90.0,
        "currency": "USD",
        "availability": "in_stock",
        "images": {"image1": "url1", "image2": "url2"}
    }
    response = await ac.post("/operations/", json=new_product_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


async def test_get_products_with_filter(ac: AsyncClient):
    # Создаем новый продукт
    new_product_data = {
        "id": 1,
        "name": "New Product",
        "brand": "Brand X",
        "description": "A new product",
        "price": 100.0,
        "old_price": 90.0,
        "currency": "USD",
        "availability": "in_stock",
        "images": {"image1": "url1", "image2": "url2"}
    }
    await ac.post("/operations/", json=new_product_data)

    # Запрашиваем продукт по фильтру
    response = await ac.get("/operations/?brands=Brand%20X")
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 1

    # Проверяем, что полученный продукт соответствует созданному
    assert products[0]["Id"] == 1
    assert products[0]["Name"] == "New Product"
    assert products[0]["Brand"] == "Brand X"
    assert products[0]["Price"] == 100.0
    assert products[0]["Сurrency"] == "USD"
    assert products[0]["Availability"] == "in_stock"
