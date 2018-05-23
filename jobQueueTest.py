import logging
import pythonwhois
from telegram.ext import Updater,CommandHandler,MessageHandler
from datetime import datetime,timedelta

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
domains = ['aban.solutions','tasbih.audio','hamrahang.com','hamrahang.ir','roozarooz.com','roozarooz.news','roozarooz.ir','radioactive.one','avano.audio','adologic.io','noise.reviews','aban.mobi']

def wellcome (bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="Please use /update Command in order to get updated domain expiry dates")
def callback_alarm (bot,job):
    bot.send_message(chat_id=job.context , text=job.text)

def start (bot,update,job_queue):
    dates = ''
    for dom in domains:
        cont= pythonwhois.get_whois(dom)

        if 'expiration_date' in cont:
            a = cont['expiration_date']
            delta = a[0] - datetime.now()

            dates = dates +dom+' : \n'+a[0].strftime("%Y/%m/%d")+' --- '+str(delta.days)+' days'+'\n \n'
            if delta < timedelta(days=10):
                bot.send_message(chat_id=update.message.chat_id,context=update.message.chat_id,text='Warning, Domain '+ dom + ' will be expired in 10 days.')
            job_queue.run_once(callback_alarm,a[0]- timedelta(days=10))
    bot.send_message(chat_id=update.message.chat_id, text=dates)


def main():
    updater= Updater('549855189:AAE46QJwcF4f7UKw9lBMZ98HNu45chUPuBs')
    dp=updater.dispatcher
    j= updater.job_queue
    dp.add_handler(CommandHandler("start",wellcome))
    timer_handler=CommandHandler('update',start, pass_job_queue=True)
    updater.dispatcher.add_handler(timer_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()