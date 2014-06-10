"""Contains chat handler for writing out the base chat page."""
import base_handler
import remark_datastore

from google.appengine.api import users


class Handler(base_handler.Handler):

  def get(self):
    remark_datastore.LogLastGet(users.get_current_user().user_id())
    self.WriteTemplate('chat.html', {})
