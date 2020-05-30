import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)

def keyboard_main():
   # ����
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   item_profile = types.KeyboardButton('�������')
   item_shop = types.KeyboardButton('�������')
   markup.add(item_profile, item_shop)

   return markup


# �����
@bot.message_handler(commands=['/start'])
def start(message):
   bot.send_message(message.chat.id, '������, {name}, ��� "���������" �������, � ���� ��������� ���� ���� ������� �� '
                                     '�������, �� �� ������ �� ������ �������� ���� � ��������, �� � �������� �� � '
                                     '���\n�� ������ ������ ��������� /start_game'.format(
      name=message.from_user.first_name))


# ������
@bot.message_handler(commands=['/start_game'])
def start_game(message):
   bot.send_message(message.chat.id, '�� ����� � ��� ����������, ��� ������ ������, ���� ������� ������� ��� '
                                     '���������� �� ������.\n�� ������ ����������� ���� � ���� ���� � ����������� ��� '
                                     '����� � �����, �� ���� ���� �������, �� ������ �������� ���')
   bot.send_message(message.chat.id, '�������� ���� ��� /name [���]')


# �������� ����� � ������ ������� � ���� users.py
@bot.message_handler(commands=['/name'])
def set_name(message):
   name = message[0]

   f_read = open('users.py', 'r')
   users = eval(f.read())
   f_read.close()

   if name in users:
      bot.send_message(message.chat.id, '������������ � ����� ������ ��� ����, ���������� ��� ���')
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

      bot.send_message(user_id, '<�������� ������� ������>')
      bot.send_message(user_id, '��� �� � ��������� � ������ �����������. ������ �����������, � ����� ������ � �������', reply_markup=markup)

   else:
      bot.send_message(message.chat.id, '<������ �������� �����>')


# �������� ����� ----------------
@bot.message_handler(content_types=['text'])
def main_options(message):
   if message == '�������':
      user_id = message.chat.id

      f_read = open('users.py', 'r')
      name = f_read[user_id]['name']
      level = f_read[user_id]['level']
      money = f_read[user_id]['money']
      rep = f_read[user_id]['rep']

      bot.send_message(message.chat.id, '���: {name}\n'
                                        '�������: {level}\n'
                                        '������: {money}\n'
                                        '���������: {rep}')


bot.polling(none_stop=True)
