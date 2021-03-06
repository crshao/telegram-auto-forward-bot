import re
import time
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_username, URL
from telebot.mastermind import get_response

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # get the chat_id to be able to respond to the same user
    chat_id = update.message.chat.id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message: ", text)

    #welcome message
    if text == "/start":
        bot_welcome = """
        HELLO, THIS IS AN AUTO FORWARD BOT
        """
        bot.sendChatAction(chat_id=chat_id, action="typing")
        time.sleep(1.5)
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    else:
        try:
            #just testing
            bot.sendMessage(chat_id=chat_id, text="comeon", reply_to_message_id=msg_id)
        except:
            bot.sendMessage(chat_id=chat_id, text="There is an error", reply_to_message_id=msg_id)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    #we use the bot object to link the bot to our app which live
    #in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'
if __name__ == '__main__':
    #note the threaded arg which allow
    #your app to have more than one thread
    app.run(threaded=True)

