import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

#Задание 1
print ("1) Http-запрос любого типа без параметра method")
response = requests.get(url)
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text}")

#Задание 2
print ("2) Http-запрос не из списка. Например, HEAD")
response = requests.head(url, data={'method': 'HEAD'})
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text}")
#Задание 3
print ("3) Запрос с правильным значением method")
response = requests.get(url, params={'method': 'GET'})
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text}")
#Задание 4
print ("4) Все возможные сочетания реальных типов запроса и значений параметра method")
methods = ['GET', 'POST', 'PUT', 'DELETE']
for test_method in methods:
    for method in methods:
        print(f"  Отправляем {test_method} с method='{method}': ", end="")
        if test_method == 'GET':
            response = requests.get(url, params={'method': method})
        elif test_method == 'POST':
            response = requests.post(url, data={'method': method})
        elif test_method == 'PUT':
            response = requests.put(url, data={'method': method})
        else:
            response = requests.delete(url, data={'method': method})
        print(f"Статус: {response.status_code}")
        print(f"Ответ: '{response.text}'")
