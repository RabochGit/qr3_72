import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6664572328:AAGrL7GhOmmqmH-Psr-DDtRgFcLxgJqx8Oc",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "опрос"  # Можно менять текст
text_button_1 = "заполнить анкету"  # Можно менять текст
text_button_2 = "основные техники"  # Можно менять текст



menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я помогу тебе распределить твое свободное время. Но для начала заполни анкету о себе!',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, '*Твое* _имя_?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, '[]Сколько времени ты в среднем тратишь на выполнение домашки?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за регистрацию!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Сколько времени ты обычно тратишь на сочиения", reply_markup=menu_keyboard)  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "6664572328:AAGrL7GhOmmqmH-Psr-DDtRgFcLxgJqx8Oc", reply_markup=menu_keyboard)  # Можно менять текст




bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()