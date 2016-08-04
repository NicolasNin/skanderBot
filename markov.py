#skander-bot
import random
from getmessage import MessageForum
class Markov(object):
	""" take a list of word into input"""
	def __init__(self, liste_mot):
		self.cache = {}
		self.words = liste_mot
		self.word_size = len(self.words)
		self.database()	
	
	def triples(self):
		""" Generates triples from the given data string. So if our string were
				"What a lovely day", we'd generate (What, a, lovely) and then
				(a, lovely, day).
		"""
		if len(self.words) < 3:
			return
		
		for i in range(len(self.words) - 2):
			yield (self.words[i], self.words[i+1], self.words[i+2])
			
	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]
				
	def generate_markov_text(self, size=25):
		seed = random.randint(0, self.word_size-3)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
		gen_words = []
		for i in range(size):
			gen_words.append(w1)
			w1, w2 = w2, random.choice(self.cache[(w1, w2)])
		gen_words.append(w2)
		return ' '.join(gen_words)

def main():
	print("testing with skander")
	skanderMsg=MessageForum("Skander")
	#we retrieve message and compute concatenated words for the markoc class
	skanderMsg.retrieveAllMsg()
	skanderMsg.createWordList()
	skanderMarkov=Markov(skanderMsg.getWordList())
	#we test
	print(skanderMarkov.generate_markov_text())

if __name__=='__main__':
	main()
