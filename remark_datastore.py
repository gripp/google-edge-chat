"""Contains functions to handle dealing with posts in the datastore."""
from datetime import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb


_LAST_GET_KEY_PREFIX = 'lastget'
_LAST_POST_KEY = 'lastpost'


class Remark(ndb.Model):
  """Class to represent a single message sent by a user."""

  # For more about how AppEngine datastores work, see:
  # https://developers.google.com/appengine/docs/python/ndb/

  user = ndb.StringProperty(required=True) # ID of the user who sent this.
  text = ndb.StringProperty(required=True) # The text the user entered.

  # Time the remark was sent in ms since the epoch.
  timestamp = ndb.DateTimeProperty(auto_now_add=True, required=True)


def ReadRemarks(user_id):
  """Get all remarks since the given user's last read."""
  # The time when the user last read; start time for the query.
  start_time = memcache.get(_MakeLastGetKey(user_id))

  LogLastGet(user_id)

  # Query the datastore for remarks. Only get remarks posted since the last time
  # this user checked (Remark.timestamp >= start_time). Order them by when they
  # were posted. Return the results as a list of tuples with (user, text).
  return [
      (remark.user, remark.text)
      for remark
      in Remark.query(
          Remark.timestamp >= start_time).order(Remark.timestamp).fetch()]


def PostRemark(user, text):
  """Puts a new remark in the datastore."""
  Remark(user=user, text=text).put()


def _MakeLastGetKey(user_id):
  """Makes a memcache key for when the given user last read remarks."""
  return ';'.join([_LAST_GET_KEY_PREFIX, user_id])


def LogLastGet(user_id):
  """Logs the fact that a given user read remarks."""
  # This sets an entry in memcache. Memcache is basically transient, server-side
  # storage of key-value pairs. Here, we use the result of
  # _MakeLastGetKey(user_id) as the key and the current system time as the
  # value. Then later we can get the time back out by reading from memcache with
  # the same key. See:
  # https://developers.google.com/appengine/docs/python/memcache/usingmemcache
  memcache.set(_MakeLastGetKey(user_id), datetime.now())
