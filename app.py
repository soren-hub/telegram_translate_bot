from Histogram_english import Text
import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update,context): 
    name= update.message.chat.first_name
    welcome = r"""
Welcome {0},
I will help you to improve your English by providing you with a quick and detailed translation of every word of the text you give me.
Commands: 
/toEN: translate the text you will send me into English 
/toES: translate the text you will send me into Español
/count: count the repetitions of each word in the text you send me """

    update.message.reply_text(welcome.format(name))


def counter_message(update,context):
    update.message.reply_text('Send me the text to count the number of times each word is repeated.')
    
 
    
def counter(update,context):
    text = Text(update.message.text)
    update.message.reply_text(text.sort_words(reverse=True))

#def prueba(update,context): 
#    update.message.reply_text(update)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
if __name__ == '__main__':
    #Updater receive the updates from Telegram
    updater = Updater(token='TOKEN')
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', start))
    
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("count",counter_message)
        ],
        states ={
            
        }
    ))
    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text,prueba))

    # log all errors
    dp.add_error_handler(error)
    
    print('Bot is polling')
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()