from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()

prompt = '> '

def analyze(inputText):
	response = alchemyapi.sentiment("text", inputText)
	print "Sentiment: ", response["docSentiment"]["type"]

print "Hi! Please enter a statement for me to process:"
myText = raw_input(prompt)
analyze(myText)
