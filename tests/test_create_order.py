import allure
from helpers.assertions import assert_response_status, assert_success_response, assert_error_message
from helpers.response_messages import OrderError



@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и валидными ингридиентами")
    def test_create_order_auth_valid_ingredients_success(
            self, api_client, auth_token, valid_ingredients
    ):
        response = api_client.create_order(
            ingredients=valid_ingredients,
            token=auth_token
        )
        assert_response_status(response, 200)
        assert_success_response(response)
        assert "order" in response.json()

    @allure.title("Создание заказа без авторизации и с валидными ингридиентами")
    def test_create_order_no_auth_valid_ingredients_success(
            self, api_client, valid_ingredients
    ):
        response = api_client.create_order(
            ingredients=valid_ingredients,
            token=None
        )
        assert_response_status(response, 200)
        assert_success_response(response)
        assert "order" in response.json()

    @allure.title("Создание заказа без ингридиентов (с авторизацией)")
    def test_create_order_missing_ingredients_with_auth_fail(
            self, api_client, auth_token
    ):
        response = api_client.create_order(
            ingredients=[],
            token=auth_token
        )
        assert_response_status(response, 400)
        assert_error_message(response, OrderError.MISSING_INGREDIENTS.value)

    @allure.title("Создание заказа без ингридиентов (без авторизации)")
    def test_create_order_missing_ingredients_no_auth_fail(
            self, api_client
    ):
        response = api_client.create_order(
            ingredients=[],
            token=None
        )
        assert_response_status(response, 400)
        assert_error_message(response, OrderError.MISSING_INGREDIENTS.value)

    @allure.title("Создание заказа с неверным хешем ингредиентов (с авторизацией)")
    def test_create_order_invalid_hash_with_auth_fail(
            self, api_client, auth_token
    ):
        response = api_client.create_order(
            ingredients=["invalid_hash_1", "invalid_hash_2"],
            token=auth_token
        )
        assert_response_status(response, 500)
        assert_error_message(response, OrderError.INVALID_HASH.value)

    @allure.title("Создание заказа с неверным хешем ингредиентов (без авторизации)")
    def test_create_order_invalid_hash_no_auth_fail(
            self, api_client
    ):
        response = api_client.create_order(
            ingredients=["invalid_hash_1", "invalid_hash_2"],
            token=None
        )
        assert_response_status(response, 500)
        assert_error_message(response, OrderError.INVALID_HASH.value)