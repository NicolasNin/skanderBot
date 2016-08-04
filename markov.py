#skander-bot
import random
from getmessage import MessageForum
from token_words import TokenW

#http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
class Markov(object):
	""" take a list of string into input"""
	def __init__(self, liste_string,n=2,concatenate=True,initToken=False):
		self.liste_string=liste_string
		self.key_size=n
		self.initToken=initToken
		self.token=TokenW(liste_string,n,concatenate,initToken)
		self.token.createDic()
		self.cache =self.token.dic 
	
	
	def generate_markov_text2(self,size=25):
		if 	self.initToken:
			#we choose randomly among the keys begining with the initToken ie self.token.initkeys
			#if n=1 there is only one such key (possibly repeated
			randomkey=random.choice(self.token.initkeys)
		else:
			#we choose randomly the keys among all keys
			randomkey=random.sample(self.cache.keys(),1)[0] 
		#now we can keep going by choosing a random value with this key, thus creating a new key
		key=randomkey
		gen_words=list(key)
		for i in range(size):
			try:
				print(key)
				value=random.choice(self.cache[key])
			except KeyError as e:
				print(e)
				break
			gen_words.append(value)
			key=tuple(gen_words[-1*self.key_size:])
		if self.initToken:
			gen_words.remove("START|HERE")
		return ' '.join(gen_words)	



#skmar=Markov(skm.getAllMessages(),n=2,concatenate=False,initToken=True)
#print(skmar.generate_markov_text2())
def main():
	user=input("Who do you want to generate ? \n")
	skanderMsg=MessageForum(user)
	#we retrieve message and compute concatenated words for the markoc class
	skanderMsg.retrieveAllMsg()
	skanderMarkov=Markov(skanderMsg.getAllMessages())
	#we test
	print(skanderMarkov.generate_markov_text2())

if __name__=='__main__':
	main()
