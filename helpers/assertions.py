def assert_response_status(response, expected_code):
    assert response.status_code == expected_code, \
        f"Expected status {expected_code}, got {response.status_code}"

def assert_success_response(response):
    assert response.json().get("success") is True, \
        "Expected success=True in response"

def assert_error_message(response, expected_message):
    assert response.json().get("message") == expected_message, \
        f"Expected message '{expected_message}', got '{response.json().get('message')}'"
