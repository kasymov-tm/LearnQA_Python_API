import datetime
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email='vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content: {response.content}"

    def test_create_user_with_incorrect_email(self):

        # Cоздание пользователя с некорректным email — без символа @

        data = self.prepare_registration_data()
        data['email'] = 'vinkotovexample.com'  # Убираем @

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        expected_error = "Invalid email format"
        actual_error = response.content.decode("utf-8")
        assert expected_error in actual_error, f"Expected '{expected_error}' in error message, but got '{actual_error}'"

    @pytest.mark.parametrize('missing_field', [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ])
    def test_create_user_missing_required_field(self, missing_field):

        # Cоздание пользователя без одного из обязательных полей.

        data = self.prepare_registration_data()
        # Удаляем одно поле из данных
        data.pop(missing_field)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        expected_error = f"The following required params are missed: {missing_field}"
        actual_error = response.content.decode("utf-8")
        assert expected_error in actual_error, \
            f"Expected '{expected_error}' in error message for missing field '{missing_field}', but got '{actual_error}'"

    def test_create_user_with_short_name(self):

        # Cоздание пользователя с очень коротким именем (1 символ)

        data = self.prepare_registration_data()
        data['firstName'] = 'A'  # Имя из одного символа

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        expected_error = "The value of 'firstName' field is too short"
        actual_error = response.content.decode("utf-8")
        assert expected_error == actual_error, \
            f"Unexpected response content: '{actual_error}'. Expected: '{expected_error}'"

    def test_create_user_with_long_name(self):

        # Cоздание пользователя с очень длинным именем (>250 символов)

        data = self.prepare_registration_data()
        # Создаём имя длиной 251 символ
        long_name = 'A' * 251
        data['firstName'] = long_name

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        expected_error = "The value of 'firstName' field is too long"
        actual_error = response.content.decode("utf-8")
        assert expected_error == actual_error, \
            f"Unexpected response content: '{actual_error}'. Expected: '{expected_error}'"