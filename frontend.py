#!/usr/bin/env python

import browser
import json
import logging
import os
import random
import webapp2

from Crypto.Cipher import AES
from Crypto import Random

from google.appengine.api import backends
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch

from handlers import BaseHandler

from models import User, Profile, ToBeVisited, ProfileList

from time import sleep

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

KEY = b'%s' % os.environ.get('KEY')

### Functions ###

def encode_pw(password):
  iv = Random.new().read(AES.block_size)
  cipher = AES.new(KEY, AES.MODE_CFB, iv)
  msg = iv + cipher.encrypt(b'%s' % password)
  hex_encode = msg.encode("hex")
  return hex_encode

def decode_pw(hex_encode):
  decoded = hex_encode.decode('hex')
  iv = decoded[:AES.block_size]
  cipher = AES.new(KEY, AES.MODE_CFB, iv)
  orig = cipher.decrypt(decoded[AES.block_size:])
  return str(orig)

def user_required(handler):
  """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
  """
  def check_login(self, *args, **kwargs):
    auth = self.auth
    if not auth.get_user_by_session():
      self.redirect(self.uri_for('login'), abort=True)
    else:
      return handler(self, *args, **kwargs)

  return check_login

def gql_json_parser(query_obj):
  result = []
  for entry in query_obj:
    result.append(dict([(p, unicode(getattr(entry, p))) for p in entry._properties]))
  return result

### APIs ###

# List of profiles crawled
class GetProfileList(BaseHandler):
  def get(self):
    profiles = gql_json_parser(self.user.crawled)
    
    output = {
      'status': 'SUCCESS',
      'count': len(profiles),
      'data': profiles,
    }

    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(output))

# List of profiles to be visited
class ToBeVisited(BaseHandler):
  def get(self):
    to_be_visited = ProfileList.query(
      ProfileList.user_key == self.user.key,
      ProfileList.visited == False).order(-ProfileList.date_added)
    to_be_visited = gql_json_parser(to_be_visited)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(to_be_visited))

# User info
class UserInfo(BaseHandler):
  def get(self):
    user = self.user
    message = {
      'is_crawling': user.is_crawling,
      'daily_quota': user.daily_quota,
      'profiles_visited_today': user.profiles_visited_today,
      'profiles_visited_counter': user.profiles_visited_counter,
    }
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(message))

# Add OkCupid
class AddOkcupidAPI(BaseHandler):
  def post(self):
    okcupid_username = self.request.get('okcupid_username')
    okcupid_password = self.request.get('okcupid_password')
    encoded_okcupid_pw = encode_pw(okcupid_password)

    logging.info(okcupid_username)
    logging.info(okcupid_password)
    # if not User.query(User.okcupid_username == okcupid_username):
    # user = self.user
    # user.okcupid_username = okcupid_username
    # user.okcupid_pw = encoded_okcupid_pw
    # user.put()

    # self.response.headers['Content-Type'] = 'application/json'
    # self.response.write(json.dumps(message))

# Is crawling
class IsCrawling(BaseHandler):
  def get(self):
    user = self.user
    message = {
      'status': user.is_crawling
    }
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(message))

class CrawlStarter(BaseHandler):
  @user_required
  def get(self, *args, **kwargs):
    user = self.user
    message = {}
    if not user.is_crawling:
      auth_id = self.user_info['auth_ids'][0]
      num = kwargs['num']

      taskqueue.add(url='/crawlworker', params={'auth_id': auth_id, 'num': num})
      user.is_crawling = True
      user.put()
      message = {
        'status': 'SUCCESS',
        'message': 'Crawl started'
      }
    else:
      logging.info('User is crawling')
      message = {
        'status': 'FAIL',
        'message': 'User is already crawling'
      }

    self.response.write(json.dumps(message))

### Workers ###
class CrawlWorker(BaseHandler):
  def post(self):
    num = int(self.request.get('num'))
    profiles_visited = 0
    auth_id = self.request.get('auth_id')
    user = User.get_by_auth_id(auth_id)
    logging.info(user.key)

    okcupid_username = user.okcupid_username
    okcupid_pw = decode_pw(user.okcupid_pw)
    logging.info('okcupid username: %s' % okcupid_username)
    logging.info('okcupid password: %s' % okcupid_pw)

    # Create browser
    br = browser.create_logged_in_browser(okcupid_username, okcupid_pw)

    # Get the to be visited list
    to_be_visited = ProfileList.query(
        ProfileList.visited == False,
        ancestor = user.key).order(ProfileList.date_added).fetch(num)

    # If it doesn't exist, get the seed profile list
    if not to_be_visited:
      browser.get_first_profiles(user, br)
      

    profiles_visited_counter = 0
    while profiles_visited_counter < num:
      to_be_visited = ProfileList.query(
        ProfileList.visited == False,
        ancestor = user.key).order(ProfileList.date_added).fetch(num-profiles_visited_counter)
      for item in to_be_visited:
        browser.visit_page(user, br, item.profile)
        item.visited = True
        item.put()
        secs = random.randint(0, 2500) / 1000.0
        sleep(secs)
      profiles_visited_counter = user.profiles_visited_counter
          
    user.is_crawling = False
    user.profiles_visited_today += user.profiles_visited_counter
    user.profiles_visited_counter = 0
    user.put()

