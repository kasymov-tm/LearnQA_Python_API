import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

print("Создание задачи")
response = requests.get(url)
data = response.json()

seconds = data["seconds"]
token = data["token"]

print(f"   Задача создана! Ожидание: {seconds} секунд")
print(f"   Токен: {token}")

print("Проверка статуса")
check_before = requests.get(url, params={"token": token})
data_before = check_before.json()

if data_before["status"] == "Job is NOT ready":
    print("Задача ещё не готова")
else:
    print("Ошибка")

print(f"Ждём {seconds} секунд")
time.sleep(seconds)

print("Проверка статуса")
check_after = requests.get(url, params={"token": token})
data_after = check_after.json()

if data_after["status"] == "Job is ready":
    print("Готово")
else:
    print("Ошибка")

if "result" in data_after:
    result = data_after["result"]
    print(f"Результат: {result}")
else:
    print("Ошибка: поля «result» нет")