SkanderBot
====================
Thr goal of this program is to be able to have access to the collective wisdom of the A.P.O.I.L forum.

====================
How to use
====================
you need your username and login
you can export them as an environment variable if you dont want to do it many times

export APOILusername="your user name"

export APOILpassword="your password"

you can test it by runing 

python3 markov.py

=======================
intepreter usage
=======================
you have to load in the python3 interpreter getmessage and markov
In [1]: from getmessage import MessageForum

In [2]: from markov import Markov

Then you have to define a MessageForum object with a user whose messages you want to get (you have to define user beforehand)
,then you have to ask to retrieve message of the user

In [3]: usermsg=MessageForum(user)

In [4]: usermsg.retrieveAllMsg()

If all went well you should have a Succes message . Then you have to define a Markov object

In [5]: usermarkov=Markov(userMsg.getAllMessages())

If the retrieveAllMsg before didnt work error will apears here.
Now you can run and test generating

In [6]: usermarkov.generate_markov_text2()

You can also use different option with the algo, this require to reload a markov object since it is the one who deals with the token structure
n is the number of word in the key , concatenate means that the message are not concatenated , initToken means that we start with words that are starting some messages.

In [7]: usermarkov2=Markov(skdmsg.getAllMessages(),n=1,concatenate=False,initToken=True)

In [10]: usermarkov2.generate_markov_text2(50)

This option is the number of words(token) int the generated message

=======================
It uses the code from  http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
