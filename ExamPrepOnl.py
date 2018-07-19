#Importing all the required libraries
import PyPDF2 
import textract
import collections
import re
import pandas as pd
from pandas import ExcelWriter
'''
import nltk
nltk.download('punkt')
nltk.download('stopwords')
'''
#Importing the methods from packages
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#Declaring the pdf 
filename = 'JavaBasics-notes.pdf'
#Using open to make the file readable
pdfFileObj = open(filename,'rb')
#Reading the file
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#Finding the no.of pages
num_pages = pdfReader.numPages
#Initialising count and text
count = 0
text = ""

#Extracting the text from each page in the pdf
while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count +=1
    text += pageObj.extractText()

if text != "":
   text = text

else:
   text = textract.process(filename, method='tesseract', language='eng')
   
#Creating the list of Java Keywords   
keywords=['boolean','byte','char','short','int','long','float','double','for','do','while',
           'if','else','switch','case','default','break','continue','return','try','throw','catch','finally','throws','public'
           ,'protected','private','static','final','abstract','synchronized','native','transient','volatile','class','interface','extends'
           ,'implements','package','import','true','false','null','void','this','new','super','instanceof']  
   
#Tokenizing the entire text i.e, making the text into individual strings
tokens = word_tokenize(text)  

#Declaring the set of stop words
stop_words = set(stopwords.words('english'))

#Creating key list using the tokens
key = [word for word in tokens]

#Removing the numbers,lowering the strings,splitting the text and removing the stopwords
corpus = []
for i in range(0, len(key)):
    review = re.sub('[^a-zA-Z]', ' ', key[i])
    review = review.lower()
    review = review.split()
    review = [word for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    corpus.append(review)
    
#Removing empty strings in the list    
key = [s for s in corpus if s] 

#Removing the charecters in the key list
for words in key:
    if len(words) == 1:
        key.remove(words)
        
#Creating a new list
key1=[]
        
#Finding the common strings in both lists and and adding them to a new list        
for i in key:
    for j in keywords:
        if i==j:
            key1.append(i)

#Finding the first 50 common words and the no.of times they are repeated 
counter = collections.Counter(key)
print(counter.most_common(50)) 

#Removing the charecters in the key1 list
for words in key1:
    if len(words) == 1:
        key1.remove(words)  
        
#Finding the common words and the no.of times they are repeated        
counter1 = collections.Counter(key1)
print(counter1.most_common())    

#Creating two Lists and adding them to dataframe
excel=list(sorted(counter1, key=counter1.__getitem__))
excel1=list(sorted(counter1.values()))
pf=pd.DataFrame({'keywords':excel,'No.of times keyword Occured':excel1})

#Converting the dataframe to an excel sheet
writer = ExcelWriter('Python.xlsx')
pf.to_excel(writer,'Sheet5')
writer.save()

