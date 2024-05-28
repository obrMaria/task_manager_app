import requests

url = 'http://127.0.0.1:5000/users'  # Замените этот URL на тот, к которому хотите обратиться

response = requests.get(url)

if response.status_code == 200:
    users = response.json()
    print('Список пользователей:', users)
else:
    print('Не удалось получить список пользователей. Код ошибки:', response.status_code)
