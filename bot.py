import telebot
import requests
import exchange_rate_for_bot
import speech_recognition as SRG
# import yt_dlp as youtube_dl
from pydub import AudioSegment
from modules import config
from random import randint, choice
from telebot import types
from os import stat
from googletrans import Translator

bot = telebot.TeleBot(config.TOKEN)


# Команды

# start
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == config.AdminID:
        bot.send_message(message.chat.id, f'Приветствую тебя хозяин')
        bot.send_sticker(message.chat.id, open(
            'stikers/KitayPartiya.webp', 'rb'))
    else:
        if message.from_user.last_name == None:
            bot.send_message(
                message.chat.id, f"Привет {message.from_user.first_name}")

        else:
            bot.send_message(
                message.chat.id, f"Привет {message.from_user.first_name} {message.from_user.last_name}")


# help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id, 'Помощь пришла на помощь')
    bot.send_message(message.chat.id, f'''
/start - Запуск/Перезапуск бота
/help - Помощь
/exchange_rate - Узнать курс валюты
/add - Добавить какой-то элемент в список
/remove - Удалить элемент из списка
/check - Посмотреть список
/myid - Узнать мой ID
/random - Случайное число
/hello - поприветствовать бота
/seabattle - Сыграть в морской бой (Переход на сайт)
/thebestwaifu - Отправит фото лучшей вайфу
''')


# exchange rate
@bot.message_handler(commands=['exchange_rate'])
def exchange_rate(message):
    markup = types.InlineKeyboardMarkup(row_width=2)  # resize_keyboard=True,
    USD = types.InlineKeyboardButton(text='Доллар', callback_data='dollar')
    EUR = types.InlineKeyboardButton(text='Евро', callback_data='euro')
    # TJS = types.KeyboardButton('Сомони')
    # UAH = types.KeyboardButton('Гривна')
    # BYN = types.KeyboardButton('Беларусский рубль')
    # KZT = types.KeyboardButton('Тенге')
    # CNY = types.KeyboardButton('Юань')
    # GBP = types.KeyboardButton('Фунт')
    # TRY = types.KeyboardButton('Лира')
    # JPY = types.KeyboardButton('Йена')
    # MDL = types.KeyboardButton('Молдавский лей')
    markup.add(USD, EUR)  # , TJS, UAH, BYN, KZT, CNY, GBP, TRY, JPY, MDL
    bot.send_message(message.chat.id, "Выберите валюту:", reply_markup=markup)


# hello
@bot.message_handler(commands=['hello'])
def hello(message):
    if randint(0, 2) == 0:
        bot.send_message(
            message.chat.id, f'И тебе привет {message.from_user.first_name} {message.from_user.last_name}')
    elif randint(0, 2) == 1:
        bot.send_sticker(message.chat.id, open('stikers/helloprog.webp', 'rb'))
    elif randint(0, 2) == 2:
        bot.send_sticker(message.chat.id, open(
            'stikers/Мяу привет.webp', 'rb'))


# seabatle
@bot.message_handler(commands=['seabattle'])
def seabatle(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Поиграть в морской бой',
               url='https://goodchebureck.github.io/Sea-battle/'))
    bot.send_message(
        message.chat.id, "Поиграйте в морской бой", reply_markup=markup)


# speedwagon
@bot.message_handler(commands=['speedwagon', 'спидвагон', 'thebestwaifu'])
def send_photo_speedwagon(message):
    speedwagon = open('img/SpeedWagon.jpg', 'rb')
    bot.send_photo(message.chat.id, speedwagon)


# myid
@bot.message_handler(commands=['MYID', 'MyId', 'Myid', 'myid'])
def MyId(message):
    bot.send_message(message.chat.id, message.from_user.id)


# random
@bot.message_handler(commands=['random'])
def random(message):
    random_change = types.InlineKeyboardMarkup()
    random_change.add(types.InlineKeyboardButton(text='Диапозон 10', callback_data="range_10"),
                      types.InlineKeyboardButton(text='Диапозон 100', callback_data="range_100"))
    bot.send_message(message.chat.id, f'Выберите диапозон: ',
                     reply_markup=random_change)


