import requests

HEADER = {
    "Content-Type": "application/json"
}

data = {"first_name": "Илья", "second_name": "Дмитривич", "last_name": "Чистогов", "mobile_phone": "79679051954", "birthday": "2003"}

response = requests.post(f" http://46.146.229.242:1980/AppFindPac", headers=HEADER, json=data)

print(response)
result = response.json()
print(result)
print(result['status_code'])
print(result['result'])




'''@bot.message_handler(func=lambda message: True)
def handle_birthday(message):
    user_id = message.from_user.id
    if user_id in user_data:
        birthday = message.text
        user_data[user_id]["birthday"] = birthday
        # Отправляем запрос на сервер для проверки данных и регистрации
        response = send_registration_request(user_data[user_id])
        if response == "OK":
            # Если ответ "OK", то выполняем звонок для верификации
            send_verification_call(user_data[user_id]["phone_number"])
            bot.send_message(user_id, "Сейчас на указанный вами номер телефона будет совершен звонок. Пожалуйста, введите последние четыре цифры телефона, с которого звонят.")
        elif response == "not found":
            send_verification_call(user_data[user_id]["phone_number"])
            bot.send_message(user_id, "Сейчас на указанный вами номер телефона будет совершен звонок. Пожалуйста, введите последние четыре цифры телефона, с которого звонят.")
            #bot.send_message(user_id, "Возможно, вы неправильно ввели данные. Попробуйте ещё раз.", reply_markup=generate_markup())
        else:
            bot.send_message(user_id, "Произошла ошибка при регистрации. Попробуйте позже.")'''


"""import requests

HEADER = {
    "Content-Type": "application/json"
}

data = {"mobile_phone": "79679051954"}

response = requests.post(f" http://46.146.229.242:1980/AppFindPac", headers=HEADER, json=data)

print(response)
result = response.json()
print(result)"""