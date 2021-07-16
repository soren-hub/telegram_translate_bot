from Histogram_english import Text
import logging
import key
import json 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters)
from textblob import TextBlob






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
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
 
    
    
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
    update.message.reply_text(str(count_translate))
    return ConversationHandler.END



IDIOM=""
IMPUT_VOICE=0


def voice_message(update,context):
    messege="Write the language in which you will send the message.\
It can be English or Spanish only."
    update.message.reply_text(messege)
    return IDIOM
    
def voice_save(update,context): 
    file_id= update.message.voice.file_id
    file = context.bot.getFile(file_id)
    file.download('./voice/voice.ogg')

def send_transcript_to_text(update,context):
    voice_save(update,context)
    text= transcript_to_text('./voice/voice.ogg')
    update.message.reply_text(text)
    return ConversationHandler.END

def receive_idiom(update,context): 
    idiom = update.message.text.strip().lower()
    
    if idiom=="spanish": 
        IDIOM = "es-CL_BroadbandModel"
        print(IDIOM)
    else:
        IDIOM = "en-US_BroadbandModel"
        print(IDIOM)
    update.message.reply_text("Send me your speech")
    return IMPUT_VOICE
    
        
def transcript_to_text(path_file):
    from ibm_watson import SpeechToTextV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    authenticator = IAMAuthenticator(key.API_SPEECH_KEY)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(key.service_speech_url) 
    print(IDIOM)
    with open(path_file,'rb') as audio_file:
        recognition_job = speech_to_text.create_job(
                                                audio_file,
                                                content_type='audio/ogg',
                                                model=IDIOM).get_result()

    return recognition_job["results"][0]["alternatives"][0]["transcript"]
    

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
    from ibm_watson import LanguageTranslatorV3
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    authenticator = IAMAuthenticator(key.API_TRANSLATE_KEY)
    language_translator = LanguageTranslatorV3(version='2018-05-01',
                                               authenticator=authenticator)
    language_translator.set_service_url(key.service_translate_url)
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
    
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("info",voice_message)
        ],
        states ={
            IDIOM:[MessageHandler(Filters.text,receive_idiom)],
            IMPUT_VOICE:[MessageHandler(Filters.voice,send_transcript_to_text)]
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