# Разные факты о котиках
@bot.message_handler(commands=['catfact'])
def catfact(message):
    tr = Translator()
    response = requests.get("https://catfact.ninja/fact")
    r = response.json()

    text_f = r["fact"]
    trans_word = tr.translate(text_f, dest="ru", src="en")

    bot.send_message(message.chat.id, trans_word.text)

'''# Скачивание видео с youtube
@bot.message_handler(commands=['dowload_from_youtube'])
def youtube_dowloader(message):
    msg = bot.send_message(message.chat.id, "Выбери камень, ножницы или бумагу")
    bot.register_next_step_handler(msg, dowload_from_youtube)

def dowload_from_youtube(message):
    url = message.text
    audio = {'format': 'bestaudio'}
    video = {'format': 'best'}

    audio_downloader = youtube_dl.YoutubeDL(audio)
    audio_full = audio_downloader.extract_info(url)

    video_downloader = youtube_dl.YoutubeDL(video)
    video_full = video_downloader.extract_info(url)

    bot.send_video(message.chat.id, video_full)
    bot.send_audio(message.chat.id, audio_full)'''




# Создание списка пользователя
@bot.message_handler(commands=['add'])  # /add
def add_func(message):
    sent1 = bot.send_message(message.chat.id, 'Что добавить?')
    bot.register_next_step_handler(sent1, add_str)


def add_str(message):
    user_file = str(message.from_user.id) + ".txt"
    with open(f"Users lists/{user_file}", 'a', encoding='utf-8') as user_file:
        user_file.write(str(message.text) + '\n')
    bot.send_message(message.chat.id, str(message.text) + ' добавлено')


@bot.message_handler(commands=['check'])  # /check
def check_list(message):
    try:
        sent2 = bot.send_message(message.chat.id, 'Список:')
        # находим файл.txt соответсвюующий пользователю
        user_file = str(message.from_user.id) + ".txt"
        # считываем инфу из файла
        lines = open(f"Users lists/{user_file}",
                     'r', encoding='utf-8').readlines()
        b = ''
        if stat(f"Users lists/{user_file}").st_size == 0:
            bot.send_message(message.chat.id, "Ваш список пуст")
        else:
            for i in lines:
                b = f'{b + str(lines.index(i)+1)} {i}\n'
            bot.send_message(message.chat.id, str(b))
    except:
        bot.send_message(message.chat.id, "Поймана ошибка")


@bot.message_handler(commands=['remove'])  # /remove
def remove_th(message):
    sent3 = bot.send_message(
        message.chat.id, 'Введите номер строки для удаления')
    bot.register_next_step_handler(sent3, remove_rep)


def remove_rep(message):
    user_file = str(message.from_user.id) + ".txt"
    replace_line(f"Users lists/{user_file}", int(message.text)-1, '')
    bot.send_message(message.chat.id, f"{str(message.text)} элемент удалён")


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

# Камень ножницы бумага
@bot.message_handler(commands=['knbgame'])
def knbgame(message):

    murcup = types.ReplyKeyboardMarkup()
    murcup.add(types.KeyboardButton("Камень"),
               types.KeyboardButton("Ножницы"),
               types.KeyboardButton("Бумага"),
               types.KeyboardButton("/knbgame"))

    msg = bot.send_message(
        message.chat.id, "Выбери камень, ножницы или бумагу", reply_markup=murcup)
    bot.register_next_step_handler(msg, KNB_game)


