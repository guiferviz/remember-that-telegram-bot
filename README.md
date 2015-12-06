
Remember That Telegram Bot
==========================

This Telegram bot allows you to schedule reminders.


Requirements.
-------------

Google AppEngine for Python

python-telegram-bot


NOTE: If you want your bot to send images from a url, before doing deploy to Google AppEngine,
you must have in mind that the python-telegram-bot library uses "from urllib.request import urlopen"
in the inputfile.py file. Change that to "from urllib2 import urlopen" if you don't have pay apps on GAE.
