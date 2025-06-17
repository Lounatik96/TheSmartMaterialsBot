import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
TOKEN = "7668699787:AAHEL3Nhfmhy9GJwGyZVSUdRP4bKqUUIxCM"  # Новый токен

# Структурированная информация
INFO_TEXT = {
    'main': """
    <b>Добро пожаловать в TheSmartMaterialsBot</b>

    Я помогу вам подготовиться к командировке. Ниже вы найдете важную информацию по оформлению документов.

    <u>Основные разделы:</u>
    • /start – начать работу
    • /info – информация о командировке
    • /templates – получить шаблоны документов

    Для получения информации выберите один из разделов ниже.
    """,
    
    'info': """
    <b>1. Подготовка служебной записки</b>
    
    Для оформления командировки необходимо подготовить служебную записку с указанием информации о поездке и точной сметы.
    
    <b>Кто должен согласовать?</b>
    • Научный руководитель (руководитель научной группы)  
    • Руководитель проекта  
    • Карташова М.С., каб. 201
    
    <b>Куда передавать?</b>
    Колесниченко С.В., каб. 205:
    • По России – за 7 рабочих дней до начала поездки
    • Зарубежом – за 5 недель до начала поездки
    
    <b>Важно:</b>
    • Документы принимаются только при наличии всех подписей
    • Нарушение сроков предоставления информации → командировка не оформляется
    • Цель командировки должна соответствовать целям проекта
    • Даты должны совпадать с билетами
    • Командировка не может совпадать с отпуском
    """,

    'project_2030': """
    <b>2. Приоритет-2030: дополнительное требование</b>
    
    При оформлении командировки в рамках проектов Приоритет-2030 дополнительно подготовьте:
    • Служебная записка на имя и.о. проректора по стратегическому развитию и исследовательской деятельности
    • Обоснование целесообразности командировки в рамках проекта
    """,

    'travel': """
    <b>3. Проезд</b>
    
    В заявке на командирование указывается тип транспорта:
    • ЖД (плацкарт, купе, сидячий)
    • Авиа (эконом-класс)
    
    <b>Не возмещаются:</b>
    • Выбор места в поезде
    • Билеты бизнес/первый класс
    • Сервисный сбор сторонних сервисов
    • Питание и прочие дополнительные услуги
    """,

    'accommodation': """
    <b>4. Проживание</b>
    
    Укажите в заявке:
    • Тип размещения (отель, гостиница, апартаменты, хостел, общежитие)
    • Категория номера (одноместный стандарт или эконом)
    • Не более 4 звёзд у гостиницы
    
    <b>Для закрытия авансового отчета:</b>
    • Гостиница: кассовый чек, акт оказания услуг, копия бронирования
    • Квартира: договор аренды, акт оказания услуг, кассовый чек
    • Через «Островок»: копия бронирования + ваучер
    
    <b>Важно:</b>
    • Все организации должны быть легальными и выдавать QR-чеки
    • При оплате одним человеком за группу – нужна расписка остальных
    • Договор аренды должен содержать паспортные данные всех проживающих
    """,

    'daily_allowance': """
    <b>5. Суточные</b>
    
    • По России: 700 руб./сутки
    • Зарубежом: 2500 руб./сутки
    
    <b>Примечание:</b>
    При зарубежной командировке суточные за дни в пути по России также выплачиваются по 700 ₽/день.
    """,

    'conference': """
    <b>6. Участие в конференции</b>
    
    Дополнительно необходимо предоставить:
    • Копия экспертного заключения о возможности открытого опубликования (обращаться к Цицуашвили В.С., каб. 204)
    • Договор и акт об оказании услуг
    • Копия сертификата/диплома/тезисов или иное подтверждение участия
    """,

    'insurance': """
    <b>7. Страховка</b>
    
    При оформлении зарубежной командировки:
    • Договор и акт об оказании услуг
    • Кассовый чек с назначением платежа (оригиналы)
    
    <b>Важно:</b>
    Если страховка оформлена на период больше командировки, оплата производится пропорционально дням поездки.
    """,

    'visa': """
    <b>8. Визовые расходы</b>
    
    Возмещаются при наличии:
    • Договор
    • Акт об оказании услуг
    • Кассовый чек с назначением платежа (оригиналы)
    
    <b>Внимание:</b>
    Без полного пакета документов — расходы не возмещаются.
    """,

    'contact': """
    <b>9. Контакты</b>
    
    За дополнительной информацией обращайтесь к:
    <b>Колесниченко С.В.</b>, каб. 205  
    📞 +7 929 820 68 58  
    📧 skole@sfedu.ru
    """
}

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ℹ️ Общая информация", callback_data='info')],
        [InlineKeyboardButton("🌍 Приоритет-2030", callback_data='project_2030')],
        [InlineKeyboardButton("🚆 Проезд", callback_data='travel')],
        [InlineKeyboardButton("🏨 Проживание", callback_data='accommodation')],
        [InlineKeyboardButton("💶 Суточные", callback_data='daily_allowance')],
        [InlineKeyboardButton("📝 Конференция", callback_data='conference')],
        [InlineKeyboardButton("🧾 Страховка", callback_data='insurance')],
        [InlineKeyboardButton("🛂 Виза", callback_data='visa')],
        [InlineKeyboardButton("📄 Получить шаблоны документов", callback_data='templates')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(INFO_TEXT['main'], parse_mode='HTML', reply_markup=reply_markup)

# Обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == 'templates':
        try:
            with open('templates/Заявка.docm', 'rb') as file:
                await query.message.reply_document(document=file, filename='Заявка.docm')
            with open('templates/Авансовый_отчет.xlsx', 'rb') как file:
                await query.message.reply_document(document=file, filename='Авансовый_отчет.xlsx')
            with open('templates/Научный_отчет.docx', 'rb') как file:
                await query.message.reply_document(document=file, filename='Научный_отчет.docx')
            with open('templates/Заявление.docx', 'rb') как file:
                await query.message.reply_document(document=file, filename='Заявление.docx')
        except Exception как e:
            await query.message.reply_text(f"Ошибка при отправке файлов: {e}")

    elif data == 'back_to_menu':
        await back_to_menu(update, context)

    else:
        text = INFO_TEXT.get(data, "Раздел временно недоступен.")
        await query.edit_message_text(text=text, parse_mode='HTML')

        # Кнопка "Назад"
        back_button = [[InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]]
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(back_button))

# Функция возврата в главное меню
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Восстанавливаем главное меню
    keyboard = [
        [InlineKeyboardButton("ℹ️ Общая информация", callback_data='info')],
        [InlineKeyboardButton("🌍 Приоритет-2030", callback_data='project_2030')],
        [InlineKeyboardButton("🚆 Проезд", callback_data='travel')],
        [InlineKeyboardButton("Hotéis Проживание", callback_data='accommodation')],
        [InlineKeyboardButton("💶 Суточные", callback_data='daily_allowance')],
        [InlineKeyboardButton("📝 Конференция", callback_data='conference')],
        [InlineKeyboardButton("🧾 Страховка", callback_data='insurance')],
        [InlineKeyboardButton("🛂 Виза", callback_data='visa')],
        [InlineKeyboardButton("📄 Шаблоны документов", callback_data='templates')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=INFO_TEXT['main'], parse_mode='HTML')
    await query.edit_message_reply_markup(reply_markup=reply_markup)

# Обработчик ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} вызвал ошибку {context.error}")
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text("Произошла ошибка. Пожалуйста, попробуйте снова.")
        except Exception как send_error:
            logging.error(f"Не удалось отправить сообщение об ошибке: {send_error}")

# Основная функция запуска бота
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()