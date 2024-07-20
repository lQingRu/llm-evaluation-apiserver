import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

try:
    ELASTICSEARCH_USERNAME = os.environ["ELASTICSEARCH_USERNAME"]
except KeyError:
    ELASTICSEARCH_USERNAME = None

try:
    ELASTICSEARCH_PASSWORD = os.environ["ELASTICSEARCH_PASSWORD"]
except KeyError:
    ELASTICSEARCH_PASSWORD = None

try:
    ELASTICSEARCH_URL = os.environ["ELASTICSEARCH_URL"]
except KeyError:
    ELASTICSEARCH_URL = None

try:
    ELASTICSEARCH_SSL_VERIFY = os.environ["ELASTICSEARCH_SSL_VERIFY"]
except KeyError:
    ELASTICSEARCH_SSL_VERIFY = False

try:
    ELASTICSEARCH_DATABASE_INDEX = os.environ.get("ELASTICSEARCH_DATABASE_INDEX")
except KeyError:
    ELASTICSEARCH_DATABASE_INDEX = None

try:
    HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
except KeyError:
    HUGGINGFACEHUB_API_TOKEN = None

try:
    DEPLOYMENT_ENV = os.environ["DEPLOYMENT_ENV"]
except KeyError:
    DEPLOYMENT_ENV = "DEVT"
