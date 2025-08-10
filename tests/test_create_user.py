import allure
import pytest
from helpers.assertions import assert_response_status, assert_success_response, assert_error_message
from helpers.generators import generate_random_email, generate_random_password, generate_random_name
from helpers.response_messages import UserError



@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, api_client, created_user):
        response = api_client.get_user(created_user)
        assert_response_status(response, 200)
        assert_success_response(response)
        assert response.json()["user"]["email"] == created_user["email"]
        assert response.json()["user"]["name"] == created_user["name"]

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_duplicate_user_fail(self, api_client, registered_user):
        response = api_client.create_user(registered_user)
        assert_response_status(response, 403)
        assert_error_message(response, UserError.DUPLICATE.value)

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