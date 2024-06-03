import requests

def get_responses(vacancy_id, access_token, status="active", page=0, per_page=20):
    url = f"https://api.hh.ru/negotiations?status={status}&vacancy_id={vacancy_id}&page={page}&per_page={per_page}"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch responses. Status code: {response.status_code}")
        return None

# Пример использования
if __name__ == "__main__":
    vacancy_id = "96449348"  # Замените на ID интересующей вакансии
    access_token = "APPLGII21QKEARJ6B5P7D96BU82A9OQSULTOGG75C8CQI33I0FTSLR5UC6EH3TGF"  # Замените на ваш OAuth токен

    responses = get_responses(vacancy_id, access_token)
    if responses:
        print("Список откликов:")
        for response in responses['items']:
            print(f"Отклик ID: {response['id']}, Состояние: {response['state']['name']}")
    else:
        print("Не удалось получить список откликов.")
