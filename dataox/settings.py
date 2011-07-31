from __future__ import absolute_import
import os

from humfrey.settings.common import *

ENDPOINT_URL = 'http://localhost:3030/dataset/query'
GRAPH_URL = 'http://localhost:3030/dataset/data'
SERVED_DOMAINS = ('data.ox.ac.uk',)

INSTALLED_APPS += (
    'dataox.core',
    'dataox.resource',
)

ROOT_URLCONF = 'dataox.urls.empty'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

ROOT_HOSTCONF = 'dataox.hosts'
DEFAULT_HOST = 'empty'

CACHE_BACKEND = 'memcached://127.0.0.1:3031/'

EMAIL_HOST = 'smtp.ox.ac.uk'
EMAIL_PORT = 587
EMAIL_HOST_USER = config.get('email', 'user')
EMAIL_HOST_PASSWORD = config.get('email', 'password')
SERVER_EMAIL = 'dataox@opendata.nsms.ox.ac.uk'
DEFAULT_FROM_EMAIL = 'opendata@oucs.ox.ac.uk'

RESIZED_IMAGE_CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'external_images')

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
) + TEMPLATE_DIRS

THUMBNAIL_WIDTHS = (200, 400)
