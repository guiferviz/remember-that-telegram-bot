
from datetime import datetime
import logging
import re

from google.appengine.ext import deferred
from google.appengine.api import taskqueue

from nltk.tokenize.regexp import RegexpTokenizer

import main


# REGULAR EXPRESSIONS for parse commands.
RE_SET = re.compile('/set')
RE_AT = re.compile('at')
RE_EACH = re.compile('each')
RE_HOUR = re.compile('([0-9])?[0-9]:[0-9][0-9]')
RE_PHRASE = re.compile('.+')
RE_NUM = re.compile('[0-9]+')
RE_DELETE = re.compile('/delete')
RE_S = re.compile('[0-9]+s')
RE_M = re.compile('[0-9]+m')

TOKENIZER = RegexpTokenizer('[^ ]+')


class SchedulerService():

    def create_task(cls, chat_id, time, text, next_time):
        pass


class ParserService():

    @classmethod
    def parse_command(cls, chat_id, text):
        try:
            tokens = TOKENIZER.tokenize(text)
            if RE_SET.match(tokens[0].lower()):
                return ParserService._process_set_task(chat_id, tokens[1:])
            elif RE_DELETE.match(tokens[0]):
                return ParserService._process_delete_task(chat_id, tokens[1:])
        except TimeException as e:
            logging.error(e)
        return False

    @classmethod
    def _process_set_task(cls, chat_id, tokens):
        if RE_AT.match(tokens[0].lower()):
            time = ParserService._get_hour_minutes(tokens[1])
            text = " ".join(tokens[2:])[:100]
            logging.info("Setting alarm at {}:{} with text \"{}\"".format(
                time.hour, time.minute, text))
            tdelta = time - time.now()
            if tdelta.seconds > 0:
                logging.info("I'll alert you in {} seconds from now.".format(tdelta.seconds))
                deferred.defer(_send_alarm, chat_id, text, 0, _countdown=tdelta.seconds)
                return True
        elif RE_EACH.match(tokens[0].lower()):
            time = ParserService._get_seconds(tokens[1])
            text = " ".join(tokens[2:])[:100]
            logging.info("Setting alarm in {} seconds with text \"{}\"".format(time, text))
            logging.info("I'll alert you in {} seconds from now.".format(time))
            deferred.defer(_send_alarm, chat_id, text, time, _countdown=time)
            return True
        return False

    @classmethod
    def _process_delete_task(cls, chat_id, tokens):
        """
            Deletes all tasks of the default queue.
            TODO: delete only tasks of the chat_id user.
        """
        q = taskqueue.Queue('default')
        q.purge()
        main.BOT.sendMessage(chat_id, main.DELETE_ALL_TXT)
        return True

    @classmethod
    def _get_seconds(cls, text):
        """
            Returns the number of seconds.
            Text must be in format Mm or Ss.
            M and S could be any positive number.
            Throws a TimeException if any error occurs.
        """
        if RE_S.match(text.lower()):
            numbers = RE_NUM.findall(text)
            return int(numbers[0])
        elif RE_M.match(text.lower()):
            numbers = RE_NUM.findall(text)
            return int(numbers[0]) * 60  # Min to sec.
        raise TimeException()

    @classmethod
    def _get_hour_minutes(cls, text):
        """
            Returns two numbers: hours and minutes.
            Text must be in format HH:MM or H:MM.
            HH must be between 0 and 23 and MM between 0 and 59.
            Throws a TimeException if any error occurs.
        """
        if RE_HOUR.match(text):
            numbers = RE_NUM.findall(text)
            hours = int(numbers[0])
            minutes = int(numbers[1])
            # Check correct numbers.
            if minutes < 60 and minutes >= 0 and\
               hours < 24 and hours >= 0:
                    return datetime.strptime(text, '%H:%M')
        raise TimeException()


class TimeException(Exception):

    def __init__(self):
        self.value = "Invalid time."

    def __str__(self):
        return repr(self.value)


def _send_alarm(chat_id, text, interval):
    logging.info("Sending \"{}\" alarm to {}".format(text, chat_id))
    main.BOT.sendMessage(chat_id, text)
    if interval > 0:
        logging.info("I'll alert you in {} seconds from now.".format(interval))
        deferred.defer(_send_alarm, chat_id, text, interval, _countdown=interval)
