from handlers import *

app = webapp2.WSGIApplication(
        [
            ('/', Home),
            ('/post/', SendMessage),
            ('/_ah/channel/disconnected/', Disconnected),
            ('/_ah/channel/connected/', Connected)
        ],
        debug = True)