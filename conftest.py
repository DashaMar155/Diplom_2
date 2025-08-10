import pytest
import allure
from helpers.assertions import assert_response_status, assert_success_response
from helpers.api import StellarBurgersAPI
from helpers.generators import generate_random_email, generate_random_password, generate_random_name


@pytest.fixture
def api_client():
    return StellarBurgersAPI()


@pytest.fixture
def registered_user(api_client):
    user_data = {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": generate_random_name()
    }

    api_client.create_user(user_data)
    return user_data


@pytest.fixture
def auth_token(api_client, registered_user):
    credentials = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    response = api_client.login_user(credentials)
    return response.json()["accessToken"]


@pytest.fixture
def valid_ingredients(api_client):
    response = api_client.get_ingredients()
    ingredients = [ingredient["_id"] for ingredient in response.json()["data"]]
    return ingredients[:2]

@pytest.fixture
def created_user(api_client):
    user_data = {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": generate_random_name()
    }

    with allure.step("Создание тестового пользователя"):
        response = api_client.create_user(user_data)
        assert_response_status(response, 200)
        assert_success_response(response)

    yield user_data

    with allure.step("Удаление тестового пользователя"):
        delete_response = api_client.delete_user(user_data)
        assert_response_status(delete_response, 202)