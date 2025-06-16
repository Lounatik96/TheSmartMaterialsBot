import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен из переменной окружения или напрямую
TOKEN = "7287080732:AAHTUgSL5Lkhv8pe0F0PWL9MWc_Ec8RssnI"  # ← обновлённый токен

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ℹ️ Информация о командировке", callback_data='info')],
        [InlineKeyboardButton("📂 Получить шаблоны документов", callback_data='templates')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Я SmartMaterialsBot. Чем могу помочь?', reply_markup=reply_markup)

# Обработчик нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'templates':
        try:
            with open('templates/Заявка.docm', 'rb') as file:
                await query.message.reply_document(document=file, filename='Заявка.docm')
            with open('templates/Авансовый_отчет.xlsx', 'rb') as file:
                await query.message.reply_document(document=file, filename='Авансовый_отчет.xlsx')
            with open('templates/Научный_отчет.docx', 'rb') as file:
                await query.message.reply_document(document=file, filename='Научный_отчет.docx')
            with open('templates/Заявление.docx', 'rb') as file:
                await query.message.reply_document(document=file, filename='Заявление.docx')
        except Exception as e:
            await query.message.reply_text(f"Ошибка при отправке файлов: {e}")

    elif query.data == 'info':
        info_text = """
        Для оформления командировки необходимо подготовить служебную записку с информацией о поездке и точной сметой.

        Служебная записка согласовывается:
        • Научным руководителем (руководителем научной группы)
        • Руководителем проекта
        • Карташова М.С. (каб. 201)

        После согласования передается Колесниченко С.В. (каб. 205):
        • По России – за 7 рабочих дней до начала поездки
        • Зарубежом – за 5 недель до начала поездки

        Подробности уточняйте у ответственных лиц.
        """
        await query.edit_message_text(text=info_text)

# Основная функция запуска бота
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()