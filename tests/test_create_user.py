import allure
import pytest
from helpers.assertions import assert_response_status, assert_success_response, assert_error_message
from helpers.generators import generate_random_email, generate_random_password, generate_random_name
from helpers.response_messages import UserError

@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, api_client):
        user_data = {
            "email": generate_random_email(),
            "password": generate_random_password(),
            "name": generate_random_name()
        }

        # Создаем пользователя
        create_resp = api_client.create_user(user_data)
        assert_response_status(create_resp, 200)
        assert_success_response(create_resp)

        # Получаем данные пользователя
        get_resp = api_client.get_user(user_data)
        assert_response_status(get_resp, 200)
        assert_success_response(get_resp)
        assert get_resp.json()["user"]["email"] == user_data["email"]
        assert get_resp.json()["user"]["name"] == user_data["name"]

        # Удаляем пользователя
        delete_resp = api_client.delete_user(user_data)
        assert_response_status(delete_resp, 202)

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_duplicate_user_fail(self, api_client):
        user_data = {
            "email": generate_random_email(),
            "password": generate_random_password(),
            "name": generate_random_name()
        }
        # Создаем пользователя первый раз
        create_resp1 = api_client.create_user(user_data)
        assert_response_status(create_resp1, 200)
        assert_success_response(create_resp1)

        # Пытаемся создать повторно
        create_resp2 = api_client.create_user(user_data)
        assert_response_status(create_resp2, 403)
        assert_error_message(create_resp2, UserError.DUPLICATE.value)

        # Удаляем пользователя
        delete_resp = api_client.delete_user(user_data)
        assert_response_status(delete_resp, 202)

    @allure.title("Создание пользователя без заполнения одного из обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_fail(self, api_client, missing_field):
        user_data = {
            "email": generate_random_email(),
            "password": generate_random_password(),
            "name": generate_random_name()
        }
        user_data.pop(missing_field)

        response = api_client.create_user(user_data)
        assert_response_status(response, 403)
        assert_error_message(response, UserError.MISSING_FIELDS.value)
