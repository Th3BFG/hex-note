import time
import logging
from resthandler import RESTHandler
from random import randint

# The main driver for decision making
class HexNoteBrain:
	# Constants
	LOWER_SLEEP_LIMIT = 36000 # Lets keep chat light while it's simple
	UPPER_SLEEP_LIMIT = 133200

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
		while True:
			# Do you want to talk to someone?
			# flip a coin for now
			coin = randint(0,1)
			if coin == 0: #tails - stay alone
				# Say something to Twitterverse
				logging.info('Talking to myself')
				url = get_trend_url(self)
				# pick a random post from the url
				# use them for the tweet
				# create a speechhandler after that
			else:
				# Say something to a random someone
				logging.info('Talking to someone')
				url = self.handler.get_trend_url()
			# Go to sleep, wake up at some point
			logging.info('Going to sleep')
			sleep_time = randint(self.LOWER_SLEEP_LIMIT, self.UPPER_SLEEP_LIMIT)
			time.sleep(sleep_time)
			# Verify credentials, reconnect if needed.
