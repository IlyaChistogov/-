import telebot
from telebot import types
import random
import requests

TOKEN = '6476840022:AAGjYn2cYnCpNE0KcJHkuPvU8DIKTKQGkWI'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных о пользователях
user_data = {}



@bot.message_handler(commands=['help'])
def handle_help(message):
    user_id = message.from_user.id
    help_message = "Список доступных команд:\n"
    help_message += "/start - Начать взаимодействие с ботом\n"
    help_message += "/registration - регистрация\n"
    help_message += "/help - Показать список команд и их описания\n"
    bot.send_message(user_id, help_message, reply_markup=generate_markup())

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Привет! Я чат-бот Клиники ухо, горло, нос им. профессора Е.Н. Оленевой и Ваш виртуальный помощник.")
    bot.send_message(user_id, "Спросите у меня, что я умею /help")
    bot.send_message(user_id, "Для начала работы нажмите кнопку registration внизу", reply_markup=generate_markup_registration())



# Обработчик команды /start
@bot.message_handler(commands=['registration'])
def handle_registration(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_yes = types.KeyboardButton("Да")
    item_no = types.KeyboardButton("Нет")
    markup.row(item_yes, item_no)
    bot.send_message(user_id, "Вы уже являетесь пациентом нашей Клиники?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_existing_patient(message):
    user_id = message.from_user.id
    if message.text.lower() == "да":
        bot.send_message(user_id, "Введите ваш контактный номер телефона в формате 7XXXXXXXXX")
        bot.register_next_step_handler(message, process_phone_number)
    elif message.text.lower() == "нет":
        bot.send_message(user_id, "Затычка", reply_markup=generate_markup())




# Функция для обработки номера телефона и отправки звонка для верификации
@bot.message_handler(func=lambda message: True)
def process_phone_number(message):
    user_id = message.from_user.id
    phone_number = message.text
    if len(phone_number) != 11 or not phone_number.startswith("7"):
        bot.send_message(user_id, "Номер телефона должен начинаться с '7' и содержать 11 цифр. Пожалуйста, введите номер ещё раз")
        bot.register_next_step_handler(message, process_phone_number)
        return
    user_data[user_id] = {"phone_number": phone_number}
    bot.send_message(message, "Укажите ФИО пациента строго в формате “Фамилия Имя Отчество”.")
    bot.send_message(message, "Если пациентом является Ваш ребенок, введите только ФИО ребенка.")
    bot.send_message(message, "Пример: Иванов Иван Иванович")
    handle_fio(message)
    # bot.register_next_step_handler(message, handle_last_name)



@bot.message_handler(func=lambda message: True)
def handle_fio(message):
    user_id = message.from_user.id
    fio_parts = message.text.strip().split()
    # Проверяем, что пользователь ввел ровно три слова
    if len(fio_parts) == 3:
        surname, name, patronymic = fio_parts
        user_data[user_id] = {
            'surname': surname,
            'name': name,
            'patronymic': patronymic
        }
        # Ответное сообщение с подтверждением
        bot.reply_to(message, f"Записано: Фамилия - {surname}, Имя - {name}, Отчество - {patronymic}.")
    else:
        # Сообщение об ошибке, если пользователь ввел данные некорректно
        bot.reply_to(message, "Пожалуйста, введите ФИО в формате 'Фамилия Имя Отчество'.")

if __name__ == "__main__":
    bot.polling(none_stop=True)



# Обработчик текстовых сообщений с ожиданием ввода фамилии пациента
@bot.message_handler(func=lambda message: True)
def handle_last_name(message):
    user_id = message.from_user.id
    if user_id in user_data:
        last_name = message.text
        user_data[user_id]["last_name"] = last_name
        bot.send_message(user_id, "Пожалуйста, укажите имя пациента. Если вы являетесь родителем, а пациент – ребёнок, введите имя ребёнка")
        bot.register_next_step_handler(message, handle_first_name)

# Обработчик текстовых сообщений с ожиданием ввода имени пациента
@bot.message_handler(func=lambda message: True)
def handle_first_name(message):
    user_id = message.from_user.id
    if user_id in user_data:
        first_name = message.text
        user_data[user_id]["first_name"] = first_name
        bot.send_message(user_id, "Пожалуйста, укажите отчество пациента. Если вы являетесь родителем, а пациент – ребёнок, введите отчество ребёнка")
        bot.register_next_step_handler(message, handle_middle_name)


# Обработчик текстовых сообщений с ожиданием ввода отчества пациента
@bot.message_handler(func=lambda message: True)
def handle_middle_name(message):
    user_id = message.from_user.id
    if user_id in user_data:
        middle_name = message.text
        user_data[user_id]["middle_name"] = middle_name
        bot.send_message(user_id, "Пожалуйста, укажите год рождения пациента в формате XXYY. Если вы являетесь родителем, а пациент – ребёнок, введите год рождения ребёнка в формате XXYY")
        bot.register_next_step_handler(message, handle_birthday)



@bot.message_handler(func=lambda message: True)
def handle_birthday(message):
    user_id = message.from_user.id
    if user_id in user_data:
        birthday = message.text
        user_data[user_id]["birthday"] = birthday
        # Отправляем запрос на сервер для проверки данных и регистрации
        response = send_registration_request(user_data[user_id])
        if response == "OK":
            # Если ответ "OK", то выполняем звонок для верификации
            verification_code = send_verification_call(user_data[user_id]["phone_number"])
            if verification_code:
                user_data[user_id]["verification_code"] = verification_code
                bot.send_message(user_id, "Сейчас на указанный вами номер телефона будет совершен звонок. Пожалуйста, введите последние четыре цифры телефона, с которого звонят.")
                # Переходим к проверке кода верификации
                entered_code = message.text
                bot.register_next_step_handler(message, handle_verification_code)
            else:
                bot.send_message(user_id, "Произошла ошибка при отправке звонка. Пожалуйста, попробуйте ещё раз.", reply_markup=generate_markup_registration()())
        elif response == "not found":
            bot.send_message(user_id, "Возможно, вы неправильно ввели данные. Попробуйте ещё раз.", reply_markup=generate_markup_registration())
        else:
            bot.send_message(user_id, "Произошла ошибка при регистрации. Попробуйте позже.", reply_markup=generate_markup_registration())




# Обработчик для кода верификации
@bot.message_handler(func=lambda message: True)
def handle_verification_code(message):
    user_id = message.from_user.id
    if user_id in user_data:  #and "waiting_verification" in user_data[user_id] and user_data[user_id]["waiting_verification"]##:
        entered_code = message.text
        actual_code = user_data[user_id].get("verification_code")
        #if actual_code:
        if entered_code == actual_code:
            bot.send_message(user_id, "Регистрация прошла успешно!", reply_markup=generate_markup())
        else:
            bot.send_message(user_id, "Возможно вы вели неправильный код или произошла ошибка, попробуйте пройти регистрацию ещё раз.", reply_markup=generate_markup_registration())
        del user_data[user_id]
       # else:
            #bot.send_message(user_id, "Произошла ошибка. Пожалуйста, попробуйте ещё раз позднее.")



@bot.message_handler(commands=['call'])
def send_verification_call1(phone_number):
    url = "https://sms.ru/code/call"
    data = {
        "phone": phone_number,
        "api_id": "2ED72E61-76C8-5637-3587-2792D47B698C"
    }

    response = requests.post(url, data=data)
    json_data = response.json()
    verification_code = None
    if json_data and json_data["status"] == "OK":
        print("Звонок выполняется.")
        print("Четырехзначный код (последние 4 цифры номера, с которого мы позвоним пользователю):", json_data["code"])
        verification_code = json_data["code"]
    else:
        print("Звонок не может быть выполнен.")
        print("Текст ошибки:", json_data.get("status_text"))
    return verification_code
    handle_verification_code(message)




# Функция для отправки запроса на звонок для верификации и получения кода
def send_verification_call(phone_number):
    url = "https://sms.ru/code/call"
    data = {
        "phone": phone_number,
        "api_id": "2ED72E61-76C8-5637-3587-2792D47B698C"
    }

    response = requests.post(url, data=data)
    json_data = response.json()
    verification_code = None
    if json_data and json_data["status"] == "OK":
        print("Звонок выполняется.")
        print("Четырехзначный код (последние 4 цифры номера, с которого мы позвоним пользователю)", json_data["code"])
        verification_code = json_data["code"]
    else:
        print("Звонок не может быть выполнен.")
        print("Текст ошибки:", json_data.get("status_text"))
    return verification_code


# Обработчик для кода верификации
#@bot.message_handler(func=lambda message: True)
#def handle_verification_code(message):
#    user_id = message.from_user.id
#    if user_id in user_data:
#        entered_code = message.text
#        actual_code = user_data[user_id].get("verification_code")
#        if actual_code:
#            if entered_code == actual_code:
#                bot.send_message(user_id, "Регистрация прошла успешно!")
#            else:
#                bot.send_message(user_id, "Попробуйте ещё раз.")
#            del user_data[user_id]
#        else:
#            bot.send_message(user_id, "Произошла ошибка. Пожалуйста, попробуйте ещё раз позднее.")


# Функция для отправки запроса на сервер для регистрации пациента
def send_registration_request(user_data):
    HEADER = {
        "Content-Type": "application/json"
    }

    data = {"first_name": user_data["first_name"],
            "second_name": user_data["middle_name"],
            "last_name": user_data["last_name"],
            "mobile_phone": user_data["phone_number"],
            "birthday": user_data["birthday"]}

    response = requests.post(f" http://46.146.229.242:1980/AppFindPac", headers=HEADER, json=data)

    print(response)
    result = response.json()
    print(result)
    print(result['status_code'])
    print(result['result'])
    return result['result']

# Функция для отправки запроса на звонок для верификации и получения кода
# def send_verification_call(phone_number):
#     url = "https://sms.ru/code/call"
#     data = {
#         "phone": phone_number,
#         "api_id": "2ED72E61-76C8-5637-3587-2792D47B698C"
#     }
#
#     response = requests.post(url, data=data)
#     json_data = response.json()
#     verification_code = None
#     if json_data:
#         if json_data["status"] == "OK":
#             print("Звонок выполняется.")
#             print("Четырехзначный код (последние 4 цифры номера, с которого мы позвоним пользователю):", json_data["code"])
#             verification_code = json_data["code"]
#             print("ID звонка:", json_data["call_id"])
#             print("Стоимость звонка:", json_data["cost"], "руб.")
#             print("Ваш баланс после звонка:", json_data["balance"], "руб.")
#         else:
#             print("Звонок не может быть выполнен.")
#             print("Текст ошибки:", json_data["status_text"])
#     else:
#         print("Запрос не выполнился. Не удалось установить связь с сервером.")
#     return verification_code




# Функция для генерации клавиатуры с кнопками "Да" и "Нет"
def yes_no_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_yes = types.KeyboardButton("Да")
    item_no = types.KeyboardButton("Нет")
    markup.add(item_yes, item_no)
    return markup

def generate_markup_registration():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item_registration = types.KeyboardButton("/registration")
    markup.add(item_registration)
    return markup



# Функция для генерации клавиатуры с кнопкой "Помощь"
def generate_markup():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item_help = types.KeyboardButton("/help")
    markup.add(item_help)
    return markup


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