### Handlers ####

class TryPw(BaseHandler):
  def get(self):
    password = 'this is my test password'
    encoded_pw = encode_pw(password)
    decode_pw(encoded_pw)

class Home(BaseHandler):
  @user_required
  def get(self):
    self.render_template('index.html', {})

class Index(BaseHandler):
  def get(self):
    if self.user:
      self.redirect('/home')
    else:
      self.render_template('template_files/index.html', {})

# User registration
class SignupHandler(BaseHandler):
  def get(self):
    self.render_template('template_files/signup.html', {})

  def post(self):
    email = self.request.get('email')
    password = self.request.get('password')
    unique_properties = ['email_address']
    user_data = self.user_model.create_user(email,
      unique_properties,
      email_address=email, password_raw=password, verified=False)
    if not user_data[0]:
      self.display_message('Unable to create user for email %s because of \
        duplicate keys %s' % (user_name, user_data[1]))
      return

    user = user_data[1]
    user_id = user.get_id()

    token = self.user_model.create_signup_token(user_id)

    verification_url = self.uri_for('verification', type='v', user_id=user_id,
      signup_token=token, _full=True)

    msg = 'Send an email to user in order to verify their address. \
          They will be able to do so by visiting <a href="{url}">{url}</a>'

    self.display_message(msg.format(url=verification_url))

class LoginHandler(BaseHandler):
  def get(self):
    self._serve_page()

  def post(self):
    email = self.request.get('email')
    password = self.request.get('password')
    try:
      u = self.auth.get_user_by_password(email, password, remember=True)
      self.redirect(self.uri_for('home'))
    except (InvalidAuthIdError, InvalidPasswordError) as e:
      logging.info('Login failed for user %s because of %s', email, type(e))
      self._serve_page(True)

  def _serve_page(self, failed=False):
    email = self.request.get('email')
    params = {
      'email': email,
      'failed': failed
    }
    self.render_template('template_files/login.html', params)

class LogoutHandler(BaseHandler):
  def get(self):
    self.auth.unset_session()
    self.redirect('/')

class AddOkcupid(BaseHandler):
  @user_required
  def get(self):
    self.render_template('template_files/okcupid.html', {})

  def post(self):
    okcupid_username = self.request.get('okcupid_username')
    okcupid_password = self.request.get('okcupid_password')
    encoded_okcupid_pw = encode_pw(okcupid_password)

    # if not User.query(User.okcupid_username == okcupid_username):
    user = self.user
    user.okcupid_username = okcupid_username
    user.okcupid_pw = encoded_okcupid_pw
    user.put()

    self.redirect('/home')

class VerificationHandler(BaseHandler):
  def get(self, *args, **kwargs):
    user = None
    user_id = kwargs['user_id']
    signup_token = kwargs['signup_token']
    verification_type = kwargs['type']

    user, ts = self.user_model.get_by_auth_token(int(user_id), signup_token, 'signup')

    if not user:
      logging.info('Could not find any user with id "%s" signup token "%s"',
        user_id, signup_token)
      self.abort(404)

    self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

    if verification_type == 'v':
      self.user_model.delete_signup_token(user.get_id(), signup_token)

      if not user.verified:
        user.verified = True
        user.put()

      self.display_message('User email address has been verified.')
      return

    elif verification_type == 'p':
      params = {
        'user': user,
        'token': signup_token
      }
      self.render_template('resetpassword.html', params)
    else:
      logging.info('verification type not supported')
      self.abort(404)

class GetList(BaseHandler):
  @user_required
  def get(self):
    logging.info(ProfileList)
    to_be_visited = ProfileList.query(
      ProfileList.visited == False,
      ancestor = self.user.key).order(-ProfileList.date_added)

    params = {
      'profiles':to_be_visited
    }
    self.render_template('template_files/getlist.html', params)
    # to_be_visited_list = ToBeVisited.query(ancestor=self.user.key).get()
    # logging.info(to_be_visited_list)
    # self.response.write(to_be_visited_list.profiles)

