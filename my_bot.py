
import telebot
from telebot import types

# Вставь сюда свой API токен, который дал BotFather
bot = telebot.TeleBot('8311827359:AAHViPd8fAk0hRMVmmHJNtro4VxhlmHf2_4')

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Создаем клавиатуру
    item1 = types.KeyboardButton("Получить гайд")
    item2 = types.KeyboardButton("Оферта")
    item3 = types.KeyboardButton("Поддержка")

    markup.add(item1, item2, item3)  # Добавляем кнопки на клавиатуру

    # Отправляем сообщение с кнопками
    bot.send_message(
        message.chat.id,
        "Привет! Добро пожаловать в бот!\n\n"
        "Этот бот научит тебя создавать и монетизировать AI-аватара с нуля!",
        reply_markup=markup
    )

# Обработчик кнопки "Получить гайд"
@bot.message_handler(func=lambda message: message.text == "Получить гайд")
def get_guide(message):
    text = (
        "«База для новичков» + создание ИИ-аватара\n\n"
        "Что внутри:\n"
        "• список актуальных нейросетей и сервисов — как ими пользоваться и где оплачивать\n"
        "• разбор агрегаторов, через которые удобно работать с нейросетями\n"
        "• пошаговое создание реалистичного ИИ-аватара с нуля\n"
        "• понимание, как превратить это в источник дохода и на каких площадках размещать контент\n\n"
        "Подойдёт даже если вы начинаете с полного нуля.\n\n"
        "Стоимость доступа — 690 ₽."
    )

    pay_markup = types.InlineKeyboardMarkup()
    pay_markup.add(
        types.InlineKeyboardButton(
            "Перейти к оплате",
            url="https://rbksa.ru/b/LlcAftUVbki0TAFRkTqREA"
        )
    )

    bot.send_message(message.chat.id, text, reply_markup=pay_markup)


# Обработчик кнопки "Оферта"
@bot.message_handler(func=lambda message: message.text == "Оферта")
def offer(message):
    bot.send_message(
    message.chat.id,
    "Договор оферты:\nhttps://docs.google.com/document/d/17eEBGv6G-LzUcZpyvygfLzJT-W_BloOs/preview"
)


# Обработчик кнопки "Поддержка"
@bot.message_handler(func=lambda message: message.text == "Поддержка")
def support(message):
    bot.send_message(
        message.chat.id,
        "Поддержка:\nMara102@mail.ru"
    )

import threading
from flask import Flask
import os

app = Flask(__name__)
from flask import request

import hashlib

PAID_INV_IDS = set()

@app.route("/robokassa/result", methods=["POST"])
def robokassa_result():

    out_sum = request.form.get("OutSum", "")
    inv_id = request.form.get("InvId", "")
    signature = request.form.get("SignatureValue", "").upper()

    password2 = os.environ.get("ROBOKASSA_PASSWORD2", "")

    check = hashlib.md5(f"{out_sum}:{inv_id}:{password2}".encode()).hexdigest().upper()

    if signature != check:
        return "bad sign", 400

    PAID_INV_IDS.add(inv_id)

    return f"OK{inv_id}", 200
@app.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Сначала поднимаем веб-сервер в отдельном потоке
threading.Thread(target=run_web, daemon=True).start()

# Потом запускаем бота (это блокирующий вызов)
bot.infinity_polling()






