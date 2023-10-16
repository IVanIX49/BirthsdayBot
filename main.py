import threading
import telebot
import random
from telebot import types
from datetime import datetime
import time
import json
import pytz

bot = telebot.TeleBot('Your API Key')
birthdays = {}
file_path = 'birthdays.json'
chat_id = -<your_group_chat>
admin_id = <admin_tg_id>

def load_birthdays():
    try:
        with open(file_path, 'r') as file:
            birthdays = json.load(file)
            for key, value in birthdays.items():
                birthdays[key] = datetime.strptime(value, '%Y-%m-%d').date()
    except FileNotFoundError:
        birthdays = {}
    return birthdays

# Сохранение дат рождения в файл
def save_birthdays(birthdays):
    with open(file_path, 'w') as file:
        json.dump(birthdays, file, default=str)

# Загрузка дат рождения при запуске
birthdays = load_birthdays()


@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.from_user.id == admin_id:
        btn1 = types.KeyboardButton('🔥Принял!👍')
        btn2 = types.KeyboardButton('⭐SecretAdminPanel⭐')
        markup.add(btn1,btn2)
        bot.send_message(message.chat.id, "😊Ну здорово! 😎Я лучший и единственный в мире бот, который не забудет вовремя поздравить тебя с днюхой!🎁", reply_markup = markup)
    else:
        btn1 = types.KeyboardButton('🔥Принял!👍')
        markup.add(btn1)
        bot.send_message(message.chat.id, "😊Ну здорово! 😎Я лучший и единственный в мире бот, который не забудет вовремя поздравить тебя с днюхой!🎁", reply_markup = markup)