def KNB_game(message):
    list = ["камень", "ножницы", "бумага"]
    bot_choise = choice(list)
    player_choise = message.text.lower()

    try:
        if bot_choise == player_choise:
            bot.send_message(
                message.chat.id, f"Кукуруза выбрала '{bot_choise}'")
            bot.send_message(message.chat.id, "Ничья")

        elif bot_choise == "камень" and player_choise == "ножницы":
            bot.send_message(
                message.chat.id, f"Кукуруза выбрала '{bot_choise}'")
            bot.send_message(
                message.chat.id, f"Победила Кукуруза 😁, а {message.from_user.first_name} проиграл 🙁")

        elif bot_choise == "ножницы" and player_choise == "бумага":
            bot.send_message(
                message.chat.id, f"Кукуруза выбрала '{bot_choise}'")
            bot.send_message(
                message.chat.id, f"Победила Кукуруза 😏, а {message.from_user.first_name} проиграл 😕")

        elif bot_choise == "бумага" and player_choise == "камень":
            bot.send_message(
                message.chat.id, f"Кукуруза выбрала '{bot_choise}'")
            bot.send_message(
                message.chat.id, f"Победила Кукуруза 🤪, а {message.from_user.first_name} проиграл 😐")

        elif bot_choise == "ножницы" and player_choise == "камень":
            bot.send_message(
                message.chat.id, f"Кукуруза выбрала '{bot_choise}'")
            bot.send_message(
                message.chat.id, f"{message.from_user.first_name} победил. А ловко ты это придумал, я сразу и не поняла, молодец")

        elif bot_choise == "бумага" and player_choise == "ножницы":
            bot.send_message(
                message.chat.id, f"Кукуруза выбрала '{bot_choise}'")
            bot.send_message(
                message.chat.id, f"{message.from_user.first_name} победил. А ловко ты это придумал, я сразу и не поняла, молодец")

        elif bot_choise == "камень" and player_choise == "бумага":
            bot.send_message(
                message.chat.id, f"Кукуруза выбрала '{bot_choise}'")
            bot.send_message(
                message.chat.id, f"{message.from_user.first_name} победил. А ловко ты это придумал, я сразу и не поняла, молодец")
        else:
            bot.send_message(message.chat.id, "Моя твоя не понимать :(")
    except:
        bot.send_message(message.chat.id, "Ошибка 😖")


# Распознавание голоса
def recognise(filename):
    language = 'ru_RU'
    r = SRG.Recognizer()

    with SRG.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            return text
        except:
            return "Ошибка, попробуйте снова"


# Отслежка callback data
@bot.callback_query_handler(func=lambda call: True)
def calldata_handler(call):
    if call.data == "range_10":
        bot.send_message(call.message.chat.id, f"{randint(0, 10)}")
        bot.answer_callback_query(call.data, "")

    elif call.data == "range_100":
        bot.send_message(call.message.chat.id, f"{randint(0, 10)}")
        bot.answer_callback_query(call.data, "")

    elif call.data == "dollar":
        bot.send_message(call.message.chat.id, f"""
Курс доллара: {round(exchange_rate_for_bot.rate_usd)} ({exchange_rate_for_bot.rate_usd})
Изменение: {exchange_rate_for_bot.rate_change_usd}
""")
        bot.answer_callback_query(call.data, "")

    elif call.data == "euro":
        bot.send_message(call.message.chat.id, f"""
Курс евро: {round(exchange_rate_for_bot.rate_eur)} ({exchange_rate_for_bot.rate_eur})
Изменение: {exchange_rate_for_bot.rate_change_eur}
""")
        bot.answer_callback_query(call.data, "")

# Отслежка текста
@bot.message_handler(content_types=["text"])
def text_handler(message):
    if message.text.lower() in ["раскажи факт о кошках", "скажи факт о кошках", "факт о кошках",]:
        catfact(message)

# Отслежка голосовых сообщений
@bot.message_handler(content_types=['voice'])
def voice_processing(message):

    src = f"voice/{message.from_user.id}.ogg"
    dst = f"voice/{message.from_user.id}_result.wav"

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    sound = AudioSegment.from_ogg(src)
    sound.export(dst, format="wav")

    text = recognise(dst)
    bot.reply_to(message, text)

bot.polling(none_stop=True, interval=0)