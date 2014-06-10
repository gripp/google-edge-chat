"""Contains functions to handle dealing with posts in the datastore."""
from datetime import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb


_LAST_GET_KEY_PREFIX = 'lastget'
_LAST_POST_KEY = 'lastpost'


class Remark(ndb.Model):
  user = ndb.StringProperty(required=True)
  text = ndb.StringProperty(required=True)
  timestamp = ndb.DateTimeProperty(auto_now_add=True, required=True)


def ReadRemarks(user_id):
  start_time = memcache.get(_MakeLastGetKey(user_id))
  LogLastGet(user_id)

  remarks = []
  for remark in Remark.query(
      Remark.timestamp >= start_time).order(Remark.timestamp).fetch():
    remarks.append((remark.user, remark.text))

  return remarks


def PostRemark(user, text):
  Remark(user=user, text=text).put()


def _MakeLastGetKey(user_id):
  return ';'.join([_LAST_GET_KEY_PREFIX, user_id])


def LogLastGet(user_id):
  memcache.set(_MakeLastGetKey(user_id), datetime.now())
