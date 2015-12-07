# encoding=utf-8


import json
import logging
import webapp2

import appengine_config
from google.appengine.api import modules
from google.appengine.api import app_identity

import telegram

import telegram_token
from service import SchedulerService


# Creating the bot.
BOT = telegram.Bot(token=telegram_token.TOKEN)

# Url that receives bot messages.
BOT_URL = '/remember-that'

# Help text that is send when /start, /help or unknow command arrives.
HELP_TXT = "For *scheduling* alarms you can use any of next commands:\n"\
         + "_/set at HH:MM Alarm name_\n"\
         + "_/set each HH:MM Alarm name_\n"\
         + "For *deleting* alarms use:\n"\
         + "_/delete all_\n"


class BotHandler(webapp2.RequestHandler):

    def get(self):
        # Setting webhook.
        version = modules.get_current_version_name()
        host_name = app_identity.get_default_version_hostname()
        host_url = 'https://{}-dot-{}{}'.format(version, host_name, BOT_URL)
        BOT.setWebhook(host_url)
        # Returning info.
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(BOT.getMe())
        self.response.write('\nWEBHOOK set to: ' + host_url)

    def post(self):
        json_str = self.request.body
        logging.info("POST Body: " + json_str)
        try:
            json_obj = json.loads(json_str)
            update = telegram.Update.de_json(json_obj)
            chat_id = update.message.chat.id
            if update.message.text:
                text = update.message.text.encode('utf-8')
                logging.info("Message Text: " + text)
                text_received(chat_id, text)
        except ValueError:
            logging.error('No body or bad JSON body.')
        except AttributeError:
            logging.error('No correct attributes in JSON body.')
        except telegram.TelegramError:
            logging.error('Telegram error.')


def text_received(chat_id, text):
    if text.startswith("/set"):
        SchedulerService.process_task(text)
    elif text.startswith("/delete all"):
        pass
    elif text.startswith("/delete"):
        pass
    else:  # text.startswith("/start") or text.startswith("/help")
        BOT.sendMessage(chat_id=chat_id,
                        text=HELP_TXT,
                        parse_mode=telegram.ParseMode.MARKDOWN)


app = webapp2.WSGIApplication([
    (BOT_URL, BotHandler),
], debug=appengine_config.DEBUG)
