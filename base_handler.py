"""Contains base handler."""
import os
import jinja2
import webapp2


class Handler(webapp2.RequestHandler):
  """Generic, base functionality handler. Other page handlers inherit this."""

  # Sets up the page templating environment. See also:
  # https://developers.google.com/appengine/docs/python/gettingstartedpython27/templates
  _JINJA_ENVIRONMENT = jinja2.Environment(
      loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
      extensions=['jinja2.ext.autoescape'],
      autoescape=True)

  def WriteTemplate(self, template, args):
    """Writes given arguments out to the given template in an HTTP response."""
    template = self._JINJA_ENVIRONMENT.get_template('/templates/%s' % template)
    self.response.write(template.render(args))
