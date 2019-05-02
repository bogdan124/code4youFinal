from bs4 import BeautifulSoup
from bs4.element import Comment



def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


string='''
<p></p>
<p></p>
<p><span style="color: inherit; font-family: inherit; font-size: 2rem;"><img src="http://localhost:5000/visualize_code?id=2" alt="">What is Python?</span></p>
<p></p>
<p>Python is a popular programming language. It was created in 1991 by Guido van Rossum.</p>

<p>It is used for:</p>

<ul>
    <li>web development (server-side), </li>
    <li>software development, </li>
    <li>mathematics,</li>
    <li>system scripting.</li>
</ul>

<p></p>
<h3>What can Python do?</h3>
<p></p>
<ul>
    <li>Python can be used on a server to create web applications.</li>
    <li>Python can be used alongside software to create workflows.</li>
    <li>Python can connect to database systems. It can also read and modify files.</li>
    <li>Python can be used to handle big data and perform complex mathematics.</li>
    <li>Python can be used for rapid prototyping, or for production-ready software development.</li>
</ul>

<p></p>
<h3>Why Python?</h3>
<p></p>
<ul>
    <li>Python works on different platforms (Windows, Mac, Linux, Raspberry Pi, etc).</li>
    <li>Python has a simple syntax similar to the English language.</li>
    <li>Python has syntax that allows developers to write programs with fewer lines than some other programming languages.</li>
    <li>Python runs on an interpreter system, meaning that code can be executed as soon as it is written. This means that prototyping can be very quick.</li>
    <li>Python can be treated in a procedural way, an object-orientated way or a functional way.</li>
</ul>

<p></p>
<h3>Good to know</h3>
<p></p>
<ul>
    <li>The most recent major version of Python is Python 3, which we shall be using in this tutorial. However, Python 2, although not being updated with anything other than security updates, is still quite popular.</li>
    <li>In this tutorial Python will be written in a text editor. It is possible to write Python in an Integrated Development Environment, such as Thonny, Pycharm, Netbeans or Eclipse which are particularly useful when managing larger collections of Python
        files.
    </li>
</ul>
<iframe src="http://localhost:5000/visualize_code?id=2" width="1018px" height="311px"></iframe>
<p></p>
<p></p>
<p></p>
<h3>Python Syntax compared to other programming languages</h3>
<p></p>
<ul>
    <li>Python was designed to for readability, and has some similarities to the English language with influence from mathematics.</li>
    <li>Python uses new lines to complete a command, as opposed to other programming languages which often use semicolons or parentheses.</li>
    <li>Python relies on indentation, using whitespace, to define scope; such as the scope of loops, functions and classes. Other programming languages often use curly-brackets for this purpose.</li>
</ul>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<hr>
'''
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import re


l=[]

class tokenization():
    def __init__(self,string_to_evaluate):
        self.string_to_evaluate=string_to_evaluate
    ##    self.dict___=
    def evaluate_string(self):
        soup = BeautifulSoup(self.string_to_evaluate, 'html.parser')
        texts = soup.get_text()
        print(word_tokenize(texts))
        return texts

class dictionary_word():
    def download_nltk_dictionary(self,give_the_word):
        l[:] = []
        word11=wordnet.synsets(give_the_word);
        for i in word11:
            l.append(i.definition())
        return l


class get_modify():
    def __init__(self,string_modify__,list_of_modification):
        self.string_modify__=string_modify__
        self.list_of_modification=list_of_modification
        self.date=[['<p>','</p>'],['<hr/>'],['<ul>','</ul>'],['<ol>','</ol>'],['table'],['img'],['video']]##https://getbootstrap.com/docs/4.3/components/popovers/
    def delete_tags_from_string(self):
        result=self.string_modify__
        for i in self.list_of_modification:
            if i[2]==1:
                result = re.sub('<p>', "", result)
                result = re.sub('</p>', "", result)
            if i[3]==1:
                result = re.sub('<hr>', "", result)
            if i[4]==1:
                result = re.sub('<ol>', "", result)
                result = re.sub('</ol>', "", result)
            if i[5]==1:
                result = re.sub('<ul>', "", result)
                result = re.sub('</ul>', "", result)
            if i[6]==1:
                result = re.sub(r'<(table|br)[^>]*?>', "", result)
                result = re.sub(r'<(td|br)[^>]*?>', "", result)
                result = re.sub('</td>', "", result)
                result = re.sub('<tr>', "", result)
                result = re.sub('</tr>', "", result)
                result = re.sub('</table>', "", result)
                result = re.sub('<tbody>', "", result)
                result = re.sub('</tbody>', "", result)
                result = re.sub('</th>', "", result)
                result = re.sub(r'<(th|br)[^>]*?>', "", result)
            if i[7]==1:
                result = re.sub('</th>', "", result)
                result = re.sub(r'<(th|br)[^>]*?>', "", result)
            if i[8]==1:
                result = re.sub(r'<(img|br)[^>]*?>', "", result)
        ##    if i[12]==1:
                ##result = re.sub(r'<(video|br)[^>]*?>', "", result)
            if i[9]!=0:
                if i[9]==1:
                    result ="<div style='text-align: left;'>"+result+"</div>"
                elif i[9]==2:
                    result ="<div style='text-align: center;'>"+result+"</div>"
                elif i[9]==3:
                    result ="<div style='text-align: right;'>"+result+"</div>"
            if i[11]==1:##don't like code
                result = re.sub(r'<(iframe|br)[^>]*?>', "", result)
            if i[13]==1:
                result = re.sub(r'<(a|br)[^>]*?>', "", result)
                result = re.sub('</a>', "", result)

    ##          elif i[10]==2:

    ##            elif i[10]==3:

        return result
