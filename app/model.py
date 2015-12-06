

from google.appengine.ext import db


class Forgetful(db.Model):

    id = db.IntegerProperty()
    last_use = db.DateTimeProperty(auto_now=True)


class ForgetfulDTO(object):

    def __init__(self, forgetful):
        self.id = forgetful.id
        self.last_use = forgetful.last_use


class ForgetfulDAO(object):

    @classmethod
    def all(cls):
        return [ForgetfulDTO(c) for c in Forgetful.all()]

    @classmethod
    def save(cls, chat_id):
        chat = Forgetful(id=chat_id)
        chat.put()

    @classmethod
    def exist(cls, chat_id):
        all_chats = Forgetful.all()
        all_chats.filter('id', chat_id)
        chat = all_chats.get()
        if chat:
            # With this we change automatically 'last_use' value.
            chat.put()
        return all_chats.get()
