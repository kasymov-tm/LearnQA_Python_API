import requests

def test_header():
    url = "https://playground.learnqa.ru/api/homework_header"
    response = requests.get(url)
    headers = response.headers

    if len(headers) == 0:
        print("Headers не получены")
    else:

        for header_name in headers:
            header_value = headers[header_name]
            print(f"  {header_name}: {header_value}")

        assert 'Content-Type' in headers, "Ошибка: заголовок 'Content-Type' не найден"

        content_type_value = headers['Content-Type']
        assert content_type_value != "", "Ошибка: значение 'Content-Type' пустое"
