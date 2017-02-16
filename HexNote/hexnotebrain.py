import time
import logging
import threading
from resthandler import RESTHandler
from random import randint
from speechhandler import SpeechHandler

# The main driver for decision making
class HexNoteBrain:
	# Constants
	LOWER_SLEEP_LIMIT = 22932 # Lets keep chat light while it's simple
	UPPER_SLEEP_LIMIT = 133200
	HOUR_LIMIT = 3600
	AUTH_ATTEMPT_MAX = 3 # Limit auth attempts to 3 for now
	MINUTE = 60

	# ctor
	def __init__(self):
		logging.info('Creating the brain')
		# start by getting our API handler up and running
		self.lock = threading.RLock()
		self.handler = RESTHandler()
		self.speech = SpeechHandler()
		self.run = True
		# Start Main loop daemon thread
		logging.info('Starting main loop thread')
		mlThread = threading.Thread(name='MainSpeechThread', target=self.main_loop)
		mlThread.daemon = True
		mlThread.start()
		# Start mention repsonse daemon thread
		mentionThead = threading.Thread(name='MentionThread', target=self.mention_loop)
		mentionThead.daemon = True
		mentionThead.start()
		
	# Main processing loop
	# We'll wait some length of time then decide if we want to talk to someone
	def main_loop(self):
		logging.info('Start the main loop')
		# Check to see if an outside source has changed run
		while self.run:
			# Check for valid creds, set run to false if they do not pass muster.
			self.run = self.creds_valid()
			if self.run:
				saying = self.get_saying()	
				# With the tweet composed, send it out
				localtime = time.asctime( time.localtime(time.time()) )
				logging.info(saying + ' at %s' % localtime)
				#self.handler.update_status(saying)
				# Go to sleep, wake up at some point
				sleep_time = randint(self.LOWER_SLEEP_LIMIT, self.UPPER_SLEEP_LIMIT)
				sleep_time_min = sleep_time / self.MINUTE
				logging.info('Going to sleep for %d min' % sleep_time_min)
				time.sleep(sleep_time)
			else:
				logging.critical('There was a major issue - shutting down')
	
	# Mentions loop
	# Respond to mentions that have happened since the last response
	def mention_loop(self):
		logging.info('Start the mention loop')
		while self.run:
			self.run = self.creds_valid()
			if self.run:
				# Check for most recent mentions, pick one to respond to
				# Check if hex, if not, respond with 'what?' in hex
				self.handler.get_mentions()
				# Go to sleep, wake up at some point
				sleep_time_min = self.HOUR_LIMIT / self.MINUTE
				logging.info('Going to sleep for %d min' % sleep_time_min)
				time.sleep(self.HOUR_LIMIT)
	
	# Verify that creditials are valid still
	def creds_valid(self):
		# Verify our creds or establish new creds if needed
		with self.lock:
			auth_attempt = 1
			while not self.handler.verify_credentials():
				# Make sure we don't just hammer the auth server
				if auth_attempt > self.AUTH_ATTEMPT_MAX:
					logging.critical('Unable to fetch valid credentials')
					return False
				logging.Warning('Issue with credentials - attempting to fix')
				# Issue with the OAuth Creds, recreate RESTHandler to fix
				self.handler = None
				self.handler = RESTHandler()
				auth_attempt += 1
			# If creds are valid return true
			return True
	
	# Gets a saying for the main speech loop
	def get_saying(self):
		# Do you want to talk to someone?
		# Lets be a bit more introverted
		text = ''
		coin = randint(0,4)
		if coin < 4:
			# Say something to Twitterverse
			logging.info('Talking to myself')
			text = self.speech.speak()
		else:
			# Say something to a random someone
			logging.info('Talking to someone')
			query = self.handler.get_trend_query()
			user = self.handler.get_tweet_user(query)
			logging.info('Talking to %s' % user)
			text = self.speech.speak(user)
		return text
