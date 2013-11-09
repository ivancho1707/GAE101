import logging
import webapp2

from models import *

from google.appengine.api import users, channel
from django.utils import simplejson as json

from settings import *

class Home(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logging.debug("user (id: " + user.nickname() + ") has logged in.")
            send_message('<em>user ' + user.nickname() + ' has connected</em>')
            channel_id = user.user_id()
            chat_token = channel.create_channel(channel_id)
            template_values = {
                'nickname'  : user.nickname(),
                'user_id'   : user.user_id(),
                'channel_id': channel_id,
                'chat_token': chat_token
            }
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class SendMessage(webapp2.RequestHandler):
    def post(self):
        user            = users.get_current_user()
        message         = '<strong>%s dice:</strong> %s' % (user.nickname(), self.request.get('message'))
        send_message(message)
        template_values = {}
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
            
class Disconnected(webapp2.RequestHandler):
    def post(self):
        client_id   = self.request.get('from')
        logging.debug('client_id:' + client_id + 'disconnected')
        channel_key = db.Key.from_path('Channels', client_id)
        current_channel = db.get(channel_key)
        if current_channel:
            db.delete(channel_key)

class Connected(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()

        client_id   = self.request.get('from')
        logging.info('client_id:' + client_id + ' has connected')
        channel_key = db.Key.from_path('Channels', client_id)
        current_channel = db.get(channel_key)
        if not current_channel:
            current_channel = Channels(key_name = client_id, channel_id = client_id)
            current_channel.put()

def send_message(msg):
    all_channels = Channels.all().fetch(1000)
    for c in all_channels:
        channel_msg = json.dumps({'success': True, 'msg': msg+'</br>'})
        logging.info('sending message to:' + c.channel_id)
        channel.send_message(c.channel_id, channel_msg)