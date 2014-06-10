"""Defines handler paths and initiates the app."""
import webapp2

import ajax_handler
import chat_handler

app = webapp2.WSGIApplication(
    [('/', chat_handler.Handler), ('/ajax', ajax_handler.Handler)], debug=False)
