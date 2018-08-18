import oauth2 as oauth
import logging

# The following class is responsible for creating an OAuth1 Client
class OAuthHandler:
	# ctor
	def __init__(self, config):
		logging.info('Creating OAuthHandler')
		self.config = config
		if(self.config is not None):
			self.create_client()
			
	# Attempts to create a client with twitter
	def create_client(self):
		consumer = oauth.Consumer(key=self.config.consumer_key(), secret=self.config.consumer_secret())
		access_token = oauth.Token(key=self.config.access_key(), secret=self.config.access_secret())
		logging.info('Attempting to create OAuth Client')
		self.client = oauth.Client(consumer, access_token)
		