from Histogram_english import Text
import logging
import key
import json 
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
    text = """Send me the text to count the number of times each word is repeated.\n \
Example: toes: this is only example"""
    update.message.reply_text(text)
    return IMPUT_TEXT_TRANSLATE
    
    
def counter(update,context):
    text,to_idiom=separate_idiom_text(update.message.text)
    text = Text(text)
    count = text.sort_words(reverse=True)
    count_translate={k:(translate(k,to_idiom),v)
                     for k,v in count.items() if len(k) > 3}
    best_format = json.dumps(count_translate, indent=1, ensure_ascii=False)
    update.message.reply_text(best_format)
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


IMPUT_TEXT_TRANSLATE=0 

def translate_command_handler(update,context): 
    text_messege="""Send me a text to translate with format: to(code idiom) \
Example: toes:Hello World!"""
    update.message.reply_text(text_messege)
    return IMPUT_TEXT_TRANSLATE

def separate_idiom_text(message): 
    to_idiom = message[2:4]
    text = message[5:]
    return text,to_idiom
    
def translate(text,to_idiom):
    idiom_origin=idiom_detection(text)
    model_id=f"{idiom_origin}-{to_idiom}"
    translation = language_translator.translate(text=text,
                                                model_id=model_id).get_result()
    translated = translation["translations"][0]["translation"]    
    return translated
    
def send_translate(update,context):
    text,to_idiom=separate_idiom_text(update.message.text)
    translated = translate(text,to_idiom)
    update.message.reply_text(translated)
    return ConversationHandler.END


def idiom_detection(text):
    text = TextBlob(text)
    idiom = text.detect_language()
    return idiom

    
def main():    

    #Updater receive the updates from Telegram
    updater = Updater(token=key.TOKEN)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # on different commands - answer counterin Telegram
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("translate",translate_command_handler)
        ],
        states ={
            IMPUT_TEXT_TRANSLATE:[MessageHandler(Filters.text,send_translate)]
        },
        fallbacks=[] 
    ))
    
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("count",counter_message)
        ],
        states ={
            IMPUT_TEXT_TRANSLATE:[MessageHandler(Filters.text,counter)]
        },
        fallbacks=[] 
    ))
    
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