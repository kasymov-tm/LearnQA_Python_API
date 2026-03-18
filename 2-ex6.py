import requests

redirect = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
first_redirect = redirect.history[0]
second_redirect = redirect.history[1]
third_redirect = redirect.history[2]
fourth_redirect = redirect

print(first_redirect.url)
print(second_redirect.url)
print(third_redirect.url)
print(fourth_redirect.url)
