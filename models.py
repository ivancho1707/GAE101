from google.appengine.ext import db

class Channels(db.Model):
    channel_id  = db.StringProperty(default = "") 