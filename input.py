#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
from sqlalchemy import create_engine
from string import digits
import numpy as np
import os
import nltk
import string
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from nltk.probability import FreqDist, DictionaryProbDist, ELEProbDist, sum_logs
from nltk.classify.api import ClassifierI

# nltk.download('stopwords')


# In[5]:
def naive_bayes ():


    csv = "./df.csv"
    df = pd.read_csv(csv, encoding = 'unicode_escape')
    df.head()


    # In[6]:


    df_sample = df.sample(frac =.1) 
    df_sample.head()
    # print(len(df_sample))


    # In[7]:


    df3 = df_sample[['Job_Type', 'Description_and_Skill']]
    df3.head()


    # In[ ]:


    # df3.to_csv('df3.csv')
    # df.describe()
    # df.dtypes
    # len(df3['Description'])


    # In[8]:


    df3.dropna(inplace=True)
    len(df3['Description_and_Skill'])


    # In[9]:


    def process_text(text):
        nopunc = [char for char in text if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
        return clean_words


    # In[10]:


        df['Description_and_Skill'].head().apply(process_text)


    # In[11]:


    #convert collection of text to a matrix of tokens
    from sklearn.feature_extraction.text import CountVectorizer
    count_v  = CountVectorizer(analyzer=process_text)
    message_bow = count_v.fit_transform(df3['Description_and_Skill'])

    # In[12]:

    #split the data into 80% training and 20% testing
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(message_bow, df3['Job_Type'],test_size=0.20, random_state=0)
    # In[13]:

    # message_bow.shape


    # In[14]:


    #create and train the naive bayes classifier
    from sklearn.naive_bayes import MultinomialNB
    classifier =  MultinomialNB().fit(X_train, y_train)


    # In[15]:


    #print the prediction
    # print(classifier.predict(X_train))
    #print values
    # print(y_train.values)


    # In[16]:


    #Evaluate the model on the training data set 
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
    prediction = classifier.predict(X_train)
    # print(classification_report(y_train, prediction))
    # print()


    # In[17]:

    # print('Confusion Matrix: \n', confusion_matrix(y_train,prediction))
    # print('Accuracy Matrix:',  accuracy_score(y_train,prediction))


    # In[18]:

    #print the prediction
    # print(classifier.predict(X_test))
    #print values
    # print(y_test.values)


    # In[19]:


    #Evaluate the model on the training data set 
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
    prediction = classifier.predict(X_test)
    print(classification_report(y_test, prediction))
    # print()
    # print('Confusion Matrix: \n', confusion_matrix(y_test,prediction))
    # print()
    # print('Accuracy Matrix:',  accuracy_score(y_test,prediction))

    # In[ ]:
    print("hey")


# print(X_train)
    
def classified_text(text):
    
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    clean_text = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    return clean_text

    # In[22]:
# resume_input= []
def classify (resume_input) :
    count_v  = CountVectorizer(analyzer=classified_text)
    resume_input  = request.form["resumeName"]

    input_bow = count_v.transform(resume_input)
        # print(input_bow)
        # classifier =  MultinomialNB().fit(X1_train, y1_train)
    job = classifier.predict(input_bow)
    return job
    # return classify

if __name__ == '__main__':
    # app.run(debug=True)

   

