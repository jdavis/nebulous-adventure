#!/usr/bin/env python
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

from flask import Flask

from google.appengine.ext.webapp.util import run_wsgi_app

from base import urls as base_urls

app = Flask(__name__)

#
# Settings
#

# TODO: Make static for deployment
SECRET_KEY = 'this_is_our_secret_key'

#
# App Settings
#

base_urls.apply_urls(app)
app.secret_key = SECRET_KEY

if __name__ == '__main__':
    run_wsgi_app(app)
