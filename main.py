from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from asd import read_json, write_json

bot = TeleBot("6316221486:AAEY0x8QZUDmHgt0b797KreE4p6N6ybet1M")


locations = read_json("location.json")#локации
players = read_json()#игроки


@bot.message_handler(commands=['start'])
def start(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add(*['/помощь','/играть'])
    bot.send_message(message.from_user.id, "Привет, добро пожаловать в игру!", reply_markup=menu_keyboard)

@bot.message_handler(commands=['помощь', 'help'])
def help(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add(*['/играть'])
    bot.send_message(message.from_user.id, "Нажимай кнопочку, чтобы погрузиться в мир квестов", reply_markup=menu_keyboard)


@bot.message_handler(commands=['играть', 'play'])
def play(message):
    global players, locations
    p_id = str(message.from_user.id)
    if new_player(p_id):return
    send_info(p_id)

@bot.message_handler(func=lambda message : True)
def engine(message):
    global players, locations
    p_id = str(message.from_user.id)
    if new_player(p_id): return
    try:
        p_new_location = locations[players[p_id]['location']]['actions'][message.text]
        players[p_id]["location"] = p_new_location  #обновим позицию игрока
        write_json(players)
    except:
        bot.send_message(p_id, "Неверное действие")
    #отправка локации
    send_info(p_id)

#обновление информации об игроке
def new_player(p_id):
    global players
    if p_id not in players:
        players[p_id] = {"location": "start", "death": 0}
        write_json(players)
        send_info(p_id)
        return True
    return False



def send_info(p_id):
    global players, locations
    text = locations[players[p_id]['location']]['description']  # описание локации
    img = open(locations[players[p_id]['location']]['image'], "rb")  # картинка локации
    actions = list(locations[players[p_id]['location']]['actions'].keys())  # действия локации

    # действия на локации:
    menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add(*actions)  # звездочка распаковывает список

    # отправка сообщения:
    bot.send_photo(p_id, photo=img, caption=text, reply_markup=menu_keyboard)
    # bot.send_message(p_id, text, reply_markup=menu_keyboard)








bot.polling()