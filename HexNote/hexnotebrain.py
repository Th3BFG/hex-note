import time
import logging
from resthandler import RESTHandler
from random import randint

# The main driver for decision making
class HexNoteBrain:
	# Constants
	LOWER_SLEEP_LIMIT = 36000 # Lets keep chat light while it's simple
	UPPER_SLEEP_LIMIT = 133200
	AUTH_ATTEMPT_MAX = 2 # Limit auth attempts to 3 for now

	# ctor
	def __init__(self):
		logging.info('Creating the brain')
		# start by getting our API handler up and running
		self.handler = RESTHandler()
		# Start main decision
		self.start_main_loop()		
		
	# Main processing loop
	# We'll wait some length of time then decide if we want to talk to someone
	def start_main_loop(self):
		logging.info('Start the main loop')
		run = True
		while run:
			# Verify our creds or establish new creds if needed
			auth_attempt = 0
			while self.handler.verify_credentials() != True:
				# Make sure we don't just hammer the auth server
				if auth_attempt > AUTH_ATTEMPT_MAX:
					logging.critical('Unable to fetch valid credentials')
					run = False
					break
				logging.Warning('Issue with credentials - attempting to fix')
				# Issue with the OAuth Creds, recreate RESTHandler to fix
				self.handler = None
				self.handler = RESTHandler()
				auth_attempt += 1
			if run:
				# Do you want to talk to someone?
				# flip a coin for now
				coin = randint(0,1)
				if coin == 0: #tails - stay alone
					# Say something to Twitterverse
					logging.info('Talking to myself')
				else:
					# Say something to a random someone
					logging.info('Talking to someone')
					query = self.handler.get_trend_query()
					logging.info(self.handler.get_tweet_user(query))
					# use them for the tweet
					# create a speechhandler after that
				# Go to sleep, wake up at some point
				logging.info('Going to sleep')
				sleep_time = randint(self.LOWER_SLEEP_LIMIT, self.UPPER_SLEEP_LIMIT)
				time.sleep(sleep_time)
			else:
				logging.critical('There was a major issue - shutting down')
