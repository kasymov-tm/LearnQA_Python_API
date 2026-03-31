import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User deletion cases")
class TestUserDelete(BaseCase):

    @allure.description("This test checks that we cannot delete user with ID 2 (protected user)")
    def test_delete_protected_user(self):

        # Попытка удаления пользователя с ID 2 — защищённого пользователя.
        # Ожидаем статус 400 и сообщение, что нельзя удалить этого пользователя.

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "Unexpected error message when trying to delete protected user"
        )

    @allure.description("This test successfully deletes just created user")
    def test_delete_just_created_user(self):

        # Позитивный тест: создаём пользователя, удаляем его и убеждаемся, что он удалён.

        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        email = register_data["email"]
        password = register_data["password"]

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(f"/user/{user_id}")

        Assertions.assert_code_status(response4, 404)

    @allure.description("This test checks that one user cannot delete another user")
    def test_delete_user_auth_as_other_user(self):

        # Негативный тест: попытка удалить пользователя, будучи авторизованным другим пользователем.
        # Ожидаем статус 400 или 403 и отсутствие удаления.

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

        response4 = MyRequests.delete(
            f"/user/{second_user_id}",
            headers={"x-csrf-token": token_first},
            cookies={"auth_sid": auth_sid_first}
        )

        Assertions.assert_code_status(response4, 400)

        response5 = MyRequests.get(f"/user/{second_user_id}")
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_has_key(response5, "username")