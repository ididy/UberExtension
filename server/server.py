import tornado.ioloop
import tornado.web
import urllib
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPClient
from config import config
from auth_handler import AuthHandler
from base_handler import BaseHandler
from product_handler import ProductHandler
from ride_handler import RideHandler

class MainHandler(BaseHandler):
  def get(self):
    print(self.current_user)
    self.write("Hello world!")  

class TokenHandler(tornado.web.RequestHandler):
  def get(self):
    print("Token route called") 

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", tornado.web.RedirectHandler, dict(url=config["AUTH_REDIRECT"], permanent=False)),
    (r"/auth", AuthHandler),
    (r"/token", TokenHandler),
    (r"/api/products", ProductHandler),
    (r"/api/requests", RideHandler)
  ], cookie_secret=config["COOKIE_SECRET"])

if __name__ == "__main__":
  app = make_app()
  app.listen(8888)
  print("Server listening on 8888")
  tornado.ioloop.IOLoop.current().start()