# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import filters
import webapp2
from webapp2 import Route


DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

routes = [
    # Testing
    Route('/try-pw', handler='frontend.TryPw', name='try-pw'),

    # API
    Route('/api/is-crawling', handler='frontend.IsCrawling', name='is-crawling'),
    Route('/api/profiles', handler='frontend.GetProfileList', name='profile-list'),
    Route('/api/profile-queue', handler='frontend.ToBeVisited', name='to-be-visited'),
    Route('/api/user-info', handler='frontend.UserInfo', name='user-info'),

    # Pages
    Route('/add-okcupid', handler='frontend.AddOkcupid', name='add-okcupid'),
    Route('/getlist', handler='frontend.GetList', name='getlist'),
    Route('/home', handler='frontend.Home', name='home'),
    Route('/', handler='frontend.Index', name='index'),

    # Task queue
    Route('/crawlstarter/<num:\d+>', handler='frontend.CrawlStarter', name='crawl-starter'),
    Route('/crawlworker', handler='frontend.CrawlWorker', name='crawl-worker'),

    # User registration
    Route('/signup', handler='frontend.SignupHandler'),
    Route('/login', handler='frontend.LoginHandler', name='login'),
    Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
      handler='frontend.VerificationHandler', name='verification'),
    Route('/password', 'frontend.SetPasswordHandler'),
    Route('/logout', 'frontend.LogoutHandler', name='logout'),
    Route('/forgot', 'frontend.ForgotPasswordHandler', name='forgot'),
    Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>', handler='frontend.VerificationHandler', name='verification'),
    ]

config = {
    'webapp2_extras.jinja2': {
        'template_path': 'dist',
        'filters': {
            'timesince': filters.timesince,
            'datetimeformat': filters.datetimeformat,
        },
        'environment_args': {
            'variable_start_string': '((',
            'variable_end_string': '))',
        },
    },
    'webapp2_extras.auth': {
        'user_model': 'models.User',
        'user_attributes': ['email_address', 'auth_ids']
    },
    'webapp2_extras.sessions': {
        'secret_key': 'YOUR_SECRET_KEY',
    },
}

application = webapp2.WSGIApplication(routes, debug=DEBUG, config=config)
