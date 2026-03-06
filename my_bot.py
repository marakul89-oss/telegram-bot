import telebot
from telebot import types
import os
import hashlib
import time
import threading
from flask import Flask, request

app = Flask(__name__)

PAID_INV_IDS = set()
PENDING_INV_BY_CHAT = {}  # chat_id -> inv_id

# Вставь сюда свой API токен, который дал BotFather
bot = telebot.TeleBot('8311827359:AAHViPd8fAk0hRMVmmHJNtro4VxhlmHf2_4')

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("Получить гайд")
    item2 = types.KeyboardButton("Оферта")
    item3 = types.KeyboardButton("Поддержка")
    markup.add(item1, item2, item3)

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
    chat_id = message.chat.id

    merchant_login = os.environ.get("MERCHANT_LOGIN", "")
    password1 = os.environ.get("ROBOKASSA_PASSWORD1", "")

    out_sum = "690"
    inv_id = str(int(time.time()))

    PENDING_INV_BY_CHAT[chat_id] = inv_id

    desc = "Гайд (доступ)"

    signature = hashlib.md5(
        f"{merchant_login}:{out_sum}:{inv_id}:{password1}".encode()
    ).hexdigest()

    pay_url = (
        "https://auth.robokassa.ru/Merchant/Index.aspx"
        f"?MerchantLogin={merchant_login}"
        f"&OutSum={out_sum}"
        f"&InvId={inv_id}"
        f"&Description={desc}"
        f"&SignatureValue={signature}"
    )

    pay_markup = types.InlineKeyboardMarkup()
    pay_markup.add(
        types.InlineKeyboardButton("Перейти к оплате", url=pay_url)
    )
    pay_markup.add(
        types.InlineKeyboardButton("Я оплатил", callback_data="check_payment")
    )
    pay_markup.add(
        types.InlineKeyboardButton("Не пришла ссылка / Поддержка", callback_data="support_payment")
    )

    bot.send_message(message.chat.id, text, reply_markup=pay_markup)


@bot.callback_query_handler(func=lambda call: call.data == "check_payment")
def check_payment(call):
    chat_id = call.message.chat.id
    inv_id = PENDING_INV_BY_CHAT.get(chat_id)

    if inv_id and inv_id in PAID_INV_IDS:
        bot.send_message(
            chat_id,
            "✅ Оплата найдена!\n\nВот ваш гайд:\nhttps://drive.google.com/file/d/guide"
        )
    else:
        bot.send_message(
            chat_id,
            "❌ Оплата пока не найдена.\n\nЕсли вы только что оплатили — подождите 10–20 секунд и нажмите кнопку снова."
        )


@bot.callback_query_handler(func=lambda call: call.data == "support_payment")
def support_payment(call):
    bot.send_message(
        call.message.chat.id,
        "Если вы оплатили, но ссылка не пришла:\n\n"
        "1. Подождите 30–60 секунд и нажмите «Я оплатил» ещё раз.\n"
        "2. Если ссылка не появилась — напишите в поддержку.\n\n"
        "Поддержка: @MarK_K13"
    )


@bot.message_handler(func=lambda message: message.text == "Оферта")
def offer(message):
    bot.send_message(
        message.chat.id,
        "Договор оферты:\nhttps://docs.google.com/document/d/17eEBGv6G-LzUcZpyvygfLzJT-W_BloOs/preview"
    )


@bot.message_handler(func=lambda message: message.text == "Поддержка")
def support(message):
    bot.send_message(
        message.chat.id,
        "Поддержка:\nMara102@mail.ru"
    )


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


threading.Thread(target=run_web, daemon=True).start()
bot.infinity_polling()
