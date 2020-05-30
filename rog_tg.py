import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)

def keyboard_main():
   # Меню
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   item_profile = types.KeyboardButton('Профиль')
   item_shop = types.KeyboardButton('Магазин')
   markup.add(item_profile, item_shop)

   return markup


# Старт
@bot.message_handler(commands=['/start'])
def start(message):
   bot.send_message(message.chat.id, 'Привет, {name}, это "хакерский" рогалик, в этой вселенной если тебя поймают за '
                                     'взломом, то ты можешь не только потерять вещи и рессурсы, но и остаться ни с '
                                     'чем\nТы можешь начать коммандой /start_game'.format(
      name=message.from_user.first_name))


# Начало
@bot.message_handler(commands=['/start_game'])
def start_game(message):
   bot.send_message(message.chat.id, 'Ты попал в мир информации, тут правят хакеры, люди готовые украсть эту '
                                     'информацию за деньги.\nТы можешь попробывать себя в этом деле и становиться все '
                                     'лучше и лучше, но если тебя поймают, ты можешь потерять все')
   bot.send_message(message.chat.id, 'Придумай себе имя /name [имя]')


# Создание имени и запись профиля в файл users.py
@bot.message_handler(commands=['/name'])
def set_name(message):
   name = message[0]

   f_read = open('users.py', 'r')
   users = eval(f.read())
   f_read.close()

   if name in users:
      bot.send_message(message.chat.id, 'Пользователь с таким именем уже есть, попробуйте еще раз')
   elif name not in users:
      user_id = message.chat.id
      dic_new_user = {user_id: {'name': name, 'level': 0, 'rep': 0, 'money': 500}}

      f_read = open('users.py', 'r')
      var_users = eval(f.read())
      f_read.close()

      dic_all_users = {**var_users, **dic_new_user}

      f_write = open('users.py', 'w')
      f_write.write(str(dic_all_users))
      f_write.colse()

      markup = keyboard_main()

      bot.send_message(user_id, '<Персонаж успешно создан>')
      bot.send_message(user_id, 'Вот вы и появились в городе небоскребов. Можешь осмотреться, а потом заходи в магазин', reply_markup=markup)

   else:
      bot.send_message(message.chat.id, '<Ошибка создания имени>')


# Основные опции ----------------
@bot.message_handler(content_types=['text'])
def main_options(message):
   if message == 'Профиль':
      user_id = message.chat.id

      f_read = open('users.py', 'r')
      name = f_read[user_id]['name']
      level = f_read[user_id]['level']
      money = f_read[user_id]['money']
      rep = f_read[user_id]['rep']

      bot.send_message(message.chat.id, 'Имя: {name}\n'
                                        'Уровень: {level}\n'
                                        'Деньги: {money}\n'
                                        'Репутация: {rep}')


bot.polling(none_stop=True)
