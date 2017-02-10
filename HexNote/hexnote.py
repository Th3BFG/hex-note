import logging
from resthandler import RestHandler

# Main entry point for Hex Note
def main():
	# start our log with INFO enabled.
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
	logging.info('Starting Hex Note')
	handler = RestHandler()
	handler.get_trends()
	# start making requests and shit
	# take in logging level from command line param
	
if __name__ == '__main__':
	main()