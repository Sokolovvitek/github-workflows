import requests
import pytest

BASE_URL = "https://hawkingbros.bsite.net/api"

# Тестируем создание товаров в корзине
def test_create_product_in_cart():
    value = 1
    url = f"{BASE_URL}/Admin/create?value={value}"
    
    response = requests.post(url)
    assert response.status_code == 200, f"Ошибка при создании продукта: {response.status_code}"

# Тестируем получение заголовка корзины
def test_get_cart_header():
    url = f"{BASE_URL}/ShoppingCart/header"
    
    response = requests.get(url)
    assert response.status_code == 200, f"Ошибка при получении заголовка корзины: {response.status_code}"
    
    # Проверяем структуру ответа
    data = response.json()
    assert "LogoImg" in data
    assert "UsedGuid" in data
    assert "UserName" in data

# Тестируем получение списка продуктов
def test_get_cart_products():
    url = f"{BASE_URL}/ShoppingCart/products"
    
    response = requests.get(url)
    assert response.status_code in [200, 204], f"Ошибка при получении продуктов: {response.status_code}"
    
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list), "Ответ должен быть списком продуктов"
        
        # Проверяем структуру первого продукта
        if data:
            product = data[0]
            assert "Id" in product
            assert "Name" in product
            assert "Description" in product
            assert "Quantity" in product
            assert "Unit" in product
            assert "Сurrency" in product
            assert "Price" in product
            assert "DiscountedPrice" in product
            assert "Images" in product

# Тестируем удаление всех продуктов в корзине
def test_delete_cart_products():
    url = f"{BASE_URL}/ShoppingCart/products"
    
    response = requests.delete(url)
    assert response.status_code == 200, f"Ошибка при удалении продуктов: {response.status_code}"
    
    data = response.json()
    assert "Name" in data
    assert "Description" in data

# Тестируем удаление конкретного продукта из корзины
def test_delete_specific_product():
    url = f"{BASE_URL}/ShoppingCart/product"
    payload = {
        "ProductId": 0,  # Укажите актуальный ID продукта
        "UserGuid": "ваш_guid"  # Укажите актуальный GUID пользователя
    }
    
    response = requests.delete(url, json=payload)
    assert response.status_code == 200, f"Ошибка при удалении продукта: {response.status_code}"

    data = response.json()
    assert "Name" in data
    assert "Description" in data

# Тестируем получение сводки корзины
def test_get_cart_summary():
    url = f"{BASE_URL}/ShoppingCart/baskedsummary"
    
    response = requests.get(url)
    assert response.status_code == 200, f"Ошибка при получении сводки корзины: {response.status_code}"

    data = response.json()
    assert "TotalProducts" in data
    assert "Discount" in data
    assert "Total" in data

# Тестируем получение просмотренных товаров
def test_get_viewed_list():
    url = f"{BASE_URL}/ShoppingCart/viewedList"
    
    response = requests.get(url)
    assert response.status_code == 200, f"Ошибка при получении просмотренных товаров: {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком просмотренных товаров"

# Тестируем увеличение количества товара в корзине
def test_increment_product_quantity():
    url = f"{BASE_URL}/ShoppingCart/quantityinc"
    payload = {
        "ProductId": 0,  # Укажите актуальный ID продукта
        "UserGuid": "ваш_guid"  # Укажите актуальный GUID пользователя
    }
    
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Ошибка при увеличении количества товара: {response.status_code}"

    data = response.json()
    assert "Name" in data
    assert "Description" in data

# Тестируем уменьшение количества товара в корзине
def test_decrement_product_quantity():
    url = f"{BASE_URL}/ShoppingCart/quantitydec"
    payload = {
        "ProductId": 0,  # Укажите актуальный ID продукта
        "UserGuid": "ваш_guid"  # Укажите актуальный GUID пользователя
    }
    
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Ошибка при уменьшении количества товара: {response.status_code}"

    data = response.json()
    assert "Name" in data
    assert "Description" in data

# Тестируем изменение количества товара в корзине
def test_change_product_quantity():
    url = f"{BASE_URL}/ShoppingCart/changequantity"
    payload = {
        "ProductId": 0,  # Укажите актуальный ID продукта
        "UserGuid": "ваш_guid",  # Укажите актуальный GUID пользователя
        "Value": 1  # Укажите новое количество
    }
    
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Ошибка при изменении количества товара: {response.status_code}"

    data = response.json()
    assert "Name" in data
    assert "Description" in data

# Тестируем применение скидки
def test_apply_discount():
    url = f"{BASE_URL}/ShoppingCart/discount"
    payload = {
        "DiscountName": "ваша_скидка",  # Укажите актуальное имя скидки
        "UsedGuid": "ваш_guid"  # Укажите актуальный GUID пользователя
    }
    
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Ошибка при применении скидки: {response.status_code}"

    data = response.json()
    assert "Name" in data
    assert "Description" in data

# Тестируем удаление скидки
def test_remove_discount():
    url = f"{BASE_URL}/ShoppingCart/discount"
    
    response = requests.delete(url)
    assert response.status_code == 200, f"Ошибка при удалении скидки: {response.status_code}"

    data = response.json()
    assert "Name" in data
    assert "Description" in data
