from gensim.summarization import summarize,keywords



class first_class():
    def summar(self,text,how_large):
        if(how_large==1):##large sumar
            text=summarize(text,ratio=1)
        if(how_large==2):##medium sumar
            text=summarize(text,ratio=0.5)
        if(how_large==3):##small sumar
            text=summarize(text,ratio=0.3)
        return text
    def keywords(self,text):
        text=keywords(text)
        return text
