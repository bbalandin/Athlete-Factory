from telegram.ext import Updater, MessageHandler, Filters
from random import choice
import sqlite3 as sql

TOKEN = '5170550841:AAEPhHnLGtl03_QU7plUI3f6HfVkesshEGU'
sender = ''


def db_get(_select, _from, _where=True, _param=0):
    db = sql.connect("AF.db")
    res = list(db.execute(f"SELECT {_select} FROM {_from} WHERE {_where}").fetchall())
    res2 = [res[i][_param] for i in range(len(res))]
    print(f'selected {_select} from {_from} where {_where}')
    print(res2)
    return res2


def get_anthropometry(sender):
    answer = 'Пустая антропометрия!'
    res = db_get("height",
                 "anthropometry",
                 _where=f"user_id == (SELECT id FROM users WHERE id_telegram == '{sender}')")
    if not res: return answer
    answer = f'дата: {res[5]}'
    return answer


answers = {
    '/help': ['Помощь по работе с ботом:\n/am - ваша антропометрия'],
    '/start': [f'Приветствую вас!\nЯ буду помогать вам тренероваться\n/help для подробностей'],
    '/am': [get_anthropometry(sender)],
    '/confirm:': ['функция не работает'],
    '/reset:': ['функция не работает']
}


def for_text(update, context):
    global sender
    sender = update.message["chat"]["username"]
    text = update.message.text.lower()
    answer = 'Вроизошла ошибка!'
    print('-' * 20)
    if sender in db_get("id_telegram", "users"):
        print(f'user {sender} was found in db')
        if text in answers.keys():
            print('building answer...')
            # собираем ответ, если нами учтен вопрос
            answer = choice(answers[text])
        if answer:
            print('sending answer...')
            # отсылаем ответ, если он собран и юзер пользуется telegram
            update.message.reply_text(answer)
            print('-' * 20)
    else:
        if not sender:
            update.message.reply_text("Укажите свое имя пользователя в настройках Telegram\n\n"
                                      "Для регистрации на сайте: link")
        else:
            update.message.reply_text("Что-то пошло не так!\n"
                                      "Вы указали верное имя пользователя Telegram?\n\n"
                                      f"Ваше имя пользователя: {sender}\n\n"
                                      "А если вы еще не зарегистрировались, самое время это сделать: link")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, for_text)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()