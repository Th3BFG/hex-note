import json
import logging
from oauthhandler import OAuthHandler
from random import randint

# Responsible for making REST calls to Twitter API
class RESTHandler:
	# End point for REST calls
	# TODO: Should I clarify GET/POST in name?
	PLACES_EP = "https://api.twitter.com/1.1/trends/place.json?id="
	VERIFY_CREDS_EP = "https://api.twitter.com/1.1/account/verify_credentials.json"

	# Constants
	GLOBAL_WOEID = 1 # I'll grab trends from a global perspective for now
	JSON_DATA_INDEX = 0 # I have a feeling that Twitter nests most of its response data
	HTTP_SUCCESS = '200'
	TRENDS_KEY = 'trends'
	PROMOTED_CONTENT_KEY = 'promoted_content'
	NAME_KEY = 'name'
	NONE_STR = 'None'
	URL_KEY = 'url'
	STATUS_KEY = 'status'

	# ctor
	def __init__(self):
		logging.info('Creating RESTHandler');
		# Attempt to get OAuth Client
		self.oauthhandler = OAuthHandler()		
		if(self.verify_credentials()):
			logging.info('OAuth Client created successfully')
		else:
			logging.critical('Unable to birth OAuth Client')
	
	# Gets a list of trends, picks a random one and returns the url
	def get_trend_url(self):
		places_ep = self.PLACES_EP + str(self.GLOBAL_WOEID)
		logging.info('Attempting to get list of places from ' + places_ep)
		resp, data = self.oauthhandler.client.request(places_ep)
		jsonData = json.loads(data)
		# With the list of trends, pick a random index
		trends = jsonData[self.JSON_DATA_INDEX][self.TRENDS_KEY]
		numTrends = len(trends)
		logging.info('Grabbing random trend')
		rndIndex = randint(0, numTrends - 1)
		trend = trends[rndIndex]
		logging.info('Getting tweets for %s' % trend[self.NAME_KEY])
		return trend[self.URL_KEY]
		
	# Used to verify that our credentials are still authorized
	def verify_credentials(self):
		logging.info('Attempting to verify credentials')
		resp, data = self.oauthhandler.client.request(self.VERIFY_CREDS_EP)
		if resp[self.STATUS_KEY] == self.HTTP_SUCCESS:
			return True
		else:
			return False
