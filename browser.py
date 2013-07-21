import random
import logging
import mechanize

from bs4 import BeautifulSoup
from google.appengine.ext import ndb
from models import User, Profile, ToBeVisited, ProfileList
from time import sleep

# Constants
LOGIN = 'http://www.okcupid.com/'
USERNAME = 'hiphopproducer'
PASSWORD = 'Briando5'
ROOT_URL = 'http://www.okcupid.com/profile/'

class FakeLink:
  pass

def create_logged_in_browser(username, password):
  # Browser
  br = mechanize.Browser()

  # Browser options
  br.set_handle_equiv(True)
  br.set_handle_gzip(True)
  br.set_handle_redirect(True)
  br.set_handle_referer(True)
  br.set_handle_robots(False)

  # Follows refresh 0 but not hangs on refresh > 0
  br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

  br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
  br.open(LOGIN)
  br.select_form(name='loginf')
  br['username'] = username
  br['password'] = password
  br.submit()
  return br

# Get the first set of seed profiles
def get_first_profiles(user, br):
  res = br.open('http://www.okcupid.com/home')
  soup = BeautifulSoup(res.read().decode('utf-8'))
  logging.info(soup.prettify())
  left_bar_matches = []
  for item in soup.find_all('a', {'class': 'profile_image'}):
    left_bar_matches.append(item['href'])
  add_unique_profiles(user, left_bar_matches)

def visit_page(user, br, url):
  logging.info('Enter visit_page: ' + url)
  try:
    res = br.open(ROOT_URL + url)
    logging.info('Mechanize opened')
    soup = BeautifulSoup(res.read().decode('utf-8'))
    logging.info('Soup read: ' + url)

    # Get and write user data
    get_user_data(user, url, soup, br)
    logging.info('got user data')

    # Add new users to queue
    # similar_users = soup.find_all('a', {'class': 'user_image'})
    # logging.info('got similar_users')
    # left_bar_matches = soup.find_all('a', {'class': 'profile_image'})
    # logging.info('got left_bar_matches')

    users_to_be_added = []

    for item in soup.find_all('a', {'class': 'profile_image'}):
      users_to_be_added.append(item['href'])
    for item in soup.find_all('a', {'class': 'user_image'}):
      users_to_be_added.append(item['href'])
    
    logging.info(users_to_be_added)
    # for item in left_bar_matches:
    #   users_to_be_added.append(item['href'])

    # for item in similar_users:
    #   users_to_be_added.append(item['href'])

    add_unique_profiles(user, users_to_be_added)

  except AttributeError as e:
    logging.info(e)

  except UnicodeEncodeError as e:
    logging.info(e)
  

