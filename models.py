import logging
import time
import webapp2_extras.appengine.auth.models

from google.appengine.ext import ndb

from webapp2_extras import security

class User(webapp2_extras.appengine.auth.models.User):
  def set_password(self, raw_password):
    self.password = security.generate_password_hash(raw_password, length=12)

  @classmethod
  def get_by_auth_token(cls, user_id, token, subject='auth'):
    token_key = cls.token_model.get_key(user_id, subject, token)
    user_key = ndb.Key(cls, user_id)
    valid_token, user = ndb.get_multi([token_key, user_key])
    if valid_token and user:
      timestamp = int(time.mktime(valid_token.created.timetuple()))
      return user, timestamp

    return None, None

  @property
  def crawled(self):
    return Profile.query(Profile.visitors == self.key).order(-Profile.date_updated)

  okcupid_username = ndb.StringProperty()
  okcupid_pw = ndb.StringProperty()
  is_crawling = ndb.BooleanProperty(default=False)
  profiles_visited_counter = ndb.IntegerProperty(default=0)
  daily_quota = ndb.IntegerProperty(default=100)
  profiles_visited_today = ndb.IntegerProperty(default=0)
  last_quota_reset = ndb.DateTimeProperty()

class Profile(ndb.Model):
  date_added = ndb.DateTimeProperty(auto_now_add=True)
  date_updated = ndb.DateTimeProperty(auto_now=True)
  username = ndb.StringProperty()
  img = ndb.StringProperty()
  img_more = ndb.StringProperty(repeated=True)
  img_more_captions = ndb.StringProperty(repeated=True)
  match = ndb.StringProperty()
  friend = ndb.StringProperty()
  enemy = ndb.StringProperty()
  age = ndb.StringProperty()
  gender = ndb.StringProperty()
  orientation = ndb.StringProperty()
  status = ndb.StringProperty()
  location = ndb.StringProperty()
  ethnicity = ndb.StringProperty()
  height = ndb.StringProperty()
  body_type = ndb.StringProperty()
  diet = ndb.StringProperty()
  smoking = ndb.StringProperty()
  drinking = ndb.StringProperty()
  drugs = ndb.StringProperty()
  religion = ndb.StringProperty()
  sign = ndb.StringProperty()
  education = ndb.StringProperty()
  job = ndb.StringProperty()
  income = ndb.StringProperty()
  children = ndb.StringProperty()
  pets = ndb.StringProperty()
  languages = ndb.StringProperty()
  last_online = ndb.StringProperty()
  essay_text_0 = ndb.TextProperty()
  essay_text_1 = ndb.TextProperty()
  essay_text_2 = ndb.TextProperty()
  essay_text_3 = ndb.TextProperty()
  essay_text_4 = ndb.TextProperty()
  essay_text_5 = ndb.TextProperty()
  essay_text_6 = ndb.TextProperty()
  essay_text_7 = ndb.TextProperty()
  essay_text_8 = ndb.TextProperty()
  essay_text_9 = ndb.TextProperty()
  what_i_want = ndb.TextProperty()
  visitors = ndb.KeyProperty(repeated=True)
  visitor_count = ndb.IntegerProperty()

class ToBeVisited(ndb.Model):
  profiles = ndb.StringProperty(repeated=True)

class ProfileList(ndb.Model):
  date_added = ndb.DateTimeProperty(auto_now_add=True)
  date_updated = ndb.DateTimeProperty(auto_now=True)
  user_key = ndb.KeyProperty()
  profile = ndb.StringProperty()
  visited = ndb.BooleanProperty()