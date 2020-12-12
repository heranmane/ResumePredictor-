import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
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
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
# from input import naive_bayes


postgres = 'williammdavis'
password = 'FuzzyRug5x7'

#################################################
# Database Setup
#################################################
engine = create_engine(f"postgres://pcmmmkwqxtqtom:a49dc8bb322c0f84b36c6e395c260182fd4c3d8310c0aab085374e22e34e4ab4@ec2-54-205-248-255.compute-1.amazonaws.com:5432/d6ks23dtmvo80e")
conn = engine.connect()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    # Load the data
    
    
    """List all available api routes."""
    return render_template("index.html")


    # return (
    #     f"Available Routes:<br/>"

    #     f"/indeed<br/>"
    #     f"/Job_Type<br/>"
    # )

@app.route("/predict", methods=["POST"])

def predict():
    csv = "./df.csv"
    df = pd.read_csv(csv, encoding = 'unicode_escape')
    df_sample = df.sample(frac = .1)
    df3 = df_sample[['Job_Type', 'Description_and_Skill']]
    df3 = df3.dropna()

    #Function to clean text
    def process_text(text):
        nopunc = [char for char in text if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
        return clean_words

    #Actually tokenize
    count_v  = CountVectorizer(analyzer=process_text)
    message_bow = count_v.fit_transform(df3['Description_and_Skill'])

    #Split data into 80% training and 20% testing
    X_train, X_test, y_train, y_test = train_test_split(message_bow, df3['Job_Type'],test_size=0.20, random_state=42)

    #Create and train the naive bays classifier
    classifier =  MultinomialNB().fit(X_train, y_train)

    #Evaluate the model on the training dataset
    classifier.predict(X_train)

    
    #User input information

    if request.method == "POST":

        message = request.form['message']
        data = [message]
        vect = count_v.transform(data)
        my_prediction = classifier.predict(vect)

    return render_template('index.html', prediction=f'Your job type is {my_prediction}')

@app.route("/final")
def indeed():
    # # Create our session (link) from Python to the DB
    # session = Session(engine)

    # Query all data
    results = pd.read_sql("SELECT * FROM final", conn)

    P2 = results.to_dict(orient='records')
    # session.close()

    # # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))

    # return jsonify(all_names)
    return jsonify(P2)


@app.route("/Job_Type")
def Job_Type():
    # # Create our session (link) from Python to the DB
    # session = Session(engine)

    # Query all data
    results1 = pd.read_sql("SELECT * FROM job_type", conn)

    Job_Type = results1.to_dict(orient='records')
    # session.close()

    # # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))

    # return jsonify(all_names)
    return jsonify(Job_Type)


@app.route("/heran")
def heran():
    # # Create our session (link) from Python to the DB
    # session = Session(engine)

    # Query all data
    results2 = pd.read_sql("SELECT * FROM final", conn)

    heran = results2.to_dict(orient='records')
    # session.close()

    # # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))

    # return jsonify(all_names)
    return jsonify(heran)

if __name__ == '__main__':
    app.run(debug=True)

