import logging
import ConfigParser
from collections import namedtuple
		
# User Configuration Handler
class ConfigHandler:
	# Some Config Constants
	CONSUMER_KEY = 'CONSUMER_KEY'
	CONSUMER_SECRET = 'CONSUMER_SECRET'
	ACCESS_KEY = 'ACCESS_KEY'
	ACCESS_SECRET = 'ACCESS_SECRET'

	def __init__(self):
		settings = self.get_config()
		if(settings != None):
			self.cKey = settings.cKey
			self.cSecret = settings.cSecret
			self.aKey = settings.aKey
			self.aSecret = settings.aSecret
		else:
			logging.critcal('Configuration retrieval has failed.')
		
	# Gets settings out of the config file
	def get_config(self):
		config = ConfigParser.SafeConfigParser()
		logging.info('Attempting to read app.cfg')
		try:
			config.read('app.cfg')
			Config = namedtuple('Config', 'cKey cSecret aKey aSecret')
			cK = config.get('Consumer Info', self.CONSUMER_KEY)
			cS = config.get('Consumer Info', self.CONSUMER_SECRET)
			aK = config.get('Access Info', self.ACCESS_KEY)
			aS = config.get('Access Info', self.ACCESS_SECRET)
			logging.info('Config read, returning data')	
			return Config(cKey = cK, cSecret = cS, aKey = aK, aSecret = aS)
		except (ConfigParser.Error):
			logging.error("There was an error reading your configuration.")