import numpy as np 

import tensorflow_datasets as tfds
import tensorflow as tf 

tfds.disable_progress_bar()

import matplotlib.pyplot as plt 

import math
from textblob import TextBlob
from urllib.request import urlopen as uReq
import requests
from bs4 import BeautifulSoup
def plot_graphs(history, metric): 
	plt.plot(history.history[metric])
	plt.plot(history.history['val_'+metric],'')
	plt.xlabel("Epochs")
	plt.ylabel(metric)
	plt.legend([metric, 'val_'+metric])

dataset, info = tfds.load('imdb_reviews', with_info=True, as_supervised=True)
train_dataset, test_dataset = dataset['train'], dataset['test']

train_dataset.element_spec
for example, label in train_dataset.take(1):
  print('text: ', example.numpy())
  print('label: ', label.numpy())

VOCAB_SIZE = 1000
encoder = tf.keras.layers.experimental.preprocessing.TextVectorization(
    max_tokens=VOCAB_SIZE)
encoder.adapt(train_dataset.map(lambda text, label: text))

vocab = np.array(encoder.get_vocabulary())
vocab[:20]

encoded_example = encoder(example)[:3].numpy()

encoded_example

model = tf.keras.Sequential([
    encoder,
    tf.keras.layers.Embedding(
        input_dim=len(encoder.get_vocabulary()),
        output_dim=64,
        # Use masking to handle the variable sequence lengths
        mask_zero=True),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])
print([layer.supports_masking for layer in model.layers])

sample_text = ('The movie was cool. The animation and the graphics '
               'were out of this world. I would recommend this movie.')
predictions = model.predict(np.array([sample_text]))
print(predictions[0])
padding = "the " * 2000
predictions = model.predict(np.array([sample_text, padding]))
print(predictions[0])
def getPostInformation(url):
	site = requests.get(url)
	soup = BeautifulSoup(site.content, 'html.parser')
	# postList = [ 
	# 	["No social distancing on the tours. Elevators and queues lined up for the elevator are packed like sardines. No cleaning being done. No staff to enforce mask rules. It’s a madhouse. Do not go until they limit the tours to only a few people in the elevators at a time and have some barriers between people. Unsafe. It’s really shocking that an icon of this magnitude doesn’t have some sort of plan in place for Covid 19! Beware", 45, 2],
	# 	["A must do in Paris. I am not sure if I would do it again. However, you have to go at least once in your life", 890, 267],
	# 	["Eiffel tower beautiful as ever, however covid rules were impossible to follow. We had booked our tickets in advance assuming there was some limitation on visitors. However nothing like it. In the queue to the summit it was impossible to keep 1.5 metres distance. Stickers on the floor are not enough. Even when keeping distance to the person in front of you, the people on the other side of the seperation bar were less than 1 metre away. Same in elevators (way too many people in one elevator). It seems that the management does not care, as long as they keep selling tickets. No cleaners seen at any point in time. We felt very uncomfortable and it's shocking that such a world renowned monument doesn't take safety seriously. The Eiffel tower could become a serious source of infections.", 6, 8],
	# 	["Amazing landmark. Happy to see the care and respect all people give to this amazing landmark", 8, 0],
	# 	["Amazing views and enjoyed my glass of champagne at the top. Social distancing was rubbish and I didn't see any hand sanitising stations. There were lots of people and they were letting too many people in the lifts and around the bases. Disappointing.", 16, 3]
	# ]
	results = soup.find(id="component_19")
	results.prettify()
	return postList

def getSentimentScore(post):
	content = TextBlob(post)
	polarityScore = content.sentiment.polarity
	return polarityScore * 100
def getMagnitudeScore(contributions, helpful_votes):

	mag = 1
	if contributions >= 6:
		mag *= math.log(contributions, 6)
	if helpful_votes >= 4:
		mag *= math.log(helpful_votes, 4)
	return mag

def analyze(phrases):
	sentiments = []
	for phrase in phrases:
		if phrase is None:
			sentiments.append(0)
			print('None')
			continue
		sentiment = getSentimentScore(phrase)
		sentiments.append(sentiment)
		print(sentiment)
	return sentiments 

phrases = ["I gotta say, Clive Barker's Undying is by far the best horror game to have ever been made. I've played Resident Evil, Silent Hill and the Evil Dead and Castlevania games but none of them have captured the pure glee with which this game tackles its horrific elements. Barker is good at what he does, which is attach the horror to our world, and it shows as his hand is clearly everywhere in this game. Heck, even his voice is in the game as one of the main characters.", "This is the kind of film for a snowy Sunday afternoon when the rest of the world can go ahead with its own business as you descend into a big arm-chair and mellow for a couple of hours. Wonderful performances from Cher and Nicolas Cage (as always) gently row the plot along. There are no rapids to cross, no dangerous waters, just a warm and witty paddle through New York life at its best. A family film in every sense and one that deserves the praise it received.", "In Stand By Me, Vern and Teddy discuss who was tougher, Superman or Mighty Mouse. My friends and I often discuss who would win a fight too. Sometimes we get absurd and compare guys like MacGyver and The Terminator or Rambo and Matrix. But now it seems that we discuss guys like Jackie Chan, Bruce Lee and Jet Li. It is a pointless comparison seeing that Lee is dead, but it is a fun one. And if you go by what we have seen from Jet Li in Lethal 4 and Black Mask, you have to at least say that he would match up well against Chan. In this film he comes across as a martial arts God"]
analyze(phrases);
