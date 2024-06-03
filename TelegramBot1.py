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
    bot.send_message(user_id, "Привет! Я чат-бот Клиники ухо, горло, нос им. профессора Е.Н. Оленевой и Ваш виртуальный помощник.\nСпросите у меня, что я умею /help\nДля начала работы нажмите кнопку /registration внизу", reply_markup=generate_markup_registration())



# Обработчик команды /start
@bot.message_handler(commands=['registration'])
def handle_registration(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_yes = types.KeyboardButton("Да")
    item_no = types.KeyboardButton("Нет")
    markup.row(item_yes, item_no)
    bot.send_message(user_id, "Вы уже являетесь пациентом нашей Клиники?", reply_markup=markup)

def generate_markup_registration():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item_registration = types.KeyboardButton("/registration")
    markup.add(item_registration)
    return markup


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
    user_data[user_id] = {}
    user_data[user_id]["phone_number"] = phone_number
    #handle_fio(message)
    bot.send_message(user_id, "Укажите ФИО пациента строго в формате “Фамилия Имя Отчество”.\nЕсли пациентом является Ваш ребенок, введите только ФИО ребенка.\nПример: Иванов Иван Иванович")
    bot.register_next_step_handler(message, handle_fio_process)

#@bot.message_handler(func=lambda message: True)
#def handle_fio(message):
#    user_id = message.from_user.id
#    bot.send_message(user_id, "Укажите ФИО пациента строго в формате “Фамилия Имя Отчество”.\nЕсли пациентом является Ваш ребенок, введите только ФИО ребенка.\nПример: Иванов Иван Иванович")
#    bot.register_next_step_handler(message, handle_fio_process)


@bot.message_handler(func=lambda message: True)
def handle_fio_process(message):
    user_id = message.from_user.id
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_good = types.KeyboardButton("Всё верно")
    item_no_good = types.KeyboardButton("Указать ФИО ещё раз")
    markup2.row(item_good, item_no_good)
    fio_parts = message.text
    fio_parts = message.text.strip().split()
    # Проверяем, что пользователь ввел ровно три слова
    if len(fio_parts) == 3:
        last_name, first_name, middle_name = fio_parts
        user_data[user_id]["last_name"] = last_name
        user_data[user_id]["first_name"] = first_name
        user_data[user_id]["middle_name"] = middle_name
        # Ответное сообщение с подтверждением
        bot.send_message(user_id, f"Проверьте, пожалуйста, в правильном ли формате вы ввели ФИО пациента:\nФамилия - {last_name}, Имя - {first_name}, Отчество - {middle_name}.\nНажмите кнопку ниже", reply_markup=markup2)
        bot.register_next_step_handler(message, handle_verification)  # Регистрируем следующий обработчик для кнопок
    else:
        # Сообщение об ошибке, если пользователь ввел данные некорректно
        bot.send_message(user_id, "Пожалуйста, введите ФИО в формате 'Фамилия Имя Отчество'.")
        bot.register_next_step_handler(message, handle_fio_process)

# Обработчик для кнопок "Всё верно" и "Указать ФИО ещё раз"
def handle_verification(message):
    user_id = message.from_user.id
    if message.text.lower() == "всё верно":
        bot.send_message(user_id, "Укажите год рождения пациента в формате YYYY.\nЕсли пациентом является Ваш ребенок, введите только год рождения ребенка в формате YYYY.\nПример: 2003")
        bot.register_next_step_handler(message, handle_middle_name)
    elif message.text.lower() == "указать фио ещё раз":
        bot.send_message(user_id, "Укажите ФИО пациента строго в формате “Фамилия Имя Отчество”.\nЕсли пациентом является Ваш ребенок, введите только ФИО ребенка.\nПример: Иванов Иван Иванович")
        bot.register_next_step_handler(message, handle_fio_process)




# Обработчик текстовых сообщений с ожиданием ввода отчества пациента
@bot.message_handler(func=lambda message: True)
def handle_middle_name(message):
    user_id = message.from_user.id
    birthday = message.text
    if len(birthday) != 4:
        bot.send_message(user_id, "Год рождения должен содержать 4 цифры. Пожалуйста, введите год рождения ещё раз")
        bot.register_next_step_handler(message, handle_middle_name)
        return
    user_data[user_id]["birthday"] = birthday
    handle_birthday(message)






@bot.message_handler(func=lambda message: True)
def handle_birthday(message):
    user_id = message.from_user.id
    if user_id in user_data:
        #birthday = message.text
        #user_data[user_id]["birthday"] = birthday
        # Отправляем запрос на сервер для проверки данных и регистрации
        response = send_registration_request(user_data[user_id])
        if response == "OK":
            # Если ответ "OK", то выполняем звонок для верификации
            phone_number = user_data[user_id]["phone_number"]
            verification_code = send_verification_call(user_id, phone_number)
            if verification_code:
                # Сохраняем код верификации в user_data
                user_data[user_id]["verification_code"] = verification_code
                # Отправляем сообщение о вводе кода верификации
                bot.send_message(user_id, "В течение нескольких секунд на указанный Вами номер телефона поступит звонок-сброс с уникального номера. Вам нужно ввести последние 4 цифры этого номера.\nПример: 3487")
                # После отправки сообщения о вводе кода верификации, регистрируем обработчик для кода
                bot.register_next_step_handler(message, handle_verification_code)
            else:
                bot.send_message(user_id, "Произошла ошибка при отправке звонка. Пожалуйста, попробуйте ещё раз.", reply_markup=generate_markup_registration())
        elif response == "not found":
            bot.send_message(user_id, "Возможно, вы неправильно ввели данные. Попробуйте ещё раз.", reply_markup=generate_markup_registration())
        else:
            bot.send_message(user_id, "Произошла ошибка при регистрации. Попробуйте позже.", reply_markup=generate_markup_registration())






# Функция для отправки запроса на звонок для верификации и получения кода
def send_verification_call(user_id, phone_number):
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
@bot.message_handler(func=lambda message: True)
def handle_verification_code(message):
    user_id = message.from_user.id
    if user_id in user_data:
        entered_code = message.text
        actual_code = user_data[user_id].get("verification_code")
        verification_code = user_data[user_id].get("verification_code")  # Получаем код верификации из user_data
        entered_code = int(entered_code)
        verification_code = int(verification_code)
        print("Entered code:", entered_code)  # Выводим введенный код для отладки
        print("Stored verification code:", verification_code)  # Выводим сохраненный код для отладки
        if verification_code is not None:  # Проверяем, есть ли код верификации
            if entered_code == verification_code:
                bot.send_message(user_id, "Регистрация прошла успешно!", reply_markup=generate_markup())
            elif entered_code != verification_code:
                bot.send_message(user_id, "Возможно вы вели неправильный код или произошла ошибка, попробуйте пройти регистрацию ещё раз.", reply_markup=generate_markup_registration())
            del user_data[user_id]
        else:
            bot.send_message(user_id, "Произошла ошибка. Пожалуйста, попробуйте ещё раз позднее.")
            del user_data[user_id]



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


# Функция для генерации клавиатуры с кнопками "Да" и "Нет"
def yes_no_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_yes = types.KeyboardButton("Да")
    item_no = types.KeyboardButton("Нет")
    markup.add(item_yes, item_no)
    return markup


# Функция для генерации клавиатуры с кнопками "Да" и "Нет"
def good_no_markup():
    markup2 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_good = types.KeyboardButton("Всё верно")
    item_no_good = types.KeyboardButton("Указать ФИО ещё раз")
    markup2.add(item_good, item_no_good)
    return markup2



# Функция для генерации клавиатуры с кнопкой "Помощь"
def generate_markup():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item_help = types.KeyboardButton("/help")
    markup.add(item_help)
    return markup


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