@bot.message_handler(commands = ['help'])
def hlp(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🔥Принял!👍')
    markup.add(btn1)
    bot.send_message(message.chat.id, "😺Все элементарно! ▶️Для запуска бота напишите '/start', для установки дня рождения '/use' и '/show' - для ручного просмотра людей у которых сегодня день рождения.💥", reply_markup = markup)

# command /set
@bot.message_handler(commands=['set'])
def set_birthday(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    try:
        birthday = datetime.strptime(message.text.split()[1], '%d-%m-%Y').date()
        if (user_id, birthday) not in birthdays.items():
            birthdays[user_id] = birthday
            save_birthdays(birthdays)
            bot.send_message(chat_id, '✅Дата рождения успешно сохранена✅')
        else:
            bot.send_message(chat_id, '❗Вы уже сохраняли эту дату рождения!❗')
    except IndexError:
        bot.send_message(chat_id, 'ℹ️Пожалуйста, введите дату рождения в формате ДД-ММ-ГГГГ после команды /setℹ️')
    except ValueError:
        bot.send_message(chat_id, '❌Некорректный формат даты. Пожалуйста, введите дату рождения в формате ДД-ММ-ГГГГ.❌')
    except Exception:
        bot.send_message(chat_id, 'Неизвестная ошибка!')

# Обработчик команды /show
@bot.message_handler(commands=['show'])
def show_birthdays(message):
    chat_id = message.chat.id
    today = datetime.now(pytz.timezone('Europe/Moscow')).date()
    birthday_users = []
    for user_id, birthday in birthdays.items():
        if today.month == birthday.month and today.day == birthday.day:
            birthday_users.append(user_id)
    if len(birthday_users) > 1:
        message_text = '🎉Сегодня поздравляю с Днем Рождения следующих кентов:🎁\n'
        for user_id in birthday_users:
            user_info = bot.get_chat_member(chat_id=-<group_chat_id>, user_id=user_id)
            username = user_info.user.username
            if str(user_id) not in message_text:
                dyear = today.year - birthdays[user_id].year
                if bot.get_chat(user_id).last_name != None:
                    message_text += f'- Приятель @{username} с ID {user_id}, которого зовут {bot.get_chat(user_id).first_name} {bot.get_chat(user_id).last_name}. Ему сегодня исполняется {dyear} лет \n'
                else:
                    message_text += f'- Приятель @{username} с ID {user_id}, которого зовут {bot.get_chat(user_id).first_name}. Ему сегодня исполняется {dyear} лет \n'
        bot.send_message(message.chat.id, message_text)
    elif len(birthday_users) == 1:
        for user_id in birthday_users:
            user_info = bot.get_chat_member(chat_id=-<group_chat_id>, user_id=user_id)
            username = user_info.user.username
            dyear = today.year - birthdays[user_id].year
            if bot.get_chat(user_id).last_name != None:
                message_text = f'🎂От всей души и сердца поздравляю @{username} {bot.get_chat(user_id).first_name} {bot.get_chat(user_id).last_name}, имеющего ID {user_id} с Днем Рождения! Сегодня ему исполняется {dyear} лет. Желаю счастья, здоровья, а также успехов и благополучия🤑\n'
            else:
                message_text = f'🎂От всей души и сердца поздравляю @{username} {bot.get_chat(user_id).first_name}, имеющего ID {user_id} с Днем Рождения! Сегодня ему исполняется {dyear} лет. Желаю счастья, здоровья, а также успехов и благополучия🤑\n'

        bot.send_message(chat_id, message_text)
    else:
        bot.send_message(message.chat.id, '😥Сегодня нет именинников😥')

@bot.message_handler(commands=['all'])
def showall(message):
    today = datetime.now(pytz.timezone('Europe/Moscow'))
    chat_id = message.chat.id
    message = '😎Список всех дней рождения😎:\n\n'
    c = 0
    for user_id, birthday in birthdays.items():
        c+=1
        dyear = today.year - birthdays[user_id].year
        dmounth = birthdays[user_id].month - today.month
        dday = birthdays[user_id].day - today.day
        if dmounth > 0:
            if bot.get_chat(user_id).last_name != None:
                message+=f' {c}. {bot.get_chat(user_id).first_name} {bot.get_chat(user_id).last_name} через {dmounth} месяца(ев)  исполнится {dyear} лет(год/а)! ({birthdays[user_id].day}.{birthdays[user_id].month}.{birthdays[user_id].year})\n'
            else:
                message += f' {c}. {bot.get_chat(user_id).first_name} через {dmounth} месяца(ев) исполнится {dyear} лет(год/а)! [{birthdays[user_id].day}.{birthdays[user_id].month}.{birthdays[user_id].year}]\n'
        elif dmounth < 0:
            if bot.get_chat(user_id).last_name != None:
                message+=f' {c}. {bot.get_chat(user_id).first_name} {bot.get_chat(user_id).last_name} в этом году исполнилось {dyear} лет(год/а)! [{birthdays[user_id].day}.{birthdays[user_id].month}.{birthdays[user_id].year}]\n'
            else:
                message += f' {c}. {bot.get_chat(user_id).first_name} в этом году исполнилось {dyear} лет(год/а)! [{birthdays[user_id].day}.{birthdays[user_id].month}.{birthdays[user_id].year}]\n'
        else:
            if dday > 0:
                if bot.get_chat(user_id).last_name != None:
                    message+=f' {c}. {bot.get_chat(user_id).first_name} {bot.get_chat(user_id).last_name} через {dday} дней/день/дня будет {dyear} лет(год/а)! [{birthdays[user_id].day}.{birthdays[user_id].month}.{birthdays[user_id].year}]\n'
                else:
                    message += f' {c}. {bot.get_chat(user_id).first_name} через {dday} дней/день/дня будет {dyear} лет(год/а)! [{birthdays[user_id].day}.{birthdays[user_id].month}.{birthdays[user_id].year}]\n'
            elif dday < 0:
                if bot.get_chat(user_id).last_name != None:
                    message+=f' {c}. {bot.get_chat(user_id).first_name} {bot.get_chat(user_id).last_name} в этом месяце исполнилось {dyear} лет(год/а)! [{birthdays[user_id].day}.{birthdays[user_id].month}.{birthdays[user_id].year}]\n'
                else:
                    message += f' {c}. {bot.get_chat(user_id).first_name} в этом месяце исполнилось {dyear} лет(год/а)! [{birthdays[user_id].day}.{birthdays[user_id].month}.{birthdays[user_id].year}]\n'
            else:
                if bot.get_chat(user_id).last_name != None:
                    message+=f' {c}.🎁 {bot.get_chat(user_id).first_name} {bot.get_chat(user_id).last_name} сегодня исполняется {dyear} лет(год/а)! Не забудь его поздравить! [{birthdays[user_id].day}.{birthdays[user_id].month}.{birthdays[user_id].year}]\n'
                else:
                    message += f' {c}.🎁 {bot.get_chat(user_id).first_name} сегодня исполняется {dyear} лет(год/а)! Не забудь его поздравить! [{birthdays[user_id].day}.{birthdays[user_id].month}.{birthdays[user_id].year}]\n'
    bot.send_message(chat_id,message + f'\n🪪Всего сохранено(a) {c} запись(ей).🪪')

@bot.message_handler(commands = ['admshow'])
def admshow(message):
    if message.from_user.id == admin_id:
        bot.send_message(message.chat.id, f'Необработанный "словарь" со всеми ДР:\n {birthdays}')
    else:
        bot.send_message(message.chat.id,'У вас недостаточно прав для выполнения данной команды!')
        bot.send_message(admin_id,f'@{bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id).user.username} попытался получить доступ к файлу базы данных пользователей!')
@bot.message_handler(commands = ['admset'])
def admset(message):
    if message.from_user.id == admin_id:
        chat_id = message.chat.id
        try:
            user_id = str(message.text.split()[1])
            birthday = datetime.strptime(message.text.split()[2], '%d-%m-%Y').date()

            if (user_id, birthday) not in birthdays.items():
                birthdays[user_id] = birthday
                save_birthdays(birthdays)
                bot.send_message(chat_id, '✅Дата рождения успешно сохранена✅')
            else:
                bot.send_message(chat_id, '❗Вы уже сохраняли эту дату рождения!❗')
        except IndexError:
            bot.send_message(chat_id, 'ℹ️Пожалуйста, после команды /admset введите ID пользователя, которого хотите добавить, а затем дату рождения! ℹ️')
        except ValueError:
            bot.send_message(chat_id, '❌Некорректный формат даты или ID пользователя. Пожалуйста, введите дату рождения в формате ДД-ММ-ГГГГ.❌')
        except Exception:
            bot.send_message(chat_id, 'Неизвестная ошибка!')
    else:
        bot.send_message(message.chat.id,'У вас недостаточно прав для выполнения данной команды!')
        bot.send_message(admin_id,f'@{bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id).user.username} только что попытался удаленно добавить ДР пользователя в БД!')
@bot.message_handler(commands = ['admdel'])
def admdel(message):
    if message.from_user.id == admin_id:
        try:
            user_id = str(message.text.split()[1])
            if user_id in birthdays:
                del birthdays[user_id]
                save_birthdays(birthdays)
                bot.send_message(message.chat.id, f'Запись о пользователе с ID {user_id} удалена!')
            else:
                bot.send_message(message.chat.id, 'Запись отсутствует в БД!')
        except KeyError:
            bot.send_message(message.chat.id, 'Очень редкая ошибка! Скорее всего запись отсутствует в БД!')
        except IndexError:
            bot.send_message(message.chat.id, 'Пожалуйста введите валидный ID после команды (/admdel <ИД пользователя>)')
        except Exception:
            bot.send_message(message.chat.id, 'Неизвестная ошибка!')
    else:
        bot.send_message(message.chat.id,'У вас недостаточно прав для выполнения данной команды!')
        bot.send_message(admin_id,f'@{bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id).user.username} только что попытался удалить записи из БД ДР!')


# Обработчик нового дня
def check_new_day(chat_id):
    hr = 6
    mr = 0
    sr = 0
    print("Поток постоянной real-time проверки даты работает!")
    while True:

        now = datetime.now(pytz.timezone('Europe/Moscow'))
        if now.hour == 23 and now.minute == 59 and (now.second == 59 or now.second == 58):
            random.seed(a=None, version=2)
            hr = random.randint(4,9)
            mr = random.randint(0,59)
            sr = random.randint(0,59)
            print(f'Время следующей отправки поздравления - {hr}:{mr}:{sr}')
        if now.hour == hr and now.minute == mr and now.second == sr:
            today = now.date()
            birthday_users = []
            for user_id, birthday in birthdays.items():
                if today.month == birthday.month and today.day == birthday.day:
                    birthday_users.append(user_id)
            if len(birthday_users) > 1:
                message_text = '🎂Сегодня поздравляю с Днем Рождения следующих людей🎂:\n'
                for user_id in birthday_users:
                    user = bot.get_chat(user_id)
                    user_info = bot.get_chat_member(chat_id, user_id=user_id)
                    username = user_info.user.username
                    dyear = today.year - birthdays[user_id].year
                    if user.last_name != None:
                        message_text += f'- Красавец @{username} с ID {user_id} ({user.first_name} {user.last_name}). Ему сегодня исполняется {dyear} лет.\n'
                    else:
                        message_text += f'- Красавец @{username} с ID {user_id} ({user.first_name}). Ему сегодня исполняется {dyear} лет.\n'
                bot.send_message(chat_id, message_text)

            elif len(birthday_users) == 1:
                for user_id in birthday_users:
                    user = bot.get_chat(user_id)
                    user_info = bot.get_chat_member(chat_id, user_id=user_id)
                    username = user_info.user.username
                    dyear = today.year - birthdays[user_id].year
                    if user.last_name != None:
                        message_text = f'🎉От всей души и сердца поздравляю {user.first_name} {user.last_name}, имеющего ID {user_id} с Днем Рождения! @{username} сегодня исполняется {dyear} лет. Желаю счастья, здоровья, а также успехов и благополучия🍻\n'
                    else:
                        message_text = f'🎉От всей души и сердца поздравляю {user.first_name}, имеющего ID {user_id} с Днем Рождения! @{username} сегодня исполняется {dyear} лет. Желаю счастья, здоровья, а также успехов и благополучия🍻\n'
                    bot.send_message(chat_id, message_text)
        time.sleep(1)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '🔥Принял!👍':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('/start')
        btn2 = types.KeyboardButton('/help')
        btn3 = types.KeyboardButton('/set')
        btn4 = types.KeyboardButton('/show')
        btn5 = types.KeyboardButton('/all')
        markup.add(btn1, btn2, btn3, btn4,btn5)
        bot.send_message(message.chat.id, '🤖Открываю меню кнопок с командами🤖', reply_markup=markup) #ответ бота
    elif message.text == '⭐SecretAdminPanel⭐' and message.from_user.id == admin_id:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('/admset')
        btn2 = types.KeyboardButton('/admshow')
        btn3 = types.KeyboardButton('/admdel')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, '🔐Access granted!🔓 Добро пожаловать в админское меню-панель!😎', reply_markup=markup)
    elif message.text == '🕛Время🕛':
        msk = datetime.now(pytz.timezone('Europe/Moscow'))
        kld = datetime.now(pytz.timezone('Europe/Kaliningrad'))
        bot.send_message(message.chat.id, (f'Сейчас в Москве: {msk}\nВремя в Калининграде: {kld}\nСистемное время: {datetime.now()}'))
birthdays = load_birthdays()

new_day_thread = threading.Thread(target=check_new_day, args=(chat_id,))
new_day_thread.start()
print("Бот успешно запущен!")

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть, чтобы не закрывался!