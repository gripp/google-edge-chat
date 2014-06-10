"""Contains AJAX handler and functions for reading and writing posts."""
import base_handler
import remark_datastore

from google.appengine.api import users


class Handler(base_handler.Handler):
  _POST_REMARK_KEY = 'post'
  _READ_REMARKS_KEY = 'read'

  def post(self):
    action = self.request.get('action', '')
    if action == self._POST_REMARK_KEY:
      remark = self.request.get('remark', None)
      if not remark:
        return
      remark_datastore.PostRemark(users.get_current_user().email(), remark)
    elif action == self._READ_REMARKS_KEY:
      self.WriteTemplate(
          'remarks.html',
          {
              'remarks': remark_datastore.ReadRemarks(
                  users.get_current_user().user_id())
          })
    else:
      self.error('Invalid action key.')
