import logging
from hexnotebrain import HexNoteBrain

# Main entry point for Hex Note
def main():
	# TODO: take logging level from cmd line arg
	# start our log with INFO enabled.
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
	logging.info('Starting Hex Note')
	brain = HexNoteBrain()
	
if __name__ == '__main__':
	main()