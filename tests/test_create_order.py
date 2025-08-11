import allure
from helpers.assertions import assert_response_status, assert_success_response, assert_error_message
from helpers.response_messages import OrderError


@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_auth_valid_ingredients_success(self, api_client, user_data, valid_ingredients):
        # Создаем пользователя
        create_resp = api_client.create_user(user_data)
        assert_response_status(create_resp, 200)
        assert_success_response(create_resp)

        # Логинимся
        login_resp = api_client.login_user({
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert_response_status(login_resp, 200)
        token = login_resp.json()["accessToken"]

        # Создаем заказ с авторизацией
        response = api_client.create_order(ingredients=valid_ingredients, token=token)
        assert_response_status(response, 200)
        assert_success_response(response)
        assert "order" in response.json()

        # Удаляем пользователя
        delete_resp = api_client.delete_user(user_data)
        assert_response_status(delete_resp, 202)

    @allure.title("Создание заказа без авторизации и с валидными ингредиентами")
    def test_create_order_no_auth_valid_ingredients_success(self, api_client, valid_ingredients):
        response = api_client.create_order(ingredients=valid_ingredients, token=None)
        assert_response_status(response, 200)
        assert_success_response(response)
        assert "order" in response.json()

    # Аналогично для других тестов — добавляйте создание пользователя и получение токена внутри теста,
    # если он нужен (с авторизацией)

    # ... остальные тесты ...
