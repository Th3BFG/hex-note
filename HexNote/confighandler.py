import logging
import confighandler

CONSUMER_KEY = 'CONSUMER_KEY'
CONSUMER_SECRET = 'CONSUMER_SECRET'
ACCESS_KEY = 'ACCESS_KEY'
ACCESS_SECRET = 'ACCESS_SECRET'

# Gets settings out of the config file
def get_config():
	config = confighandler.Safeconfighandler()
	logging.info('Attempting to read app.cfg')
	try:
		config.read('app.cfg')
		cK = config.get('Consumer Info', CONSUMER_KEY)
		cS = config.get('Consumer Info', CONSUMER_SECRET)
		aK = config.get('Access Info', ACCESS_KEY)
		aS = config.get('Access Info', ACCESS_SECRET)
		logging.info('Config read, returning data')
		return Config(cK, cS, aK, aS)
	except (confighandler.Error):
		logging.error("There was an error reading your configuration.")
		
# Data Struct for easy listening	
class Config:
	def __init__(self, cKey, cSecret, aKey, aSecret):
		self.cKey = cKey
		self.cSecret = cSecret
		self.aKey = aKey
		self.aSecret = aSecret