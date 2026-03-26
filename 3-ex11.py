import requests

def test_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    cookies = response.cookies

    if len(cookies) == 0:
        print("Cookie не получены")
    else:
        first_cookie = list(cookies)[0]

        print(f"Имя cookie: {first_cookie.name}")
        print(f"Значение cookie: {first_cookie.value}")

        assert first_cookie.name != "", "Ошибка: имя cookie пустое!"
        assert first_cookie.value != "", "Ошибка: значение cookie пустое!"
