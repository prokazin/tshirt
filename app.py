import os
from flask import Flask, request
import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont
import io
import logging

# Настройка приложения
app = Flask(__name__)
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Пути к ресурсам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
FONTS_DIR = os.path.join(BASE_DIR, 'fonts')

# Проверка существования директорий
if not os.path.exists(TEMPLATES_DIR):
    os.makedirs(TEMPLATES_DIR)
if not os.path.exists(FONTS_DIR):
    os.makedirs(FONTS_DIR)

# Данные пользователей
user_data = {}

def color_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add(
        types.KeyboardButton("⚪ Белый"),
        types.KeyboardButton("⚫ Черный"),
        types.KeyboardButton("🔴 Красный")
    )
    return markup

def font_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add(
        types.KeyboardButton("Arial"),
        types.KeyboardButton("Comic Sans"),
        types.KeyboardButton("Times New Roman")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(
            message.chat.id,
            "👕 Привет! Я создам футболку с твоим текстом.\n➡️ Сначала выбери цвет футболки:",
            reply_markup=color_keyboard()
        )
    except Exception as e:
        logger.error(f"Start error: {e}")

# Остальные обработчики остаются такими же, как у вас
# ...

@app.route('/', methods=['GET'])
def index():
    return "Футболко-бот работает!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return "ok", 200
    return "bad request", 400

if __name__ == '__main__':
    app.run(debug=True)
