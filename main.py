import telebot
import os
import keyboard
import crypter
import database
TOKEN = '6937610129:AAHvGN2EhxHy0uzlNAPdUcl4OAtPb0L4A60'
bot = telebot.TeleBot(TOKEN)

cryptkeylib = {}

@bot.message_handler(commands=['start','help'])
def start_message(message):
  with open('icons/hello.png', 'rb') as hello:
    bot.send_photo(message.chat.id, hello, caption="""
*KeyGuard* \- удобный бот, позволяющий безопасно хранить ваши пароли\! 😼

🚨 Для начала пользования ботом прочитайте инструкцию, нажав по кнопке ниже\.
""", reply_markup=keyboard.markupinfo, parse_mode='MarkdownV2')

@bot.message_handler(commands=['menu'])
def menu(message):
  with open('icons/menu.png', 'rb') as menu:
    bot.send_photo(message.chat.id, menu, caption="""
🤖 *Выберите опцию:*
""", reply_markup=keyboard.markup, parse_mode='MarkdownV2')
  if message.from_user.is_bot == True:
    bot.delete_message(message.chat.id, message.message_id)

def info(message):
  bot.delete_message(message.chat.id,message.message_id)
  with open('icons/info.png', 'rb') as info:
    bot.send_photo(message.chat.id, info, caption="""
⚙️ *Инструкция по пользованию бота:*

 `1\.` Добавление пароля:
Чтобы добавить пароль в бота необходимо воспользоваться кнопкой: *"➕ Добавить пароль"* в меню\. После чего пароль должен вводиться в формате сервис:пароль, по сервису будет проводиться поиск вашего пароля\.
                   
🚨 Для дополнительной защиты ваших паролей вы можете воспользоваться кнопкой: *"🔑 Настройка шифрования"* ниже под этим сообщением\. Эта функция будет шифровать ваши пароли с ключом для большей безопасности\.
                   
 `2\.` Получение пароля:
Чтобы получить пароль от необходимого вам сервиса, уже добавленного вами в бота воспользуйтесь кнопкой: *"🕹️ Запросить пароль"* в меню\. Введите интересующий вас сервис и бот ответит вам сообщением с паролем\.
                   
 `3\.` Получение всех подключенных сервисов:
Для удобства понимания имеющихся в базе бота паролей воспользуйтесь кнопкой: *"📃 Все пароли"* в меню\. Бот отправит вам список подключенных вами сервисов\.
                   
😊 Приятного пользования\!
""", reply_markup=keyboard.markupbackandpass, parse_mode='MarkdownV2')


def add_pass(message):
  with open('icons/add.png', 'rb') as add:
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_photo(message.chat.id, add, caption="""
📝 Введите данные в формате `service:password`
""", reply_markup=keyboard.markupback)
    bot.register_next_step_handler(message, handle_password_entry)

def handle_password_entry(message):
  try:
    service, password = message.text.split(':', 1)
    if message.from_user.id in cryptkeylib:
      hashed_key = cryptkeylib[message.from_user.id]
      encryptedpassword, tag = crypter.encrypt(password, hashed_key)
      database.add_password(message.from_user.id, service, encryptedpassword, tag)
    else:
      database.add_password_notag(message.from_user.id, service, password)
    bot.send_message(message.chat.id, "✅ Пароль успешно добавлен!")
  except ValueError:
    bot.send_message(message.chat.id, "❗ Неверный формат\. Используйте формат `service:password`\.", reply_markup=keyboard.markupmenu, parse_mode='MarkdownV2')
  except Exception as e:
    bot.send_message(message.chat.id, f"❗ Произошла ошибка: {str(e)}", reply_markup=keyboard.markupmenu)

def pass_list(message, userid):
  bot.delete_message(message.chat.id, message.message_id)
  services_string = database.get_list_of_services(userid)
  if services_string != '':
    with open('icons/list.png', 'rb') as list:
      bot.send_photo(message.chat.id, list, caption=f"""
  📄 Список ваших сервисов:\n<pre><code>{services_string}</code></pre>
  """, reply_markup=keyboard.markupbacklist, parse_mode='HTML')
  else:
    bot.send_message(message.chat.id, '❗ Пароли отсутствуют!', reply_markup=keyboard.markupmenu)

def remove_service_message(message):
  bot.delete_message(message.chat.id, message.message_id)
  bot.send_message(message.chat.id, "✏️ Введите название сервиса, который хотите удалить", reply_markup=keyboard.markupmenu)
  bot.register_next_step_handler(message, remove_service_agree)

def remove_service_agree(message):
  bot.delete_message(message.chat.id, message.message_id-1)
  bot.send_message(message.chat.id, f"🧐 Вы уверены, что хотите удалить `{message.text}`?\n Подтвердите действие кнопкой ниже\.", reply_markup=keyboard.markupremoveservice, parse_mode='MarkdownV2')

