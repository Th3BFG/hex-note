import os
import logging
import ConfigParser
from collections import namedtuple
		
# User Configuration Handler
class ConfigHandler:
	# Some Config Constants
	DIR_NAME = os.getcwd()
	print("******" + DIR_NAME)
	FILE_NAME = os.path.join(DIR_NAME, '/app/cfg/app.cfg')
	FILE_MODE = 'wb'
	CONSUMER_SECTION = 'Consumer Info'
	ACCESS_SECTION = 'Access Info'
	MENTION_SECTION = 'Mention Info'
	CONSUMER_KEY = 'CONSUMER_KEY'
	CONSUMER_SECRET = 'CONSUMER_SECRET'
	ACCESS_KEY = 'ACCESS_KEY'
	ACCESS_SECRET = 'ACCESS_SECRET'
	MENTION_ID = 'MENTION_ID'

	def __init__(self):
		self.config = ConfigParser.SafeConfigParser()
		self.get_config()
		
	# Gets settings out of the config file
	def get_config(self):
		logging.info('Attempting to read configuration')
		try:
			self.config.read(self.FILE_NAME)
			logging.info('Config read')	
		except (ConfigParser.Error):
			logging.error("There was an error reading your configuration")
			return None
		
	# GETTERS!!!
	def consumer_key(self):
		return self.config.get(self.CONSUMER_SECTION, self.CONSUMER_KEY)
	def consumer_secret(self):
		return self.config.get(self.CONSUMER_SECTION, self.CONSUMER_SECRET)
	def access_key(self):
		return self.config.get(self.ACCESS_SECTION, self.ACCESS_KEY)
	def access_secret(self):
		return self.config.get(self.ACCESS_SECTION, self.ACCESS_SECRET)
	def mention_id(self):
		return self.config.get(self.MENTION_SECTION, self.MENTION_ID)
		
	# Set a config values
	def set_value(self, section, option, value):
		logging.info('Updating Configuration Values')
		self.config.set(section, option, value)
		# Write changes to file
		with open(self.FILE_NAME, self.FILE_MODE) as configFile:
			self.config.write(configFile)
		