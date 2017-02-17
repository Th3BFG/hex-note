import json
import logging
import urllib
import threading
from confighandler import ConfigHandler
from oauthhandler import OAuthHandler
from random import randint

# Responsible for making REST calls to Twitter API
class RESTHandler:
	# End points for REST calls
	PLACES_EP = "https://api.twitter.com/1.1/trends/place.json?id=" #GET
	VERIFY_CREDS_EP = "https://api.twitter.com/1.1/account/verify_credentials.json" #GET
	UPDATE_STATUS_EP = "https://api.twitter.com/1.1/statuses/update.json?status=" #POST
	QUERY_SEARCH_EP = "https://api.twitter.com/1.1/search/tweets.json?q=" #GET
	MENTIONS_EP = "https://api.twitter.com/1.1/statuses/mentions_timeline.json?count=" #GET

	# Constants
	GLOBAL_WOEID = 1 # I'll grab trends from a global perspective for now
	JSON_DATA_INDEX = 0 # I have a feeling that Twitter nests most of its response data
	MAX_TWEET_LEN = 140
	MAX_MENTIONS = 10 # Number of mentions to get at one time
	TWEET_SEARCH_LIMIT = "&count=20" # Additional, optional parameter for Query Search to limit returned tweets
	HTTP_SUCCESS = '200'
	TRENDS_KEY = 'trends'
	PROMOTED_CONTENT_KEY = 'promoted_content'
	NAME_KEY = 'name'
	NONE_STR = 'None'
	QUERY_KEY = 'query'
	STATUS_KEY = 'status'
	STATUSES_KEY = 'statuses'
	SCREEN_NAME_KEY = 'screen_name'
	USER_KEY = 'user'
	SINCE_ID_KEY = '&since_id='
	ID_KEY = 'id'
	TEXT_KEY = 'text'

	# ctor
	def __init__(self):
		logging.info('Creating RESTHandler');
		self.lock = threading.RLock()
		self.since_id = None
		# Get Config and set since_id
		self.config = ConfigHandler()
		self.since_id = self.config.mention_id()
		# Attempt to get OAuth Client
		self.oauthhandler = OAuthHandler(self.config)		
		if(self.verify_credentials()):
			logging.info('OAuth Client created successfully')
		else:
			logging.critical('Unable to birth OAuth Client')
	
	# Gets a list of mentions and will use the since_id if it exists
	def get_user_from_mention(self):
		logging.info('Attempting to get list of mentions')
		mentions_ep = self.MENTIONS_EP +str(self.MAX_MENTIONS)
		# if a since_id exists, attach it
		if self.since_id is not None and self.since_id != '':
			logging.info('since_id found: %s' % self.since_id)
			mentions_ep += self.SINCE_ID_KEY + str(self.since_id)
		logging.info('Getting mentions at %s' % mentions_ep)
		# With the constructed endpoint, make the callable
		resp, data = self.get_request(mentions_ep)
		if self.resp_success(resp[self.STATUS_KEY]):
			mentions_data = json.loads(data)
			# Pick a mention out of the list
			numMentions = len(mentions_data)
			if numMentions > 0:
				logging.info('Grabbing random mention')
				rndIndex = randint(0, (numMentions - 1))
				mention = mentions_data[rndIndex]
				logging.info('id: %s' % mention[self.ID_KEY])
				self.config.set_value(self.config.MENTION_SECTION, self.config.MENTION_ID, str(mention['id']))
				logging.info('mention: %s' % mention[self.TEXT_KEY])
				logging.info(mention)
				return None
			else:
				logging.info('No mentions were found')
				return None
		else:
			logging.error('There was an issue fetching the list of mentions')
			return None
			
	# Gets a list of trends, picks a random one and returns the query
	def get_trend_query(self):
		# Take lock to do work
		with self.lock:
			places_ep = self.PLACES_EP + str(self.GLOBAL_WOEID)
			logging.info('Attempting to get list of places from ' + places_ep)
			resp, data = self.get_request(places_ep)
			if self.resp_success(resp[self.STATUS_KEY]):
				jsonData = json.loads(data)
				# With the list of trends, pick a random index
				trends = jsonData[self.JSON_DATA_INDEX][self.TRENDS_KEY]
				numTrends = len(trends)
				if numTrends > 0:
					logging.info('Grabbing random trend')
					rndIndex = randint(0, (numTrends - 1))
					trend = trends[rndIndex]
					logging.info('Getting tweets for %s' % trend[self.NAME_KEY])
					return trend[self.QUERY_KEY]
				else:
					logging.error('No trends were returned')
					return None
			else:
				logging.error('There was an issue getting the list of locales')
				return None
					
	# From the trend query, select a random tweet. Return the user who posted it
	def get_tweet_user(self, query):
		# Take lock to do work
		with self.lock:
			logging.info('Attempting to get list of tweets for trend')
			tweets_ep = self.QUERY_SEARCH_EP + query + self.TWEET_SEARCH_LIMIT
			resp, data = self.get_request(tweets_ep)
			if self.resp_success(resp[self.STATUS_KEY]):
				tweet_data = json.loads(data)
				tweets = tweet_data[self.STATUSES_KEY]
				logging.info('Selecting a random tweet')
				numTweets = len(tweets)
				if numTweets > 0:
					rndIndex = randint(0, numTweets - 1)
					tweet = tweets[rndIndex]
					logging.info('Grabbing user info')
					user = tweet[self.USER_KEY]
					user_sn = user[self.SCREEN_NAME_KEY]
					return user_sn
				else:
					logging.warmomg('No tweets were returned')
					return None
			else:
				logging.error('There was an issue fetching the list of tweets')
				return None
	
	# Updates status with a tweet. Takes in the status.	
	def update_status(self, status):
		# Take lock to do work
		with self.lock:
			# Verify that status is under 140 characters
			if len(status) <= self.MAX_TWEET_LEN:
				status_ep = self.UPDATE_STATUS_EP + status
				logging.info('Attempting to post tweet')
				resp, data = self.post_request(status_ep, status)
				if self.resp_success(resp[self.STATUS_KEY]):
					logging.info('Post successful')
				else:
					logging.error('There was an error posting the tweet')
			else:
				logging.error('Tweet is too long to post')
	
	# Used to verify that our credentials are still authorized
	def verify_credentials(self):
		logging.info('Attempting to verify credentials')
		resp, data = self.get_request(self.VERIFY_CREDS_EP)
		return self.resp_success(resp[self.STATUS_KEY])

	# Checks HTTP response code for success
	def resp_success(self, status_val):
		return status_val == self.HTTP_SUCCESS
		
	# Executes a GET request and returns the response & data
	def get_request(self, endpoint):
		return self.oauthhandler.client.request(endpoint)
	
	# Executes a POST request and returns the response & data
	def post_request(self, endpoint, post_body):
		return self.oauthhandler.client.request(
			endpoint,
			method='POST',
			body=urllib.urlencode({'status':post_body}),
			headers=None
		)
