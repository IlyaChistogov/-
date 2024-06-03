import requests

# Замените YOUR_CLIENT_ID и YOUR_CLIENT_SECRET на ваши реальные данные
CLIENT_ID = 'SF8SD977TROP1QT1UL89OKSQ8T89SAAI6TDHFD1NRTBOS6E9VF24G5I58DMJT7E5'
CLIENT_SECRET = 'GQO05KIBO38VBPTSNVJ0DR6N1GH8Q5UBEH380HBH0UPJ001TVB65TIJQ9J4PE4BF'

# URL для запроса токена доступа
token_url = 'https://hh.ru/oauth/token'

# Параметры запроса
payload = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}

# Отправка POST-запроса для получения токена доступа
response = requests.post(token_url, data=payload)

# Проверка статуса ответа
if response.status_code == 200:
    # Обработка JSON-ответа
    token_data = response.json()
    # Вывод Access Token
    access_token = token_data.get('access_token')
    print("Access Token:", access_token)
else:
    print(f"Ошибка: {response.status_code}")