
import telebot
from telebot import types

# Вставь сюда свой API токен, который дал BotFather
bot = telebot.TeleBot('8311827359:AAHViPd8fAk0hRMVmmHJNtro4VxhlmHf2_4')

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Создаем клавиатуру
    item1 = types.KeyboardButton("Цена")  # Кнопка для прайса
    item2 = types.KeyboardButton("Договор оферты")  # Кнопка для договора
    item3 = types.KeyboardButton("Обратная связь")  # Кнопка для обратной связи

    markup.add(item1, item2, item3)  # Добавляем кнопки на клавиатуру

    # Отправляем сообщение с кнопками
    bot.send_message(
        message.chat.id,
        "Привет! Добро пожаловать в бот!\n\n"
        "Этот бот научит тебя создавать и монетизировать AI-аватара с нуля!",
        reply_markup=markup
    )

# Обработчик кнопки "Цена"
@bot.message_handler(func=lambda message: message.text == "Цена")
def price(message):
    bot.send_message(message.chat.id, "Цена за гайд: 690 рублей.")

# Обработчик кнопки "Договор оферты"
@bot.message_handler(func=lambda message: message.text == "Договор оферты")
def offer(message):
    bot.send_message(message.chat.id, "https://docs.google.com/document/d/17eEBGv6G-LzUcZpyvygfLzJT-W_BloOs/edit?usp=sharing&ouid=107708342823288631650&rtpof=true&sd=true")

# Обработчик кнопки "Обратная связь"
@bot.message_handler(func=lambda message: message.text == "Обратная связь")
def contact(message):
    bot.send_message(message.chat.id, "Mara102@mail.ru")

import threading
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# Запускаем веб-сервер
threading.Thread(target=run_web).start()

# Запускаем бота
bot.polling()

