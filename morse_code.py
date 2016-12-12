__author__ = "Steve Wilson"

DOT = 1
DASH = 2
SPACE = 3
LETTER = 4
WORD = 5
END = 10

textToCode = {
  'A' : (DOT, DASH),
  'B' : (DASH, DOT, DOT, DOT),
  'C' : (DASH, DOT, DASH, DOT),
  'D' : (DASH, DOT, DOT),
  'E' : (DOT,),
  'F' : (DOT, DOT, DASH, DOT),
  'G' : (DASH, DASH, DOT),
  'H' : (DOT, DOT, DOT, DOT),
  'I' : (DOT, DOT),
  'J' : (DOT, DASH, DASH, DASH),
  'K' : (DASH, DOT, DASH),
  'L' : (DOT, DASH, DOT, DOT),
  'M' : (DASH, DASH),
  'N' : (DASH, DOT),
  'O' : (DASH, DASH, DASH),
  'P' : (DOT, DASH, DASH, DOT),
  'Q' : (DASH, DASH, DOT, DASH),
  'R' : (DOT, DASH, DOT),
  'S' : (DOT, DOT, DOT),
  'T' : (DASH,),
  'U' : (DOT, DOT, DASH),
  'V' : (DOT, DOT, DOT, DASH),
  'W' : (DOT, DASH, DASH),
  'X' : (DASH, DOT, DOT, DASH),
  'Y' : (DASH, DOT, DASH, DASH),
  'Z' : (DASH, DASH, DOT, DOT),
  '1' : (DOT, DASH, DASH, DASH, DASH),
  '2' : (DOT, DOT, DASH, DASH, DASH),
  '3' : (DOT, DOT, DOT, DASH, DASH),
  '4' : (DOT, DOT, DOT, DOT, DASH),
  '5' : (DOT, DOT, DOT, DOT, DOT),
  '6' : (DASH, DOT, DOT, DOT, DOT),
  '7' : (DASH, DASH, DOT, DOT, DOT),
  '8' : (DASH, DASH, DASH, DOT, DOT),
  '9' : (DASH, DASH, DASH, DASH, DOT),
  '0' : (DASH, DASH, DASH, DASH, DASH)
 }
 
 
codeToText = {}
 
for text in textToCode:
	codeToText[textToCode[text]] = text

DOT_LENGTH = 1
DASH_LENGTH = 3
LENGTH_BETWEEN_LETTER_UNITS = 1
LENGTH_BETWEEN_LETTERS = 3
LENGTH_BETWEEN_WORDS = 7

def encodeWord(text):
	cypherText = []
	for i in range(0,len(text)):
		letter = text[i]
		try:
			value = textToCode[letter.upper()]
		except KeyError as e:
			continue
	
		cypherText.append(value)
	
	return cypherText

# End encodeWord


def decodeWord(cypherText):
	text = []
	for code in cypherText:
		try:
			value = codeToText[code]
		except KeyError as e:
			continue
		
		text.append(value)
	
	theText = ''
	for letter in text:
		theText += letter
	
	return theText

# End decodeWord


def encodePhrase(phrase):
	phrases = phrase.split(' ')
	encodedPhrases = []
	
	for segment in phrases:
		encodedPhrases.append(encodeWord(segment))
	
	return encodedPhrases

# end encodePhrase


def decodePhrase(segment):
	phrase = []
	for item in segment:
		phrase.append(decodeWord(item))

	theText = ''
	
	for i in range(0,len(phrase)):
		theText += phrase[i]
		if i < (len(phrase) - 1):
			theText += " "
	
	return theText

# End decodePhrase


class SignalHandler(object):
	
	def __init__(self):
		
		self.__buffer = ""
	
	# End __init__
	
	
	def dot(self, t):
		
		self.__buffer += '.' * t
	
	# End dot
	
	
	def dash(self, t):
		
		self.__buffer += '-' * t
	
	# End dash
	
	
	def space(self, t):
		
		self.__buffer += ' ' * t
	
	# End space
	
	
	def reset(self):
		
		self.__buffer = ''
	
	# End reset
	
	
	@property
	def buffer(self):
		return self.__buffer
	
	# End buffer

# End SignalHandler



def sendMessage(phrase, delta, handler=SignalHandler()):

	global DOT
	global DASH

	cypherText = encodePhrase(phrase)
	
	for i in range(0, len(cypherText)):

		word = cypherText[i]
		
		for j in range(0, len(word)):
			
			codedLetter = word[j]
			
			for k in range(0, len(codedLetter)):
				
				code = codedLetter[k]
				
				if code == DOT:
					handler.dot(delta * DOT_LENGTH)
				elif code == DASH:
					handler.dash(delta * DASH_LENGTH)
				
				if k < (len(codedLetter) - 1):
					handler.space(delta * LENGTH_BETWEEN_LETTER_UNITS)
			
			if j < (len(word) - 1):
				handler.space(delta * LENGTH_BETWEEN_LETTERS)
		
		if i < (len(cypherText) - 1):
			handler.space(delta * LENGTH_BETWEEN_WORDS)

# End sendMessage


def readMessage(delta, reader):
	
	letter = []
	word = []
	phrase = []

	inCode = SPACE
	
	generator = reader.read(delta)
	
	inCode = generator.next()

	while inCode != END:
		
		if inCode == DASH or inCode == DOT:
			letter.append(inCode)
		elif inCode == LETTER:
			word.append(tuple(letter))
			letter = []
		elif inCode == WORD:
			phrase.append(word)
			word = []
			letter = []
	
		inCode = generator.next()

	return decodePhrase(phrase)
	
# End readMessage

