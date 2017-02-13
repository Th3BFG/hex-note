import sys
import logging
import threading
from optparse import OptionParser
from hexnotebrain import HexNoteBrain

# Main entry point for Hex Note
def main():
	# Set up args parsing
	parser = OptionParser()
	parser.add_option("-l", "--log", dest="loglevel", default="WARNING",
					help="Set the logging level to LVL - Options: INFO, WARNING, ERROR", metavar="LVL")
	(options, args) = parser.parse_args()
	# start log
	logLvl = options.loglevel
	logging.basicConfig(format='[%(levelname)s](%(threadName)-10s):%(message)s', level=get_log_lvl(logLvl))
	#Start up Hex Note Daemon
	dThread = create_hn_daemon()
	dThread.start()
	# Listen for stop command on main thread
	while True:
		if raw_input() == 'stop':
			logging.info('"stop" received')
			logging.info('Shutting down Hex Note')
			sys.exit() # TODO: clean up worker thread before exiting

# Daemon to run Hex Note
def create_hn_daemon():
	logging.info('Starting Hex Note')
	thread = threading.Thread(name='BrainThread', target=HexNoteBrain)
	thread.daemon = True
	return thread
	
# Based on lvl, return enum logging level
def get_log_lvl(lvl):
	if lvl == 'INFO' or lvl == 'WARNING' or lvl == 'ERROR':
		return getattr(logging, lvl)
	else:
		# Poor formatting of lvl - set to default
		return logging.WARNING
	
if __name__ == '__main__':
	main()
