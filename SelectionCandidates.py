import requests
from os import getenv

# Загрузка API ключа из переменной окружения
API_KEY = 'APPLGII21QKEARJ6B5P7D96BU82A9OQSULTOGG75C8CQI33I0FTSLR5UC6EH3TGF'
VACANCY_ID = '96449348'  # Замените на актуальный ID вакансии

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "HealthHire/1.0"  # Замените на имя вашего приложения/сервиса
}

try:
    # Запрос для получения списка откликов на конкретную вакансию
    response = requests.get(f'https://api.hh.ru/vacancies/{VACANCY_ID}/negotiations', headers=headers)

    if response.status_code == 200:
        applications = response.json()
        items = applications.get('items', [])

        if items:
            # Вывод информации об откликах
            for application in items:
                print(f"{application['id']}: {application.get('message', 'No message provided')}")
        else:
            print("Список откликов пуст или ключ 'items' отсутствует в ответе.")
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")
        print(response.text)  # Вывод текста ошибки для анализа

except requests.exceptions.RequestException as e:
    print(f"Произошла ошибка при выполнении запроса: {e}")
