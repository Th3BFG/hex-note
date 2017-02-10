import json
import logging

# Responsible for making REST calls to Twitter API
class RestHandler:
	

	# ctor
	def __init__(self, client):
		logging.info('Creating REST Handler');
		self.client = client
		
	
		