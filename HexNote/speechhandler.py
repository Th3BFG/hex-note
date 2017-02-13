import logging
import binascii
from random import randint

class SpeechHandler:
	# TODO: Do this right. I'll need to research grammars a bit and flesh this out.
	#SECONDARY_NOUN = {'you'}
	#PUNCTUATION = ['?']
	PLURAL_NOUN = ['cars', 'computers', 'peaches', 'pies', 'feelings', 'people', 'money']
	PLURAL_PRESENT_VERB = ['are', 'makes', 'causes', 'uses', 'eats', 'steals']
	START = ['What']
	SENTENCE = [START, PLURAL_PRESENT_VERB, PLURAL_NOUN]
	
	# ctor
	def __init__(self):
		logging.info('Starting up speech center')
		
	# From the defined grammar, pick something to say and return it
	def speak(self, user=None):
		logging.info('Decide what to say')
		s = ''
		firstWord = True
		# Account for username - simply add it to the front for now
		if user != None:
			s += '@%s ' % user
		# Loop through the parts and construct the sentence
		for part in self.SENTENCE:
			if firstWord:
				firstWord = False
			else:
				s += ' '
			length = len(part)
			rndIndex = randint(0, length)
			result = part[rndIndex - 1]
			s += result
		s += '?' # Questions for now
		logging.info(s)
		# Convert the saying to hex as is tradition
		hexStr = binascii.hexlify(s)
		return hexStr
		
