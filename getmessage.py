#skander-bot
#functions to retrieve messages from people from the apoil forum
import os #for environment variable
import random
from  bs4 import BeautifulSoup as bs
import urllib
import requests
	

#il faut rajouter des verif sur la conexion sinon la liste des messages sera vide car on sera sur une page de conection
#potentile problem: pb de conection avec les login/pss, probleme d'user, probleme de web ajouter exception HTTPerror 
class MessageForum():
	""" This class goal is to retrieve message from a given user of the APOIL forum 
		at init it doesnt do anything you have to run getAllMsg to compute them
		and remember them in allMessages list
	"""
	def __init__(self,user):
		self.user=user		#user we wish to get message from the forum
		self.urlMessage=self.getUrl("/spa/"+ urllib.parse.quote(self.user))
		self.allMessages=[]
		#data for markov class folowing 
		self.concatenatedWords=[]
		if "APOILusername" not in os.environ.keys():
			self.username=input("Username of APOIL FORUM ? You should do export APOILusername=yourusername ")
			os.environ["APOILusername"]=self.username
		else:
			self.username=os.environ["APOILusername"]	
		if "APOILpassword" not in os.environ.keys():
			self.password=input("Password of APOIL FORUM ?  ")
			os.environ["APOILpassword"]=self.password
		else:
			self.password=os.environ["APOILpassword"]	
			
	def liste_message(self,page_messages):
		"""takes beautifoul souup html into input  output: une liste de message en texte de l'url donnee"""
		listeMessageText=[]
		listeMessages=page_messages.findAll("div",{"class":"postbody"})
		for m in listeMessages:
			listeMessageText.append(self.nettoyer(m))
		return listeMessageText
	def retrieveAllMsg(self,force=False):
		"""en input l'url de la page forum actif de message d'un user en output liste de tous les messages en texte"""
		if self.allMessages==[] or  force:
			#d'abord on se connecte
			print("connecting to forum")
			s = requests.session()
			url="http://apoil.forumactif.com/login"
			page=s.get(url)
			headers={'username':self.username ,	'password': self.password,	"autologin":"on",	'redirect':"",	'query':"",	'login':"Connexion"	}
			auth = s.post(url, params=headers, cookies=page.cookies)
			#on fait une boucle sur toutes les pages
			#ensuite on get la page on envoie a bs
			url_temp=self.urlMessage
			liste_all=[]
			num_pages=1
			while True:
				print("retrieving ", url_temp,"pages number",num_pages)
				member=s.get(url_temp)
				page=bs(member.text)		#bs du code de la page message du membre donné
				liste_current=self.liste_message(page)
				liste_all.extend(liste_current)
				print("added",len(liste_current)," messages")
				suiv=page.findAll("img",{"alt":"Suivant"})
				if len(suiv)==0:
					break
				url_temp=self.getUrl(suiv[0].parent.get('href'))
				num_pages+=1
			self.allMessages=liste_all	
	def nettoyer(self,message):
		"""input: bs tag, retourne du texte sans html avec les quotes en moins"""
		for quote in message.findAll("dl",{"class":"codebox"}):
			quote.decompose()
		return message.get_text()					
	def getUrl(self,relativ_url):
		return "http://apoil.forumactif.com"+relativ_url 
	def getAllMessages(self):
		return self.allMessages
	def createWordList(self):
		""" liste de mot qui se suivent que l'on donne a manger a la classe d'apres"""
		if self.allMessages==[]:
			print("you should retrieve message first")
		for msg in self.allMessages:
			self.concatenatedWords.extend((msg.replace("'"," ")).split())	
	def getWordList(self):
		return 	self.concatenatedWords

#from http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
class Markov(object):
	
	def __init__(self, liste_mot):
		self.cache = {}
		#self.open_file = open_file
		self.words = liste_mot
		self.word_size = len(self.words)
		self.database()
		
	
	def file_to_words(self):
		self.open_file.seek(0)
		data = self.open_file.read()
		words = data.split()
		return words
		
	
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
