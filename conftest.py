import pytest
from helpers.api import StellarBurgersAPI
from helpers.generators import generate_random_email, generate_random_password, generate_random_name

@pytest.fixture
def api_client():
    return StellarBurgersAPI()

@pytest.fixture
def user_data():
    return {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": generate_random_name()
    }

# Фикстура только отдаёт api_client и user_data, логика создания пользователя в тесте
@pytest.fixture
def user(api_client, user_data):
    return api_client, user_data

@pytest.fixture
def valid_ingredients(api_client):
    response = api_client.get_ingredients()
    ingredients = [ingredient["_id"] for ingredient in response.json()["data"]]
    return ingredients[:2]

# Пример теста, где создаётся пользователь и проверяется результат
def test_create_user(user):
    api_client, user_data = user
    response = api_client.create_user(user_data)
    assert response.status_code == 200
    assert response.json().get("success") is True

# Пример теста для авторизации
def test_login_user(user):
    api_client, user_data = user
    api_client.create_user(user_data)
    credentials = {"email": user_data["email"], "password": user_data["password"]}
    response = api_client.login_user(credentials)
    assert response.status_code == 200
    assert "accessToken" in response.json()
