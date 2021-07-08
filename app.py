from Histogram_english import Text
import logging
import key
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters)
from textblob import TextBlob
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


authenticator = IAMAuthenticator(key.API_KEY)
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator)


language_translator.set_service_url(key.service_url)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)




def start(update,context): 
    name= update.message.chat.first_name
    welcome_messege = """Welcome {0},\nI will help you to improve your English by \
providing you with a quick and detailed translation of every word of the text you \
give me."""

    update.message.reply_text(welcome_messege.format(name))
    
    
def help(update,context): 
    
    help_messege ="""Commands: \n \
/toEN: translate the text you will send me into English  
/toES: translate the text you will send me into Español  
/count: count the repetitions of each word in the text you send me """

    update.message.reply_text(help_messege)
    
    
def counter_message(update,context):
    text = 'Send me the text to count the number of times each word is repeated.'
    update.message.reply_text(text)
    
    
def counter(update,context):
    text = Text(update.message.text)
    update.message.reply_text(text.sort_words(reverse=True))


def prueba(update,context): 
    return update.message.reply_text()


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


IMPUT_TEXT_TRANSLATE=0 

def translate_command_handler(update,context): 
    update.message.reply_text("Send me a text to translate")
    return IMPUT_TEXT_TRANSLATE
    
def translate_messege(update,context):
    text = update.message.text
    idiom_origin=idiom_detection(text)
    to_idiom = ""
    model_id=f"{0}-{1}".format(idiom_origin,to_idiom)
    translation = language_translator.translate(text=text,
                                                model_id=model_id).get_result()
    translated = translation["translations"][0]["translation"]    
    update.message.reply_text(translated)
    
def input_text(update,context):
    pass

def idiom_detection(text):
    text = TextBlob(text)
    idiom = text.detect_language()
    return idiom

    
def main():    

    #Updater receive the updates from Telegram
    updater = Updater(token=key.TOKEN)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("translate",translate_command_handler)
        ],
        states ={
            IMPUT_TEXT_TRANSLATE:[MessageHandler(Filters.text,input_text)]
        }
    ))
    
    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text,idiom_detection))

    # log all errors
    dp.add_error_handler(error)
    
    print('Bot is polling')
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    
if __name__ == '__main__':
    main()