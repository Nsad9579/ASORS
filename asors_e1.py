# -*- coding: utf-8 -*-
"""ASORS-E1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ro5Z28kNGR7y4zJsTgG6RO-r4dSXh8aD
"""

import pandas as pd
import numpy as np 
import re
import nltk
nltk.download('stopwords')

"""#DATA




"""

with open('/content/Cereals_Relevant.txt', 'r') as F:
  contents=F.read()

content=re.sub(r'\n','', contents)

types=re.findall(r'@(\w.*){',contents)
years=re.findall(r'year = {(\w.*)}',contents)
titles=re.findall(r' title = {(.*)}',contents)

data= {'type':types,'years':years,'title':titles}
df_relevant=pd.DataFrame(data)

with open('/content/Cereals_NotRelevant.txt', 'r') as F2:
  contents2=F2.read()

types2=re.findall(r'@(\w.*){',contents2)
years2=re.findall(r'year = {(\w.*)}',contents2)
titles2=re.findall(r' title = {(.*)}',contents2)

data2= {'type':types2,'years':years2,'title':titles2}
df_notrelevant=pd.DataFrame(data2)

target_relevant=[1 for i in range(297)]
target_notrelevant=[0 for i in range(387)]

df_relevant.insert(3,"target",target_relevant)
df_relevant.head()

df_notrelevant.insert(3,"target",target_notrelevant)
df_notrelevant.head()

df=pd.concat([df_notrelevant,df_relevant])
df.head()

df=df.sort_values( by=["title"],ascending= True )

df.head()

from sklearn.model_selection import train_test_split
x=df[['title','type']]
y=df['target']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

"""#preprocessing"""

#1:remove puntuation 

import string

def remove__puntuation(text):
  V=text.maketrans('','',string.punctuation)
  return text.translate(V)

df['title']=df.title.map(lambda x: remove__puntuation(x))

X_train['title']=X_train.title.map(lambda x: remove__puntuation(x))
X_test['title']=X_test.title.map(lambda x: remove__puntuation(x))

X_train.head()

#2:remove stopwords
from nltk.corpus import stopwords

the_stopwords=set(stopwords.words('english'))

def remove__stopwords(text):
  text=[word.lower() for word in text.split() if word.lower() not in the_stopwords]
  return " ".join(text)

df['title']= df.title.map(lambda x: remove__stopwords(x))

X_train['title']= X_train.title.map(lambda x: remove__stopwords(x))
X_test['title']= X_test.title.map(lambda x: remove__stopwords(x))

#tokenization 
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
def Tokenize_cp(df):
  corpus=[]
  for word in df["title"]:
    w=[word.lower() for word in word_tokenize(word)]
    corpus.append(w)
  return corpus

corpus=Tokenize_cp(df)
len(corpus)

from sklearn.model_selection import train_test_split
x=df[['title','type']]
y=df['target']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

"""#Embedings"""

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

num_words=len(corpus)+1

tokenizer=Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(X_train["title"])

train_sequence=tokenizer.texts_to_sequences(X_train["title"])

len(max(X_test["title"]).split())

max_len=17
train_pad=pad_sequences(train_sequence,maxlen=max_len,truncating="post",padding="post")

train_pad

#and now same for test
max_len=17
test_sequence=tokenizer.texts_to_sequences(X_test["title"])
test_pad=pad_sequences(test_sequence,maxlen=max_len,truncating="post",padding="post")

print(X_train.title[0])
print(train_sequence[0])

WordIindex=tokenizer.word_index

print("Number of unique words:", len(WordIindex))

pip install urllib

import urllib.request
urllib.request.urlretrieve('https://nlp.stanford.edu/data/glove.6B.zip','glove.6B.zip')

!unzip "/content/glove.6B.zip" -d "/content/"

Dict_Embeded={}
with open('/content/glove.6B.200d.txt') as the_file:
  for line in the_file:
    val=line.split()
    word=val[0]
    vec=np.asarray(val[1:],'float32')
    Dict_Embeded[word]=vec

len(Dict_Embeded["with"])

type(embedding_matrix)

num_words = len(WordIindex) + 1
embedding_matrix = np.zeros((num_words, 200))

for word, i in WordIindex.items():
    if i < num_words:
        emb_vec = Dict_Embeded.get(word)
        if emb_vec is not None:
            embedding_matrix[i] = emb_vec

#1.Define the model.
#2.Compile the model.
#3.Fit the model.
#4.Evaluate the model.
#5.Make predictions.

from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.initializers import Constant
from tensorflow.keras.optimizers import Adam

model = Sequential()

model.add(Embedding(num_words,200, embeddings_initializer=Constant(embedding_matrix),input_length=max_len,trainable=False))
model.add(LSTM(200, dropout=0.1))
model.add(Dense(1, activation="sigmoid"))
optimizer = Adam(learning_rate=3e-4)
model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=["accuracy"])

train_labels=y_train
test_labels=y_test
model.fit(train_pad,train_labels,epochs=10,validation_data=(test_pad, test_labels),verbose=1)



pred = model.predict(padded)
pred_int = pred.round().astype("float32")

model.summary()

test="the effect of heart failure on mortality of pregnant females through the third semaster"
sequences = tokenizer.texts_to_sequences([test])
padded = pad_sequences(sequences, maxlen=max_len, padding="post", truncating="post")

pred = model.predict(padded)
pred_int = pred.round().astype("int")

pred_int

#that's true :)