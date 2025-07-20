import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from utils.parser import parse_hh
from utils.pdf_generator import create_beautiful_pdf

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Импорт данных
from config import TOKEN

# Глобальные данные
user_data = {}
tracked_resumes = {}  # {user_id: {resume_id: True}}

# Кнопки
def get_city_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏙 Москва", callback_data='city_1')],
        [InlineKeyboardButton("🌆 Санкт-Петербург", callback_data='city_2')],
        [InlineKeyboardButton("🏰 Казань", callback_data='city_3')],
        [InlineKeyboardButton("🌍 Другой", callback_data='city_other')]
    ])

def get_experience_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👶 Без опыта", callback_data='exp_0')],
        [InlineKeyboardButton("👷 От 1 года", callback_data='exp_1')],
        [InlineKeyboardButton("🛠 От 3 лет", callback_data='exp_3')],
        [InlineKeyboardButton("🏆 От 6 лет", callback_data='exp_6')]
    ])

def get_back_or_cancel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад", callback_data='action_back'),
         InlineKeyboardButton("🚫 Отмена", callback_data='action_cancel')]
    ])

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = {}
    await update.message.reply_text("👋 Привет! Я помогу найти резюме на hh.ru. Введите /search для начала.")
    await update.message.reply_text("⏳ Я также буду автоматически искать новые резюме каждые 30 минут.")

# Команда /search
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = {}
    await update.message.reply_text("🏙 Выберите город:", reply_markup=get_city_keyboard())

# Обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data.startswith('city_'):
        city = data.split('_')[1]
        user_data[user_id]['city'] = city
        await query.message.reply_text("🎂 Введите возраст от:")
        user_data[user_id]['awaiting'] = 'age_from'
        user_data[user_id]['step_history'] = ['city']

    elif data.startswith('exp_'):
        exp = data.split('_')[1]
        user_data[user_id]['experience'] = exp
        await query.message.reply_text("💰 Укажите минимальную зарплату (в рублях, например: 50000):")
        user_data[user_id]['awaiting'] = 'salary'
        user_data[user_id]['step_history'].append('experience')

    elif data == 'gender_m':
        user_data[user_id]['gender'] = '1'
        await query.message.reply_text("🔍 Введите ключевые слова (например, должность, навыки):")
        user_data[user_id]['awaiting'] = 'keyword'
        user_data[user_id]['step_history'].append('gender')

    elif data == 'gender_f':
        user_data[user_id]['gender'] = '2'
        await query.message.reply_text("🔍 Введите ключевые слова (например, должность, навыки):")
        user_data[user_id]['awaiting'] = 'keyword'
        user_data[user