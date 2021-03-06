import os
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
from webhooks_handler import WebhooksHandler
from request_status_handler import RequestStatusHandler
from price_estimates_handler import PriceEstimatesHandler
from mongo_conn import mongo
from reminder_handler import ReminderHandler

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
    (r"/api/requests", RideHandler),
    (r"/api/requests/(.*)", RideHandler),
    (r"/api/webhooks", WebhooksHandler),
    (r"/tests/webhooks/(.*)", tornado.web.StaticFileHandler, {"path": "../testing/", "default_filename": "webhooks.html"}),
    (r"/api/request_status", RequestStatusHandler),
    (r"/api/estimates/price", PriceEstimatesHandler),
    # Pass reference to reminders collection in MongoDB to reminders request handlers
    (r"/api/reminders", ReminderHandler, dict(reminders_collection=mongo["reminders"])),
    (r"/api/reminders/(.*)", ReminderHandler, dict(reminders_collection=mongo["reminders"]))
  ], cookie_secret=config["COOKIE_SECRET"])

if __name__ == "__main__":
  app = make_app()
  app.listen(os.environ.get("PORT", 8888))
  print("Server listening on " + str(os.environ.get("PORT", 8888)))
  main_loop = tornado.ioloop.IOLoop.current()
  # Periodically ping websocket connections to keep them active
  ping_websockets = tornado.ioloop.PeriodicCallback(RequestStatusHandler.ping_connections, 5000, io_loop=main_loop)
  ping_websockets.start()
  main_loop.start()