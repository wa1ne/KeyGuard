import telebot

markup = telebot.types.InlineKeyboardMarkup()
button1 = telebot.types.InlineKeyboardButton("⚙️ Настройки", callback_data='to_info')
button2 = telebot.types.InlineKeyboardButton("➕ Добавить пароль", callback_data='add_pass')
markup.row(button1, button2)
button3 = telebot.types.InlineKeyboardButton("📃 Все пароли", callback_data='pass_list')
button4 = telebot.types.InlineKeyboardButton("🕹️ Запросить пароль", callback_data='get_pass')
markup.row(button3, button4)

markupkeymenu = telebot.types.InlineKeyboardMarkup()
buttonaddkey = telebot.types.InlineKeyboardButton("➕ Добавить ключ", callback_data='add_key') #не работает если пароль уже добавлен
buttonremovekey = telebot.types.InlineKeyboardButton("➖ Удалить ключ", callback_data='remove_key')
buttoneditkey = telebot.types.InlineKeyboardButton("📝 Изменить ключ", callback_data='edit_key')
markupkeymenu.row(buttonaddkey, buttonremovekey)
markupkeymenu.row(buttoneditkey)

markupinfo = telebot.types.InlineKeyboardMarkup()
buttontoinfo = telebot.types.InlineKeyboardButton("📑 Инструкция", callback_data='to_info')
markupinfo.row(buttontoinfo)

markupback = telebot.types.InlineKeyboardMarkup()
buttonbacktomenu = telebot.types.InlineKeyboardButton("🔙 Назад", callback_data='to_menu')
markupback.row(buttonbacktomenu)

markupmenu = telebot.types.InlineKeyboardMarkup()
buttontomenu = telebot.types.InlineKeyboardButton("🎮 Меню", callback_data='to_menu')
markupmenu.row(buttontomenu)

markupbacklist = telebot.types.InlineKeyboardMarkup()
buttonremoveservice = telebot.types.InlineKeyboardButton("➖ Удалить сервис", callback_data='remove_service')
markupbacklist.row(buttonremoveservice, button4)
markupbacklist.row(buttonbacktomenu)

markupaddmenu = telebot.types.InlineKeyboardMarkup()
buttonbacktoadd = telebot.types.InlineKeyboardButton("🔙 Назад", callback_data='add_pass')
markupaddmenu.row(buttonbacktoadd)

markupaddmenu2 = telebot.types.InlineKeyboardMarkup()
buttonbacktoadd2 = telebot.types.InlineKeyboardButton("📝 Добавить", callback_data='add_pass')
markupaddmenu2.row(buttonbacktoadd2)

markupbacktoget = telebot.types.InlineKeyboardMarkup()
buttonbacktoget = telebot.types.InlineKeyboardButton("🔙 Назад", callback_data='get_pass')
markupbacktoget.row(buttonbacktoget)

markupbackandpass = telebot.types.InlineKeyboardMarkup()
buttontopass = telebot.types.InlineKeyboardButton("🔑 Настройка шифрования", callback_data='to_key')
markupbackandpass.row(buttontomenu)
markupbackandpass.row(buttontopass)

markuptokeymenu = telebot.types.InlineKeyboardMarkup()
buttontokeymenu = telebot.types.InlineKeyboardButton("🔙 Назад", callback_data='to_key')
markuptokeymenu.row(buttontokeymenu)

markupremovekey = telebot.types.InlineKeyboardMarkup()
buttonagreetoremovek = telebot.types.InlineKeyboardButton("✅ Подтвердить", callback_data='agree_to_remove_key')
markupremovekey.row(buttonagreetoremovek)

markupremoveservice = telebot.types.InlineKeyboardMarkup()
buttonagreetoremoves = telebot.types.InlineKeyboardButton("✅ Подтвердить", callback_data='agree_to_remove_service')
markupremoveservice.row(buttonagreetoremoves)