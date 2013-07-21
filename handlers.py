# -*- coding: utf-8 -*-
import datetime
import webapp2
from webapp2_extras import jinja2

from webapp2_extras import auth
from webapp2_extras import sessions



class BaseHandler(webapp2.RequestHandler):
  """
    BaseHandler for all requests all other handlers will
    extend this handler

  """
  @webapp2.cached_property
  def auth(self):
    return auth.get_auth()

  @webapp2.cached_property
  def user_info(self):
    return self.auth.get_user_by_session()

  @webapp2.cached_property
  def user(self):
    u = self.user_info
    return self.user_model.get_by_id(u['user_id']) if u else None

  @webapp2.cached_property
  def user_model(self):
    return self.auth.store.user_model

  @webapp2.cached_property
  def session(self):
    return self.session_store.get_session(backend="datastore")

  @webapp2.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def render_template(self, template_name, template_values):
    user = self.user_info
    template_values['user'] = user
    self.response.write(self.jinja2.render_template(
      template_name, **template_values))

  def render_string(self, template_string, template_values):
    self.response.write(self.jinja2.environment.from_string(
      template_string).render(**template_values))

  def display_message(self, message):
    template_values = {
      'message': message
    }
    self.render_template('template_files/message.html', template_values)

  def dispatch(self):
    self.session_store = sessions.get_store(request=self.request)

    try:
      webapp2.RequestHandler.dispatch(self)
    finally:
      self.session_store.save_sessions(self.response)
