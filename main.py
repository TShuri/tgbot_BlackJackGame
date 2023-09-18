import random
import time
import telebot
import configure
from telebot import types

bot = telebot.TeleBot(configure.config['token'])

deck = None
points = None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_yes = types.KeyboardButton('Играем!')
    markup.add(btn_yes)
    bot.send_message(message.chat.id, 'Играем в игру "21-ОЧКО"?', reply_markup=markup)
    bot.register_next_step_handler(message, choise)

def choise(message):
    if (message.text.strip() == 'Играем!'):
        global deck, points
        deck = [2, 3, 4, 6, 7, 8, 9, 10, 11] * 4
        random.shuffle(deck)
        points = 0
        
        bot.send_message(message.chat.id, 'Правильно. Тогда начнем!👍')
        game(message)
    else:
        bot.send_message(message.chat.id, 'Офигел?😠', reply_markup=types.ReplyKeyboardMarkup())
    
def game(message):
    time.sleep(1)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_yes = types.KeyboardButton('Да')
    btn_no = types.KeyboardButton('Нет')
    markup.add(btn_yes, btn_no)
    bot.send_message(message.chat.id, 'Берете карту?🧐', reply_markup=markup)
    bot.register_next_step_handler(message, choiseCard)
    
def choiseCard(message):
    match (message.text.strip()):
        case 'Да':
            global points
            current = takeCard()
            points += current
            bot.send_message(message.chat.id, '♣️Попалась карта со значением: ' + str(current))
            time.sleep(1)
            if (points > 21):
                bot.send_message(message.chat.id, '🥴Очень жаль, Вы проиграли!🥴')
                return
            elif (points == 21):
                bot.send_message(message.chat.id, '🎉Поздравляю, Вы выиграли!🎉')
                return
            else:
                bot.send_message(message.chat.id, 'У вас: ' + str(points) + ' очков')
                game(message)
            
        case 'Нет':
            bot.send_message(message.chat.id, '♣️Игра окончена со счетом: ' + str(points))
            return
        case _:
            game(message)
            
def takeCard():
    return deck.pop()
    
bot.polling(non_stop=True)