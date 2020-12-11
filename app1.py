import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from input import naive_bayes, classify, classified_text

postgres = 'williammdavis'
password = 'FuzzyRug5x7'

# #################################################
# # Database Setup
# #################################################
engine = create_engine(f"postgres://pcmmmkwqxtqtom:a49dc8bb322c0f84b36c6e395c260182fd4c3d8310c0aab085374e22e34e4ab4@ec2-54-205-248-255.compute-1.amazonaws.com:5432/d6ks23dtmvo80e")
conn = engine.connect()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/")
def welcome():
    """List all available api routes."""
    return render_template("index.html")


@app.route("/send", methods=["GET", "POST"])

def classified():
    global feed
    resume_prediction = []
    if request.method == "POST":
       
        resume_input  = request.form["resumeName"]
        
        resume_text = classified_text(resume_input)
        prediction = classify(resume_text)
        print(prediction)
        
       
        # return resume_prediction
        # return redirect((resume_prediction = classify(resume_text)), code=302)
    return render_template("form.html", prediction_text= f"your ideal job is {prediction}")

# @app.route("/indeed")
# def indeed():
#     # # Create our session (link) from Python to the DB
#     # session = Session(engine)

#     # Query all data
#     results = pd.read_sql("SELECT * FROM indeed", conn)

#     P2 = results.to_dict(orient='records')
#     # session.close()

#     # # Convert list of tuples into normal list
#     # all_names = list(np.ravel(results))

#     # return jsonify(all_names)
#     return jsonify(P2)


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



    return render_template("form.html")
if __name__ == '__main__':
    app.run(debug=True)

