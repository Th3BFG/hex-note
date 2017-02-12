import logging
import binascii
from random import randint

class SpeechHandler:
	# I'm going to need to define a grammar. I can't decide if I want to stick to a tree or CFG.
	#SECONDARY_NOUN = {'you'}
	PLURAL_NOUN = ['cars', 'computers', 'peaches', 'pies', 'feelings', 'people', 'money']
	PLURAL_PRESENT_VERB = ['are', 'makes', 'causes', 'uses', 'eats', 'steals']
	START = ['What']
	SENTENCE = [START, PLURAL_PRESENT_VERB, PLURAL_NOUN]
	
	# ctor
	def __init__(self):
		logging.info('Starting up speech center')
		
	# From the defined grammar, pick something to say and return it
	def speak(self):
		logging.info('Decide what to say')
		s = ''
		firstWord = True
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
		
