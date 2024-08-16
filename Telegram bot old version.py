import telebot

lst = []

token = 'токен бота'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Привет, Я телеграмм бот группы Fizfuck.Confessions, чтобы узнать больше напиши команду /help')


@bot.message_handler(commands=['help'])
def description(message):
    bot.send_message(message.chat.id,
                     'Чтобы опубликовать запись напиши команду /publish и в ЭТОМ же сообщении текст публикации \n'
                     '\nOбращаю внимание, что команду и текст публикации необходимо присылать в ОДНОМ сообщении. \n'
                     '\nЕсли хочешь узнать больше о группе напиши команду /more \n'
                     '\n Напиши команду /example, чтобы посмотреть пример публикации\n'
                     '\n Если хочешь опубликовать фото и текст к нему, просто пришли боту фото и текст публикации в ТОМ ЖЕ сообщении, что и фото')


@bot.message_handler(commands=['example'])
def example(message):
    bot.send_message(message.chat.id,
                     '/publish  \nЭто пример публикации, все, что написано после команды, будет опубликовано на канале\n'
                     'Гарантия, того, что бот записал ваш пост ответное сообщение "Отправлено на публикацию"')


@bot.message_handler(commands=['more'])
def description(message):
    bot.send_message(message.chat.id, 'ссылка на канал: https://t.me/ff_conf \n'
                                      'ссылка на беседу: https://t.me/ff_conf_chat \n'
                                      'ссылка на бота: https://t.me/APDXnBot')


def editor(x):
    return ''.join(x.split('/publish'))


@bot.message_handler(commands=['publish'])
def publish(message):
    global lst
    global i
    lst.append('#' + str(i) + '\n' + editor(message.text) + 2 * '\n')
    bot.send_message(message.chat.id, 'Отправлено на публикацию')
    with open("testFile.txt", "a") as file:
        file.writelines(lst)
    i += 1
    lst = []


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        if message.caption != None:
            photo = message.photo[-1]
            file_info = bot.get_file(photo.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            save_path = 'Photo_posts\\' + '#' + str(i) + '   ' + '_'.join(message.caption.split('\n')) + '.jpg'
            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, 'Фотография и текст к ней сохранены.')
        else:
            photo = message.photo[-1]
            file_info = bot.get_file(photo.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            save_path = 'Photo_posts\\' + '#' + str(i) + '   ' + 'photo.jpg'
            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, 'Фотография сохранена.')
    except Exception as e:
        bot.reply_to(message, 'Ошибка, попробуйте снова')


# time.sleep(30)

# bot.polling(non_stop=True)

if __name__ == '__main__':
    bot.polling(none_stop=True)
