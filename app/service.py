
from datetime import datetime
import logging
import re

from nltk.tokenize.regexp import RegexpTokenizer


# REGULAR EXPRESSIONS for parse commands.
RE_SET = re.compile('/set')
RE_AT = re.compile('at')
RE_HOUR = re.compile('([0-9])?[0-9]:[0-9][0-9]')
RE_PHRASE = re.compile('.+')
RE_NUM = re.compile('[0-9]+')
RE_DELETE = re.compile('/delete')

TOKENIZER = RegexpTokenizer('[^ ]+')


class SchedulerService():

    @classmethod
    def process_task(cls, text):
        try:
            tokens = TOKENIZER.tokenize(text)
            if RE_SET.match(tokens[0].lower()):
                SchedulerService._process_set_task(tokens[1:])
            elif RE_DELETE.match(tokens[0]):
                SchedulerService._process_delete_task(tokens[1:])
            return True
        except TimeException as e:
            logging.error(e)
            return False

    @classmethod
    def _process_set_task(cls, tokens):
        if RE_AT.match(tokens[0].lower()):
            time = SchedulerService._get_hour_minutes(tokens[1])
            text = " ".join(tokens[2:])[:100]
            logging.info("Setting alarm at {}:{} with text \"{}\"".format(
                time.hour, time.minute, text))

    @classmethod
    def _process_delete_task(cls, tokens):
        pass

    @classmethod
    def _get_hour_minutes(cls, text):
        """
            Returns two numbers: hours and minutes.
            Text must be in format HH:MM or H:MM.
            HH must be between 0 and 23 and MM between 0 and 59.
            Returns -1, -1 if there is an error.
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
