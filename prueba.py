import telepot
import sys
import time
from telepot.loop import MessageLoop
from googletrans import Translator

traductor = Translator()

def handler(msg):
    msgType, chtType, chatId = telepot.glance(msg)
    mensaje = msg['text']
    
    if mensaje[0:5] == "ToEn:":
    	traduccion = traductor.translate(mensaje[6:],dest = 'en')
    	bot.sendMessage(chatId,traduccion.text)
    	
    elif mensaje[0:5] == "ToEs:":
    	traduccion = traductor.translate(mensaje[6:],dest = 'es')
    	bot.sendMessage(chatId,traduccion.text)
  
    else:
    	bot.sendMessage(chatId, "No se reconoce ninguno de los comandos establecidos :( F")

#aqui ponen su TOKEN!
TOKEN = ""

bot = telepot.Bot(TOKEN)      

MessageLoop(bot,handler).run_as_thread()

while True:
    time.sleep(10)