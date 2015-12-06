
import re


# REGULAR EXPRESSIONS for parse commands.
RE_HOUR = re.compile('/set at ([0-9])?[0-9]:[0-9][0-9]')


class SchedulerService():

    def process_task(text):
        return 0, 0
