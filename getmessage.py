#skander-bot
import os
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
		#data for markov  
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
	def createConcatenatedWordList(self):
		""" liste de mot qui se suivent que l'on donne a manger a la classe d'apres"""
		if self.allMessages==[]:
			print("you should retrieve message first")
		for msg in self.allMessages:
			self.concatenatedWords.extend((msg.replace("'"," ")).split())	
	def getWordList(self):
		return 	self.concatenatedWords


def main():
	print("testing with skander")
	skanderMsg=MessageForum("Skander")
	#we retrieve message and compute concatenated words for the markoc class
	skanderMsg.retrieveAllMsg()
	skanderMsg.createWordList()


if __name__=='__main__':
	main()
