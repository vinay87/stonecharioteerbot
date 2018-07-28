import os
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.DEBUG)

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

def start(bot, update):
    bot.send_message(chat_id=update.message.id, text="Hello, world!")

def categorize(bot, update):
    """
    Takes a user's query and categorizes it.
    TODO: Use `nltk` or `sklearn` here.
    """
    query = update.message.text.lower()
    if "cowsay" in query:
        if "fortune" in query:
            cowsay_fortune(bot, update)
        else:
            cowsay(bot, update, update.message.text)
        return True
    elif "fortune" in query:
        fortune(bot, update)
        return True
    return None

def cowsay(bot, update, text):
    import subprocess
    out = subprocess.check_output(["cowsay", text.replace("cowsay ", "")])
    logging.debug(out.decode("ascii"))
    return send(bot, update, out.decode("ascii"))

def fortune(bot, update):
    import subprocess
    out = subprocess.check_output(["fortune"])
    logging.debug(out.decode("ascii"))
    return send(bot, update, out.decode("ascii"))

def cowsay_fortune(bot, update):
    import subprocess
    out = subprocess.check_output(["fortune"])
    out = subprocess.check_output(["cowsay", out.decode("ascii")])
    return send(bot, update, out.decode("ascii"))

def send(bot, update, message):
    bot.send_message(chat_id=update.message.chat_id, text=message)

def response(bot, update):
    response_attempt = categorize(bot, update)
    if response_attempt is None:
        bot.send_message(chat_id=update.message.chat_id, text="I'm not sure what you need.")

def serve(env):
    import logging
    from dotenv import load_dotenv
    load_dotenv(env)
    updater = Updater(token=os.environ["TOKEN"])
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    response_handler = MessageHandler(Filters.text, response)
    dispatcher.add_handler(response_handler)

    try:
        logging.info("Beginning polling now!")
        updater.start_polling()
    except KeyboardInterrupt:
        updater.stop()
