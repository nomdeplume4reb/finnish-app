from flask import Flask, render_template, request, redirect

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from random import randint, shuffle
import random
import re
import requests
from bs4 import BeautifulSoup

# import libvoikko
# from libvoikko import Voikko
# v = libvoikko.Voikko(u"fi")

app = Flask(__name__)

# TESTING
def practice():

    return ['fill_in_blank', 'options', 'word']


@app.route("/")
@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == 'POST':
            if request.form.get('Next') == 'Next':
                result = practice()
                fill_in_blank = result[0]
                options = result[1]
                answer = result[2]
                return render_template('home.html', options=options, fill_in_blank = fill_in_blank, answer = answer)
            else:
                return render_template('home.html', options=options, fill_in_blank = fill_in_blank, answer = answer)
    else:
            result = practice()
            fill_in_blank = result[0]
            options = result[1]
            answer = result[2]
            return render_template('home.html', options=options, fill_in_blank = fill_in_blank, answer = answer)


if __name__ == '__main__':
    app.run(debug=False)
