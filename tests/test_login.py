import allure
from helpers.assertions import assert_response_status, assert_success_response, assert_error_message
from helpers.response_messages import AuthError



@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Логин под существующим пользователем")
    def test_login_valid_credentials_success(self, api_client, registered_user):
        credentials = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_client.login_user(credentials)

        assert_response_status(response, 200)
        assert_success_response(response)
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

    @allure.title("Логин с неверным логином и паролем")
    def test_login_invalid_credentials_fail(self, api_client, registered_user):
        credentials = {
            "email": registered_user["email"],
            "password": "invalid_password"
        }
        response = api_client.login_user(credentials)

        assert_response_status(response, 401)
        assert_error_message(response, AuthError.INVALID_CREDENTIALS.value)