# Retrieves and puts the new user data
def get_user_data(user, url, soup, br):
  logging.info('Inside get user data function')
  userId = url

  user_data = Profile.get_by_id(userId)
  img_more = []
  img_more_captions = []

  # If this is a new profile
  if not user_data:
    logging.info('new profile')
    # Get the last online time
    if soup.find('span', {'class': 'fancydate'}) != None:
      last_online = soup.find('span', {'class': 'fancydate'}).text
    else:
      last_online = 'Online now!'
    logging.info('got the date')
    # logging.info(user.key)
    logging.info(soup.prettify())

    # img = str(soup.find(id='thumb0_a').find('img')['src'])
    # logging.info(img)
    # match = str(soup.find('span', {'class': 'match'}).text.split('%')[0])
    # logging.info(match)
    # friend = str(soup.find('span', {'class': 'friend'}).text.split('%')[0])
    # logging.info(friend)
    # enemy = str(soup.find('span', {'class': 'enemy'}).text.split('%')[0])
    # logging.info(enemy)
    # age = str(soup.find(id='ajax_age').text)
    # logging.info(age)
    # orientation = str(soup.find(id='ajax_orientation').text)
    # logging.info(orientation)
    # status = str(soup.find(id='ajax_status').text)
    # logging.info(status)
    # location = str(soup.find(id='ajax_location').text)
    # logging.info(location)
    # ethnicity = str(soup.find(id='ajax_ethnicities').text)
    # logging.info(ethnicity)
    # height = soup.find(id='ajax_height').text
    # logging.info(height)
    # body_type = str(soup.find(id='ajax_bodytype').text)
    # logging.info(body_type)
    # diet = str(soup.find(id='ajax_diet').text)
    # logging.info(diet)
    # smoking = str(soup.find(id='ajax_smoking').text)
    # logging.info(smoking)
    # drinking = str(soup.find(id='ajax_drinking').text)
    # logging.info(drinking)
    # drugs = str(soup.find(id='ajax_drugs').text)
    # logging.info(drugs)
    # religion = soup.find(id='ajax_religion').text
    # logging.info(religion)
    # sign = soup.find(id='ajax_sign').text
    # logging.info(sign)
    # education = str(soup.find(id='ajax_education').text)
    # logging.info(education)
    # income = soup.find(id='ajax_income').text
    # logging.info(income)
    # pets = soup.find(id='ajax_pets').text
    # logging.info(pets)
    # languages = str(soup.find(id='ajax_languages').text)
    # logging.info(languages)
    # essay_text_0 = unicode(soup.find(id='essay_text_0'))    
    # essay_text_1 = unicode(soup.find(id='essay_text_1'))
    # essay_text_2 = unicode(soup.find(id='essay_text_2'))
    # essay_text_3 = unicode(soup.find(id='essay_text_3'))
    # essay_text_4 = unicode(soup.find(id='essay_text_4'))
    # essay_text_5 = unicode(soup.find(id='essay_text_5'))
    # essay_text_6 = unicode(soup.find(id='essay_text_6'))
    # essay_text_7 = unicode(soup.find(id='essay_text_7'))
    # essay_text_8 = unicode(soup.find(id='essay_text_8'))
    # essay_text_9 = unicode(soup.find(id='essay_text_9'))
    # what_i_want = unicode(soup.find(id='what_i_want'))
    # logging.info(essay_text_0)
    # logging.info(essay_text_1)
    # logging.info(essay_text_2)
    # logging.info(essay_text_3)
    # logging.info(essay_text_4)
    # logging.info(essay_text_5)
    # logging.info(essay_text_6)
    # logging.info(essay_text_7)
    # logging.info(essay_text_8)
    # logging.info(essay_text_9)
    # logging.info(what_i_want)
    # logging.info(last_online)
    # logging.info([user.key])

    user_data = Profile(
      id = userId,
      username = userId,
      img = unicode(soup.find(id='thumb0_a').find('img')['src']),
      match = unicode(soup.find('span', {'class': 'match'}).text.split('%')[0]),
      friend = unicode(soup.find('span', {'class': 'friend'}).text.split('%')[0]),
      enemy = unicode(soup.find('span', {'class': 'enemy'}).text.split('%')[0]),
      age = unicode(soup.find(id='ajax_age').text),
      gender = unicode(soup.find(id='ajax_gender').text),
      orientation = unicode(soup.find(id='ajax_orientation').text),
      status = unicode(soup.find(id='ajax_status').text),
      location = unicode(soup.find(id='ajax_location').text),
      ethnicity = unicode(soup.find(id='ajax_ethnicities').text),
      height = unicode(soup.find(id='ajax_height').text),
      body_type = unicode(soup.find(id='ajax_bodytype').text),
      diet = unicode(soup.find(id='ajax_diet').text),
      smoking = unicode(soup.find(id='ajax_smoking').text),
      drinking = unicode(soup.find(id='ajax_drinking').text),
      drugs = unicode(soup.find(id='ajax_drugs').text),
      religion = unicode(soup.find(id='ajax_religion').text),
      sign = unicode(soup.find(id='ajax_sign').text),
      education = unicode(soup.find(id='ajax_education').text),
      job = unicode(soup.find(id='ajax_job').text),
      income = unicode(soup.find(id='ajax_income').text),
      children = unicode(soup.find(id='ajax_children').text),
      pets = unicode(soup.find(id='ajax_pets').text),
      languages = unicode(soup.find(id='ajax_languages').text),
      last_online = unicode(last_online),
      essay_text_0 = unicode(soup.find(id='essay_text_0')),
      essay_text_1 = unicode(soup.find(id='essay_text_1')),
      essay_text_2 = unicode(soup.find(id='essay_text_2')),
      essay_text_3 = unicode(soup.find(id='essay_text_3')),
      essay_text_4 = unicode(soup.find(id='essay_text_4')),
      essay_text_5 = unicode(soup.find(id='essay_text_5')),
      essay_text_6 = unicode(soup.find(id='essay_text_6')),
      essay_text_7 = unicode(soup.find(id='essay_text_7')),
      essay_text_8 = unicode(soup.find(id='essay_text_8')),
      essay_text_9 = unicode(soup.find(id='essay_text_9')),
      what_i_want = unicode(soup.find(class_='what_i_want')),
      visitors = [user.key],
      visitor_count = 1)
    logging.info('got the basic info')
    # Get extra photos
    res = br.follow_link(url_regex=r'/photos')
    logging.info('followed link')
    soup = BeautifulSoup(res.read().decode('utf-8'))

    # Detect if it's an album page and build new soup
    if len(soup.find_all('div', {'class': 'photo'})) == 0:
      res = br.open(ROOT_URL + userId + '/photos#0')
      soup = BeautifulSoup(res.read().decode('utf-8'))

    for item in soup.find_all('div', {'class': 'photo'}):
      img = item.find('div', {'class': 'img'}).find('img')['src']
      if item.find('p', {'class': 'text'}) is not None:
        caption = item.find('p', {'class': 'text'}).text
      else:
        caption = ''
      img_more.append(img)
      img_more_captions.append(caption)

    user_data.img_more = img_more
    user_data.img_more_captions = img_more_captions


    logging.info('entity created')
  
  # If this profile is new to this user
  elif user.key not in user_data.visitors:

    # Get the last online time
    if soup.find('span', {'class': 'fancydate'}) != None:
      last_online = soup.find('span', {'class': 'fancydate'}).text
    else:
      last_online = 'Online now!'

    user_data.populate(
      img = unicode(soup.find(id='thumb0_a').find('img')['src']),
      match = unicode(soup.find('span', {'class': 'match'}).text.split('%')[0]),
      friend = unicode(soup.find('span', {'class': 'friend'}).text.split('%')[0]),
      enemy = unicode(soup.find('span', {'class': 'enemy'}).text.split('%')[0]),
      age = unicode(soup.find(id='ajax_age').text),
      gender = unicode(soup.find(id='ajax_gender').text),
      orientation = unicode(soup.find(id='ajax_orientation').text),
      status = unicode(soup.find(id='ajax_status').text),
      location = unicode(soup.find(id='ajax_location').text),
      ethnicity = unicode(soup.find(id='ajax_ethnicities').text),
      height = unicode(soup.find(id='ajax_height').text),
      body_type = unicode(soup.find(id='ajax_bodytype').text),
      diet = unicode(soup.find(id='ajax_diet').text),
      smoking = unicode(soup.find(id='ajax_smoking').text),
      drinking = unicode(soup.find(id='ajax_drinking').text),
      drugs = unicode(soup.find(id='ajax_drugs').text),
      religion = unicode(soup.find(id='ajax_religion').text),
      sign = unicode(soup.find(id='ajax_sign').text),
      education = unicode(soup.find(id='ajax_education').text),
      job = unicode(soup.find(id='ajax_job').text),
      income = unicode(soup.find(id='ajax_income').text),
      children = unicode(soup.find(id='ajax_children').text),
      pets = unicode(soup.find(id='ajax_pets').text),
      languages = unicode(soup.find(id='ajax_languages').text),
      last_online = unicode(last_online),
      essay_text_0 = unicode(soup.find(id='essay_text_0')),
      essay_text_1 = unicode(soup.find(id='essay_text_1')),
      essay_text_2 = unicode(soup.find(id='essay_text_2')),
      essay_text_3 = unicode(soup.find(id='essay_text_3')),
      essay_text_4 = unicode(soup.find(id='essay_text_4')),
      essay_text_5 = unicode(soup.find(id='essay_text_5')),
      essay_text_6 = unicode(soup.find(id='essay_text_6')),
      essay_text_7 = unicode(soup.find(id='essay_text_7')),
      essay_text_8 = unicode(soup.find(id='essay_text_8')),
      essay_text_9 = unicode(soup.find(id='essay_text_9')),
      what_i_want = unicode(soup.find(id='what_i_want')))
    user_data.visitors.append(user.key)
    user_data.visitor_count += 1

    # Get extra photos
    res = br.follow_link(url_regex=r'/photos')
    logging.info('followed link')
    soup = BeautifulSoup(res.read().decode('utf-8'))

    # Detect if it's an album page and build new soup
    if len(soup.find_all('div', {'class': 'photo'})) == 0:
      res = br.open(ROOT_URL + userId + '/photos#0')
      soup = BeautifulSoup(res.read().decode('utf-8'))

    for item in soup.find_all('div', {'class': 'photo'}):
      img = item.find('div', {'class': 'img'}).find('img')['src']
      if item.find('p', {'class': 'text'}) is not None:
        caption = item.find('p', {'class': 'text'}).text
      else:
        caption = ''
      img_more.append(img)
      img_more_captions.append(caption)

    user_data.img_more = img_more
    user_data.img_more_captions = img_more_captions

  user_data.put()
  logging.info('user data put')

