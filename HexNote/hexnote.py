import logging
import oauthhandler

# Main entry point for Hex Note
def main():
	# start our log with INFO enabled.
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
	logging.info('Starting Hex Note')
	# Attempt to get OAuth Client
	oauthhandler = oauthhandler.oauthhandler()
	if(oauthhandler.client is None):
		logging.critical('Unable to birth OAuth Client')
	else:
		logging.info('Starting Hex Note Main Process')
		# start making requests and shit
		# take in logging level from command line param
	
if __name__ == '__main__':
	main()