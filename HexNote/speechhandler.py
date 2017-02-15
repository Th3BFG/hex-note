import logging
import binascii
from random import randint

class SpeechHandler:
	# Constants
	QUESTION = 0

	# TODO: Do this right. I'll need to research grammars a bit and flesh this out.
	#SECONDARY_NOUN = {'you'}
	PUNCTUATION = ['?', '.']
	WHITESPACE = [' ']
	ADJECTIVE = ['blue', 'big', 'moist', 'far', 'high', 'lonely', 'tasty', 'old', 'younger', 'black', 'silky', 'cute', 'cool']
	PLURAL_NOUN = ['cars', 'computers', 'peaches', 'pies', 'feelings', 'people', 'money']
	PLURAL_PRESENT_VERB = ['are', 'makes', 'causes', 'uses', 'eats', 'steals']
	PERSONAL_VERB = ['am', 'run', 'taste', 'cut', 'feel']
	START = ["What", "I"]
	WHAT_S = [START[0], WHITESPACE, PLURAL_PRESENT_VERB, WHITESPACE, PLURAL_NOUN, PUNCTUATION[QUESTION]] # What
	IA_S = [START[1], WHITESPACE, PERSONAL_VERB, WHITESPACE, ADJECTIVE, PUNCTUATION] # I 
	IPN_S = [START[1], WHITESPACE, PERSONAL_VERB, WHITESPACE, PLURAL_NOUN, PUNCTUATION] # I
	IAPN_S = [START[1], WHITESPACE, PERSONAL_VERB, WHITESPACE, ADJECTIVE, WHITESPACE, PLURAL_NOUN, PUNCTUATION] # I
	SENTENCES = [WHAT_S, IA_S, IPN_S, IAPN_S]
	HEY = 'Hey'
	
	# ctor
	def __init__(self):
		logging.info('Starting up speech center')
		
	# From the defined grammar, pick something to say and return it
	def speak(self, user=None):
		logging.info('Decide what to say')
		s = ''
		# Account for username - simply add it to the front for now
		if user != None:
			logging.info('User found, adding to status')
			heyHex = binascii.hexlify(HEY)
			s += heyHex + ' @%s ' % user
		# Pick a sentence and construct it
		numSentences = len(self.SENTENCES)
		rndSentence = randint(0, (numSentences - 1))
		sentence = self.SENTENCES[rndSentence]
		res = self.construct_sentence(sentence)
		# Convert the saying to hex as is tradition
		hexStr = binascii.hexlify(res)
		s += hexStr
		logging.info(s)
		return s
		
	# Construct a sentence from the collection of its parts
	def construct_sentence(self, parts=None):
		# Loop through the parts and construct the sentence
		construct = ''
		logging.info('Beginning to construct sentence')
		for part in parts:
			result = ''
			if type(part) is list:
				length = len(part)
				if length > 0:
					rndIndex = randint(0, (length - 1))
					result = part[rndIndex]
				else:
					result = part[0]
			else:
				result = part
			# After finding the result, add it to the string
			construct += result
		# return the constructed parts
		return construct
