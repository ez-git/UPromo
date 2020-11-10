import telebot
import psycopg2
import datetime

token = '1413165223:AAE-GnZ6hYLVhsaWtxTCdyQ-OSYoeg4raPk'

UBot = telebot.TeleBot(token)

ans_list = []
mark = '\U000027A1 '


@UBot.message_handler(commands=['start'])
def start_message(message):
    q_type(message)


@UBot.message_handler(content_types=['text'])
def greetings(message):
    q_type(message, 'greetings')


@UBot.callback_query_handler(func=lambda call: True)
def callback_processor(call):
    if call.data in ['promos', 'raffles', 'all']:
        ans_list.append(call.data)
        q_date(call)
    elif call.data in ['today', '3days', 'week', 'month']:
        ans_list.append(call.data)
        post_offers(call)
    elif call.data == 'again':
        q_type(call.message, 'again')


def q_date(call):
    markup = init_markup()
    markup.add(telebot.types.InlineKeyboardButton(text='Сегодня', callback_data='today'))
    markup.add(telebot.types.InlineKeyboardButton(text='3 дня', callback_data='3days'))
    markup.add(telebot.types.InlineKeyboardButton(text='Неделя', callback_data='week'))
    markup.add(telebot.types.InlineKeyboardButton(text='Месяц', callback_data='month'))
    UBot.send_message(call.message.chat.id, text=mark + "За какой период?", reply_markup=markup)


def send_msg(message, text):
    UBot.send_message(message.chat.id, text)


def q_type(message, help_command=''):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Промокоды', callback_data='promos'))
    markup.add(telebot.types.InlineKeyboardButton(text='Розыгрыши', callback_data='raffles'))
    markup.add(telebot.types.InlineKeyboardButton(text='Промокоды и розыгрыши', callback_data='all'))

    if help_command == 'again':
        UBot.send_message(message.chat.id, text=mark + 'Давай по новой, ' + message.chat.first_name + ', всё не то!',
                          reply_markup=markup)
    elif help_command == 'greetings':
        UBot.send_message(message.chat.id, text=mark + 'Уже виделись, уведомления выключены? Что хочешь?',
                          reply_markup=markup)
    else:
        UBot.send_message(message.chat.id, text=mark +
"""Привет! Отключи уведомления! 
Переходи и подписывайся на @UPromoOnline!
Зачем ты здесь?""", reply_markup=markup)


def post_offers(call):
    texts = get_offers()
    for text in texts:
        send_msg(call.message, text)
    # text = mark + 'Только сегодня, только сейчас и всегда по жизни ничего ты не получишь =('

    markup = init_markup()
    markup.add(telebot.types.InlineKeyboardButton(text='Посмотреть ещё', callback_data='again'))
    UBot.send_message(call.message.chat.id, text=mark + 'Ещё?', reply_markup=markup)


def get_offers():
    con = psycopg2.connect(
        database='upromo_main',
        user="postgres",
        password="Zxcvbnm0+",
        host="127.0.0.1",
        port="5432"
    )

    cur = con.cursor()

    cur_date = datetime.datetime.now()
    result_date = cur_date - datetime.timedelta(weeks=1)
    select_date = datetime.date(result_date.year, result_date.month, result_date.day)
    query = """SELECT PROMO,
                RELEASE_DATE 
                FROM PROMOS
                WHERE RELEASE_DATE >= '{0}' 
                ORDER BY RELEASE_DATE DESC; """.format(select_date)
    cur.execute(query)

    rows = cur.fetchall()
    texts = []
    for row in rows:
        texts.append('    ПРОМОКОД от ' + row[1].strftime("%d.%m") + """
        """ + row[0])

    return texts  # text[:len(text) - 2]


def init_markup():
    return telebot.types.InlineKeyboardMarkup()


if __name__ == '__main__':
    UBot.polling(none_stop=True, interval=0)
