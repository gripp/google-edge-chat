"""Contains chat handler for writing out the base chat page."""
import os
import jinja2
import webapp2


class Handler(webapp2.RequestHandler):
  _JINJA_ENVIRONMENT = jinja2.Environment(
      loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
      extensions=['jinja2.ext.autoescape'],
      autoescape=True)

  def WriteTemplate(self, template, args):
    template = self._JINJA_ENVIRONMENT.get_template('/templates/%s' % template)
    self.response.write(template.render(args))
