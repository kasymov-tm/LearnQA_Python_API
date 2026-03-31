from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test checks that we cannot edit user data without authorization")
    def test_edit_user_no_auth(self):

        #Попытка изменения данных пользователя без авторизации.
        #Ожидаем статус 400 и отсутствие изменений данных.

        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        new_name = "Edited Name"
        response2 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})

        Assertions.assert_code_status(response2, 400)

    @allure.description("This test checks that one user cannot edit another user's data")
    def test_edit_user_auth_as_other_user(self):

        #Попытка изменения данных другого пользователя при авторизации как другой пользователь.
        #Ожидаем статус 400 и отсутствие изменений данных.

        first_user_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=first_user_data)
        Assertions.assert_code_status(response1, 200)
        first_user_id = self.get_json_value(response1, "id")

        login_data_first = {
            'email': first_user_data["email"],
            'password': first_user_data["password"]
        }
        response2 = MyRequests.post("/user/login", data=login_data_first)
        auth_sid_first = self.get_cookie(response2, "auth_sid")
        token_first = self.get_header(response2, "x-csrf-token")

        second_user_data = self.prepare_registration_data()
        response3 = MyRequests.post("/user/", data=second_user_data)
        Assertions.assert_code_status(response3, 200)
        second_user_id = self.get_json_value(response3, "id")

        new_email = "edited@example.com"
        response4 = MyRequests.put(
            f"/user/{second_user_id}",
            headers={"x-csrf-token": token_first},
            cookies={"auth_sid": auth_sid_first},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response4, 400)

    @allure.description("This test checks that user cannot change email to invalid format (without @)")
    def test_edit_user_invalid_email(self):

        #Изменение email на некорректный (без символа @) при авторизации тем же пользователем.
        #Ожидаем статус 400 и отсутствие изменений данных.

        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': register_data["email"],
            'password': register_data["password"]
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        invalid_email = "invalid-email.com"  # Без символа @
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": invalid_email}
        )

        Assertions.assert_code_status(response3, 400)

    @allure.description("This test checks that user cannot change firstName to very short value (1 character)")
    def test_edit_user_short_first_name(self):

        #Изменение firstName на очень короткое значение (1 символ) при авторизации тем же пользователем.
        #Ожидаем статус 400 и отсутствие изменений данных.

        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': register_data["email"],
            'password': register_data["password"]
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        short_name = "A"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": short_name}
        )

        Assertions.assert_code_status(response3, 400)