def get_password(message):
  bot.delete_message(message.chat.id, message.message_id)
  with open('icons/get.png', 'rb') as get:
    bot.send_photo(message.chat.id, get, caption="""
📄 Введите необходимый сервис или ключ по которому вы добавляли необходимый пароль
""", reply_markup=keyboard.markupback, parse_mode='MarkdownV2')
    bot.register_next_step_handler(message, handle_password_get)

def handle_password_get(message):
  try:
    password = database.get_password(message.from_user.id, message.text)
    if len(password) != 0:
      pass_text = password[0]
      if message.from_user.id in cryptkeylib:
        hashed_key = cryptkeylib[message.from_user.id]
        decryptedpassword = crypter.decrypt(pass_text[0], hashed_key, pass_text[1])
        bot.send_message(message.chat.id, f'🔐 Ваш пароль: ```{decryptedpassword}```', parse_mode='MarkdownV2')
      else:
        bot.send_message(message.chat.id, f'🔐 Ваш пароль: ```{pass_text[0]}```', parse_mode='MarkdownV2')
    else:
      bot.send_message(message.chat.id, f'❗ Пароль не найден', reply_markup=keyboard.markupmenu, parse_mode='MarkdownV2')
  except Exception as e:
    bot.send_message(message.chat.id, f"❗ Произошла ошибка: {str(e)}", reply_markup=keyboard.markupmenu)

def key_menu(message, user_id):
  bot.delete_message(message.chat.id,message.message_id)
  if user_id in cryptkeylib:
    with open('icons/crypt.png', 'rb') as crypt:
      bot.send_photo(message.chat.id, crypt, caption=f"""
🙈 <b>Настройка шифрования паролей</b>
Данная функция не обязательна, но она поможет добавить дополнительную защиту вашим паролям.
> Ключ шифрования: <b>{cryptkeylib[user_id]}</b>
  """, reply_markup=keyboard.markupkeymenu, parse_mode='HTML')
  else:
    with open('icons/crypt.png', 'rb') as crypt:
      bot.send_photo(message.chat.id, crypt, caption=f"""
🙈 <b>Настройка шифрования паролей</b>
Данная функция не обязательна, но она поможет добавить дополнительную защиту вашим паролям.
> Ключ шифрования: <b>Отсутствует</b>
  """, reply_markup=keyboard.markupkeymenu, parse_mode='HTML')

def add_key(message):
  bot.delete_message(message.chat.id,message.message_id)
  bot.send_message(message.chat.id, "✏️ Введите ключ шифрования", reply_markup=keyboard.markuptokeymenu)
  bot.register_next_step_handler(message, handle_add_key)

def handle_add_key(message):
  try:
    encryptedkey = crypter.hash_key(message.text)
    cryptkeylib[message.from_user.id] = encryptedkey
    bot.send_message(message.chat.id, '✅ Ключ установлен!', reply_markup=keyboard.markupmenu)
    bot.delete_message(message.chat.id, message.message_id-1)
  except Exception as e:
    bot.send_message(message.chat.id, f"❗ Произошла ошибка: {str(e)}", reply_markup=keyboard.markuptokeymenu)

def remove_key_message(message):
  bot.send_message(message.chat.id, "🧐 Вы уверены, что хотите удалить ключ шифрования?\n Подтвердите действие кнопкой ниже.", reply_markup=keyboard.markupremovekey)
  bot.delete_message(message.chat.id, message.message_id)

def remove_key(user_id):
  del cryptkeylib[user_id]

def edit_key(message):
  bot.send_message(message.chat.id, "✏️ Введите ключ шифрования", reply_markup=keyboard.markuptokeymenu)
  bot.register_next_step_handler(message, handle_add_key)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
  data = call.data
  userid = call.from_user.id
  if data == 'to_menu':
    menu(call.message)
  elif data == 'to_info':
    info(call.message)
  elif data == 'add_pass':
    add_pass(call.message)
  elif data == 'pass_list':
    pass_list(call.message, userid)
  elif data == 'get_pass':
    get_password(call.message)
  elif data == 'to_key':
    key_menu(call.message, userid)
  elif data == 'add_key':
    add_key(call.message)
  elif data == 'remove_key':
    if userid in cryptkeylib:
      remove_key_message(call.message)
    else:
      bot.delete_message(call.message.chat.id, call.message.message_id)
      bot.send_message(call.message.chat.id, '❗ Ключ шифрования отсутствует!', reply_markup=keyboard.markupmenu)
  elif data == 'remove_service':
    remove_service_message(call.message)
  elif data == 'agree_to_remove_key':
    remove_key(call.message, userid)
    bot.send_message(call.message.chat.id, '✅ Ключ шифрования удален!', reply_markup=keyboard.markupmenu)
    bot.delete_message(call.message.chat.id, call.message.message_id)
  elif data == 'agree_to_remove_service':
    text = call.message.text[33:]
    ind = text.find('\n')
    text = text[:ind-1]
    database.remove_service(userid, text)
    bot.send_message(call.message.chat.id, '✅ Сервис удален!', reply_markup=keyboard.markupmenu)
    bot.delete_message(call.message.chat.id, call.message.message_id)
  elif data == 'edit_key':
    edit_key(call.message)

database.open_connection()
bot.polling()