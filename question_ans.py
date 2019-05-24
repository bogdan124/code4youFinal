import nltk



class QandA():
	def ie_preprocess(self,document):
	    sentences = nltk.sent_tokenize(document)
	    sentences = [nltk.word_tokenize(sent) for sent in sentences] 
	    sentences = [nltk.pos_tag(sent) for sent in sentences]
	    return sentences

	def take_result_q_and_a(self,take_result):
	   createQ=[]
	   create_sentence=""
           l=0
	   for i in take_result:
		for j in i:
			if  j[1]=='NN':
			    createQ.append(j[0])
			    l=l+1
			    create_sentence=create_sentence+" "+"__"+str(l)+"__"	
			else:
			   create_sentence=create_sentence+" "+j[0]		   	
	  	
	   return [[create_sentence],[createQ]]


##result1= QandA()
##result = result1.ie_preprocess('''Python uses new lines to complete a command, as opposed to other programming languages which often use semicolons or parentheses.
##Python relies on indentation, using whitespace, to define scope; such as the scope of loops, functions and classes. Other programming languages often use curly-brackets for ##this purpose.''')

##print(result1.take_result_q_and_a(result))

