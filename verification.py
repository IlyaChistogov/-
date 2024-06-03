import requests

url = "https://sms.ru/code/call"
data = {
    "phone": "79679051954",  # номер телефона пользователя
    "api_id": "2ED72E61-76C8-5637-3587-2792D47B698C"
}

response = requests.post(url, data=data)

json_data = response.json()
if json_data:  # Получен ответ от сервера
    print(json_data)  # Для дебага
    if json_data["status"] == "OK":  # Запрос выполнился
        print("Звонок выполняется.")
        print("Четырехзначный код (последние 4 цифры номера, с которого мы позвоним пользователю):", json_data["code"])
        print("ID звонка:", json_data["call_id"])
        print("Стоимость звонка:", json_data["cost"], "руб.")
        print("Ваш баланс после звонка:", json_data["balance"], "руб.")
    else:  # Ошибка в запросе
        print("Звонок не может быть выполнен.")
        print("Текст ошибки:", json_data["status_text"])
else:
    print("Запрос не выполнился. Не удалось установить связь с сервером.")
