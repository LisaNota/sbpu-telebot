import telebot
import requests

bot = telebot.TeleBot('token') # my token

bot.remove_webhook()

user_names = {}
START, CONTINUE, WEATHER_CITY, EXCHANGE_RATE, STOP = range(5)
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):

    if message.from_user.id not in user_names:
        bot.send_message(message.chat.id, 'Добро пожаловать! Как вас зовут?')
    else:
        bot.send_message(message.chat.id, f'Привет, {user_names[message.from_user.id]}! Как я могу вам помочь?')
    user_states[message.from_user.id] = START

@bot.message_handler(commands=['help'])
def help(message):
        bot.send_message(message.chat.id, f'Меня зовут ChatBot, я - Ваш персональный помощник. Вот мой функционал:'
                                          f'\n 1. Погода. Я могу рассказать о текущей температуре, и как она '
                                          f'ощущается. Для этого введите фразу "Расскажи о погоде"'
                                          f'\n 2. Курс валюты. Расскажите, какая валюта вас интересует, и я переведу '
                                          f'ее в рубли. Для этого введите фразу в формате "Курс валюты USD"')

@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id, 'Спасибо за работу. До свидания!')
    if message.from_user.id in user_names:
        del user_names[message.from_user.id]

@bot.message_handler(content_types=['text'])
def get_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if user_id not in user_names:
        user_names[user_id] = message.text
        bot.send_message(chat_id, f'Приятно познакомиться, {message.text}! Узнайте о моих возможностях с помощью '
                                  f'команды "/help".')
        user_states[user_id] = CONTINUE

    elif message.text.lower() == 'расскажи о погоде':
        bot.send_message(chat_id, f'Конечно, {user_names[user_id]}! Погода в каком городе Вас интересует? Введите'
                                  f' фразу в формате "Город Сочи"')
        user_states[user_id] = WEATHER_CITY

    elif message.text.lower().startswith('город'):
        if user_states[user_id] == WEATHER_CITY:
            city = message.text[6:].strip()
            if city:
                send_weather(chat_id, city)
                user_states[user_id] = CONTINUE
                bot.send_message(chat_id, 'Чем еще я могу Вам помочь?')
        else:
            bot.send_message(chat_id, 'Вы желаете узнать погоду в этом городе? Начните с фразы "Расскажи о погоде"')

    elif message.text.lower().startswith('курс валюты'):
        user_states[user_id] = EXCHANGE_RATE
        currency_code = message.text[12:].strip().upper()
        if currency_code:
            send_exchange_rate(chat_id, currency_code)
            user_states[user_id] = CONTINUE
            bot.send_message(chat_id, 'Чем еще я могу Вам помочь?')
        else:
            bot.send_message(chat_id, f'{user_names[user_id]}, Вы желаете узнать курс валюты? '
                                      f'Введите три буквы валюты, и я переведу их к рублю. Доступные валюты: '
                                      f'USD, EUR, GBP, CAD, PLN.')
    else:
        user_states[user_id] = CONTINUE
        bot.send_message(chat_id, f'Привет, {user_names[user_id]}! Как я могу вам помочь?')


def send_exchange_rate(chat_id, currency_code):
    api_key = 'token' # my token

    # Используем USD как базовую валюту, чтобы получить курсы для различных валют по отношению к USD
    url = f'https://www.freeforexapi.com/api/live?pairs=USDRUB,{currency_code}USD&apikey={api_key}'

    try:
        exchange_data = requests.get(url).json()

        rub_rate = exchange_data['rates']['USDRUB']['rate']
        if currency_code != 'USD':
            other_rate = exchange_data['rates'][f'{currency_code}USD']['rate']
        else:
            other_rate = 1

        rate = rub_rate / other_rate

        exchange_message = f'Курс {currency_code} к RUB сейчас: {rate}'
        bot.send_message(chat_id, exchange_message)
    except Exception as e:
        print(f'Error fetching exchange rate data: {e}')
        bot.send_message(chat_id, 'Не удалось получить данные о курсе валюты. Убедитесь, что название валюты'
                                  ' введено верно. Пример: USD, EUR, GBP, CAD, PLN.')


def send_weather(chat_id, city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={token}' # my token
    try:
        weather_data = requests.get(url).json()

        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])

        w_now = f'Сейчас в городе {city} {temperature} °C'
        w_feels = f'Ощущается как {temperature_feels} °C'

        bot.send_message(chat_id, w_now)
        bot.send_message(chat_id, w_feels)
    except Exception as e:
        print(f'Error fetching weather data: {e}')
        bot.send_message(chat_id, 'Не удалось получить данные о погоде. Убедитесь, что искомый город введен верно.')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
