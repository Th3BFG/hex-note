import oauth2 as oauth
import logging
from confighandler import ConfigHandler

# The following class is responsible for creating an OAuth1 Client
class OAuthHandler:
	# ctor
	def __init__(self):
		logging.info('Creating OAuthHandler')
		self.config = ConfigHandler()
		if(self.config is not None):
			self.create_client()
			
	# Attempts to create a client with twitter
	def create_client(self):
		consumer = oauth.Consumer(key=self.config.cKey, secret=self.config.cSecret)
		access_token = oauth.Token(key=self.config.aKey, secret=self.config.aSecret)
		logging.info('Attempting to create OAuth Client')
		self.client = oauth.Client(consumer, access_token)
		