import os 
import jinja2
import logging
import webapp2

ROOT_PATH = os.path.dirname(__file__)
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.join(ROOT_PATH, 'templates')))
logging.getLogger().setLevel(logging.DEBUG)