# Strip profiles to just the username
def get_stripped_profiles(profile_list):
  stripped_profiles = []
  for profile in profile_list:
    userId = profile.split('?')[0]
    userId = userId.split('/')[2]
    stripped_profiles.append(userId)
  return set(stripped_profiles)

def add_unique_profiles(user, profile_list):
  logging.info('entered add_unique_profiles')

  logging.info(profile_list)
  logging.info(user.key)
  logging.info(user)
  logging.info(user.key.id())

  stripped_profiles = get_stripped_profiles(profile_list)

  logging.info('got stripped_profiles')

  new_profiles_to_add = []

  for profile in stripped_profiles:
    if not ProfileList.get_by_id(str(user.key.id()) + '|' + profile):
      new_profile = ProfileList(
        parent = user.key,
        id = str(user.key.id()) + '|' + profile,
        user_key = user.key,
        profile = profile,
        visited = False)
      new_profiles_to_add.append(new_profile)

  ndb.put_multi(new_profiles_to_add)


  # to_be_visited = ToBeVisited.query(ancestor=user.key).get()

  # logging.info('got to_be_visited')
  # logging.info(to_be_visited)

  # if to_be_visited is not None:
  #   existing_profiles = to_be_visited.profiles
  #   for profile in stripped_profiles:
  #     if profile not in existing_profiles:
  #       existing_profiles.append(profile)
  #   to_be_visited.profiles = existing_profiles

  # else:
  #   to_be_visited = ToBeVisited(parent=user.key,
  #                               profiles=stripped_profiles)

  # to_be_visited.put()
