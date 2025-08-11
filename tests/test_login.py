import allure
from helpers.assertions import assert_response_status, assert_success_response, assert_error_message
from helpers.response_messages import AuthError
from helpers.generators import generate_random_email, generate_random_password, generate_random_name

@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Логин под существующим пользователем")
    def test_login_valid_credentials_success(self, api_client):
        user_data = {
            "email": generate_random_email(),
            "password": generate_random_password(),
            "name": generate_random_name()
        }

        # Создаем пользователя
        create_resp = api_client.create_user(user_data)
        assert_response_status(create_resp, 200)
        assert_success_response(create_resp)

        # Логинимся с правильными данными
        credentials = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        login_resp = api_client.login_user(credentials)
        assert_response_status(login_resp, 200)
        assert_success_response(login_resp)
        assert "accessToken" in login_resp.json()
        assert "refreshToken" in login_resp.json()

        # Удаляем пользователя
        delete_resp = api_client.delete_user(user_data)
        assert_response_status(delete_resp, 202)

    @allure.title("Логин с неверным логином и паролем")
    def test_login_invalid_credentials_fail(self, api_client):
        user_data = {
            "email": generate_random_email(),
            "password": generate_random_password(),
            "name": generate_random_name()
        }

        # Создаем пользователя
        create_resp = api_client.create_user(user_data)
        assert_response_status(create_resp, 200)
        assert_success_response(create_resp)

        # Пробуем залогиниться с неверным паролем
        credentials = {
            "email": user_data["email"],
            "password": "invalid_password"
        }
        login_resp = api_client.login_user(credentials)
        assert_response_status(login_resp, 401)
        assert_error_message(login_resp, AuthError.INVALID_CREDENTIALS.value)

        # Удаляем пользователя
        delete_resp = api_client.delete_user(user_data)
        assert_response_status(delete_resp, 202)
