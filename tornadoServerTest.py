#Lots of code blatantly stolen from the Websocket demo included with
#Tornado

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
from tornado import gen
import gameWorldInterface
import message

global ListOfUniquePeeps
ListOfUniquePeeps = {}

global GlobalGameInterface
GlobalGameInterface = ""

class DoThat(tornado.web.RequestHandler):
    def get(self):
        self.write("THIS IS ANOTHER PAGE")

class MainHandler(tornado.web.RequestHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("index.html", messages=ComSocket.cache)
        print(repr(self.request))

class someMessage(tornado.web.RequestHandler):
    def post(self):
        message = {
            "id": "SOMEID",
            "from": "I GUESS A USER",
            "body": "LIKE I CARE"
        }
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
"""
myapplication = tornado.web.Application([
    (r"/", MainHandler),
    (r"/somepage", DoThat),
    (r"/MESSAGING", someMessage)
    ]
    )
"""


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/somepage", DoThat),
            (r"/MESSAGING", someMessage),
            (r"/ComSocket", ComSocket),
            (r"/mylogin", LoginToThis),
            (r"/pickupMessages", PickUpMessages),
            (r"/ENDTHIS", EndLoop)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #login_url="/mylogin"
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class EndLoop(tornado.web.RequestHandler):
    def get(self):
        tornado.ioloop.IOLoop.instance().stop()
        print("Heysup this is end")

class ComSocket(tornado.websocket.WebSocketHandler):
    waiters = set()
    #ComSocket is the class for ALL THE THINGS. AGH.
    #Cache isn't a list, cache needs to be a dictionary...of lists.
    #Each user will have an individual list.
    GameInterface = ""
    cache = []
    cache_size = 100

    def open(self):
        #ANYTIME SOMEONE JOINS
        ComSocket.waiters.add(self)
        print(self.request.remote_ip)
        global GlobalGameInterface
        self.GameInterface = GlobalGameInterface
        global ListOfUniquePeeps
        ListOfUniquePeeps[self.request.remote_ip] = self.request.remote_ip
        #myGameWorldInterface.sendMessageToWorld(self.request.remote_ip, "server", "JOINED YO")
        

    def on_close(self):
        #ANYTIME SOMEONE LEAVES (How do we know?)
        ComSocket.waiters.remove(self)

    def on_message(self, message):
        #ANYTIME WE GET A HIT FROM SOMETHING
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"]
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))
        print("Some message just happened")

        ComSocket.update_cache(chat, self.request.remote_ip)
        ComSocket.send_updates(chat, self.request.remote_ip)
        self.putMessageInInterfaceBox(chat["body"], self.request.remote_ip)

    @classmethod
    def send_updates(cls, chat, myuser):
        for waiter in cls.waiters:
            print("WAITER:" + myuser)
            try:
                waiter.write_message(chat)
            except:
                print("COULD NOT SEND MESSAGE")

    @classmethod
    def update_cache(cls, chat, myuser):
        #We don't append the chat on a message, we must identify
        #who that message goes to before we append it
        #If it goes to us we append it if it doesn't we don't.
        print("Updater:" + myuser)
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    def pickUpMessagesFromInterface(self):
        pass

    def putMessageInInterfaceBox(self, tinyChat, personIP):
        print(tinyChat)
        print(personIP)
        myMessage = message.Message(personIP, "world", tinyChat)
        self.GameInterface.sendMessageToWorld(myMessage)
        print("Put message in the box hopefully?")
            
class LoginToThis():
    @gen.coroutine
    def get(self):
        self.write("You hit the login page, yay!")


class PickUpMessages():
    def get(self):
        pass
        #If I got hit with this, then I was just told I need to go pick up messages
        #and distribute them, yo.
"""
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
"""
def beginServer(myGameInterface):
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8888)
    global GlobalGameInterface
    GlobalGameInterface = myGameInterface
    tornado.ioloop.IOLoop.instance().start()
