#skander-bot

class TokenW():
	"""this class implement multiple ways to derive a dictionnary from a list of string as input of token(words or charactere
		with concantenate=True we have less chance to end up on a dead end with the last token
		without we may have a lot of last token who may or may not have a follow up value
	"""
	def __init__(self,liste_string,n=2,concatenate=True,initToken=False):
		self.key_size=n
		self.listeTokens=self.convertirStringtoList(liste_string) 		#this is a liste of liste
		self.dic={}					#a dictionnary where key are n-tuples of tokens and values are tokesn
		if concatenate:				#in this case we deal with only one liste ie a list of 1 list
			self.concatenateListe()
		self.initToken=initToken 	#to add (or not ) a special token to say where to begin, its no use if we concatenate then there'd be only one start
		self.initkeys=[]			#if we use initToken we need to keep track of all the keys that are begining each lists
	def convertirStringtoList(self,liste_message):
		l=[]
		for msg in liste_message:
			l.append((msg.replace("'"," ")).split())
		return l	
	def concatenateListe(self):		
		while(len(self.listeTokens)>1):
			dernier=self.listeTokens.pop()
			avant_dernier=self.listeTokens.pop()
			avant_dernier.extend(dernier)
			self.listeTokens.append(avant_dernier)
	def generateTuples(self):
		""" Generates tuples of n+1 consecutives tokens from the data in liste
			n is then number of tokens in the keys we need at least n+1 token to create a pair keys value
			see the n=2 code 
			Its EZ to add special token here at the start of each list
		"""
		n=self.key_size
		for l in self.listeTokens:
			if self.initToken:
				l=["START|HERE"]+l				#this has consequences:  we have key with effectively only less true token
			if len(l)>=n+1:
				for i in range(len(l)-(n)):
					yield tuple(l[i:i+n+1])
	def createDic(self):			
		for t in self.generateTuples():
				key=t[:-1]
				value=t[-1]
				if key[0]=="START|HERE":
					self.initkeys.append(key)
				if key in self.dic:
					self.dic[key].append(value)
				else:
					self.dic[key]=[value]

def testToken():
	
	print("Testing tokens on simple case")
	print("empty string")
	l=""
	t=TokenW(l)
	t.createDic()
	print(t.dic)
	print("two small list should NOT return empty")
	l=["1","2"]
	t=TokenW(l,n=1)
	t.createDic()
	print(t.dic)
	print("two small list no concat should  return empty")
	l=["1","2"]
	t=TokenW(l,n=1,concatenate=False)
	t.createDic()
	print(t.dic)
	print("With one liste ")
	print('input: ["a b c d a e b c f"], n=1, concat=False')
	l=["a b c d a e b c f"]
	t=TokenW(l,n=1,concatenate=False)			
	t.createDic()
	print(t.dic)
	print("n=2")
	t=TokenW(l,n=2,concatenate=False)			
	t.createDic()
	print(t.dic)
	print("test concatenate [1,2],[3,4],[8],[5,6,7]"	)				
	l=["1 2","3 4","","8","5 6 7"]
	t=TokenW(l,n=1,concatenate=True)
	print(t.listeTokens)			
	print("no concat n=1")
	l=["1 2","3 4","","8","5 6 7"]
	t=TokenW(l,n=1,concatenate=False)
	print(t.listeTokens)
	t.createDic()
	print(t.dic)
	print("testing init: [[1,2],[3,4],[],[8],[5,6,7]] n=1 no concat")
	l=["1 2","3 4","","8","5 6 7"]
	t=TokenW(l,n=1,concatenate=False,initToken=True)
	t.createDic()
	print(t.dic)
	print(t.initkeys)
def main():
	testToken()

if __name__=='__main__':
	main()
