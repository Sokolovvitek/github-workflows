import requests
import pytest
import json

BASE_URL = "https://hawkingbros.bsite.net/api"

# Функция для логирования ответа
def log_response(endpoint, method, response):
    print("\n" + "=" * 50)
    print(f"🔎 Запрос: {method} {endpoint}")
    print(f"📋 Статус ответа: {response.status_code} - {response.reason}")
    print(f"⏲️ Время ответа: {response.elapsed.total_seconds()} сек")
    print("-" * 50)

    try:
        json_data = response.json()
        print("📥 JSON-ответ:")

        # Форматированный вывод JSON с отступами
        pretty_json = json.dumps(json_data, indent=4, ensure_ascii=False)
        print(pretty_json)

        # Дополнительный вывод ключевых метаданных
        if isinstance(json_data, dict):
            print("\n📊 Ключевые поля:")
            for key in ["Id", "Name", "Description", "TotalProducts"]:
                if key in json_data:
                    print(f"  {key}: {json_data[key]}")

        elif isinstance(json_data, list) and json_data:
            print("\n📝 Пример первого элемента:")
            first_item = json_data[0]
            for key, value in first_item.items():
                print(f"  {key}: {value}")

    except ValueError:
        print("⚠️ Ответ не содержит JSON или некорректный формат данных.")
        print(f"📄 Сырой текст ответа:\n{response.text.encode('utf-8').decode('utf-8')}")

    print("=" * 50)

# Тестируем создание товара в корзине
def test_create_product_in_cart():
    value = 1
    url = f"{BASE_URL}/Admin/create?value={value}"
    response = requests.post(url)

    log_response(url, "POST", response)
    assert response.status_code == 200, f"Ошибка при создании продукта: {response.status_code}"

# Тестируем получение заголовка корзины
def test_get_cart_header():
    url = f"{BASE_URL}/ShoppingCart/header"
    response = requests.get(url)

    log_response(url, "GET", response)
    assert response.status_code == 200, f"Ошибка при получении заголовка корзины: {response.status_code}"

    data = response.json()
    assert "LogoImg" in data
    assert "UsedGuid" in data
    assert "UserName" in data

# Тестируем получение списка продуктов
def test_get_cart_products():
    url = f"{BASE_URL}/ShoppingCart/products"
    response = requests.get(url)

    log_response(url, "GET", response)
    assert response.status_code in [200, 204], f"Ошибка при получении продуктов: {response.status_code}"

    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list), "Ответ должен быть списком продуктов"
        if data:
            product = data[0]
            assert "Id" in product
            assert "Name" in product

# Тестируем удаление всех продуктов из корзины
def test_delete_cart_products():
    url = f"{BASE_URL}/ShoppingCart/products"
    response = requests.delete(url)

    log_response(url, "DELETE", response)
    assert response.status_code == 200, f"Ошибка при удалении продуктов: {response.status_code}"

    data = response.json()
    assert "Name" in data
    assert "Description" in data

# Тестируем удаление конкретного продукта
def test_delete_specific_product():
    url = f"{BASE_URL}/ShoppingCart/product"
    payload = {"ProductId": 0, "UserGuid": "ваш_guid"}

    response = requests.delete(url, json=payload)
    log_response(url, "DELETE", response)
    assert response.status_code == 200, f"Ошибка при удалении продукта: {response.status_code}"

# Тестируем получение сводки корзины
def test_get_cart_summary():
    url = f"{BASE_URL}/ShoppingCart/baskedsummary"
    response = requests.get(url)

    log_response(url, "GET", response)
    assert response.status_code == 200, f"Ошибка при получении сводки корзины: {response.status_code}"

    data = response.json()
    assert "TotalProducts" in data

# Тестируем получение просмотренных товаров
def test_get_viewed_list():
    url = f"{BASE_URL}/ShoppingCart/viewedList"
    response = requests.get(url)

    log_response(url, "GET", response)
    assert response.status_code == 200, f"Ошибка при получении просмотренных товаров: {response.status_code}"
    assert isinstance(response.json(), list)

# Тестируем увеличение количества товара
def test_increment_product_quantity():
    url = f"{BASE_URL}/ShoppingCart/quantityinc"
    payload = {"ProductId": 0, "UserGuid": "ваш_guid"}

    response = requests.post(url, json=payload)
    log_response(url, "POST", response)
    assert response.status_code == 200, f"Ошибка при увеличении количества товара: {response.status_code}"

# Тестируем уменьшение количества товара
def test_decrement_product_quantity():
    url = f"{BASE_URL}/ShoppingCart/quantitydec"
    payload = {"ProductId": 0, "UserGuid": "ваш_guid"}

    response = requests.post(url, json=payload)
    log_response(url, "POST", response)
    assert response.status_code == 200, f"Ошибка при уменьшении количества товара: {response.status_code}"

# Тестируем изменение количества товара
def test_change_product_quantity():
    url = f"{BASE_URL}/ShoppingCart/changequantity"
    payload = {"ProductId": 0, "UserGuid": "ваш_guid", "Value": 1}

    response = requests.post(url, json=payload)
    log_response(url, "POST", response)
    assert response.status_code == 200, f"Ошибка при изменении количества товара: {response.status_code}"

# Тестируем применение скидки
def test_apply_discount():
    url = f"{BASE_URL}/ShoppingCart/discount"
    payload = {"DiscountName": "ваша_скидка", "UsedGuid": "ваш_guid"}

    response = requests.post(url, json=payload)
    log_response(url, "POST", response)
    assert response.status_code == 200, f"Ошибка при применении скидки: {response.status_code}"

# Тестируем удаление скидки
def test_remove_discount():
    url = f"{BASE_URL}/ShoppingCart/discount"
    response = requests.delete(url)

    log_response(url, "DELETE", response)
    assert response.status_code == 200, f"Ошибка при удалении скидки: {response.status_code}"
