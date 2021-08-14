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
#
# Voikko.setLibrarySearchPath(r"C:\Users\rache\Downloads\data_science\finnish-app\Voikko")
#
# v = libvoikko.Voikko("fi", r"C:\Users\rache\Downloads\data_science\finnish-app\Voikko\dict")



app = Flask(__name__)

# def practice():
#
#     yle_url = 'https://yle.fi/uutiset/osasto/selkouutiset/'
#
#     response=requests.get(yle_url)
#
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     results = soup.find("div", {"class": "text"})
#
#     yle_articles = results.findAll(text=True)
#
#     #removing headlines and cleaning characters from scraped text
#     h3s = results.findAll('h3')
#     headlines = []
#
#     for h3 in h3s:
#         temp = str(h3)
#         temp = temp.replace('<h3>', '')
#         temp = temp.replace('</h3>', '')
#         headlines.append(temp)
#         del temp
#
#     unwanted_text = ['+ ', '–', '\n', '–\n', 'TV:n selkouutisilla on kesätauko. ', \
#                       '(',')', ')\n', ';', '-"-\n', '; ']
#
#     unwanted_text = unwanted_text + headlines
#
#     article_list = [char for char in yle_articles if char not in unwanted_text]
#
#     article_list = [sent for sent in article_list if not '\n' in sent]
#
#     print(article_list)
#
#     pattern = RegexpTokenizer(r'\w+')
#
#     # Split into sentences
#
#     num = randint(0, len(article_list)-1)
#
#     sentence = article_list[num]
#
#     #print('Sent: '+ sentence)
#
#     # Tokenize sentence, remove punctuation, numbers, and capitalized words (to avoid proper nouns).
#
#     tokenized_sent = pattern.tokenize(sentence)
#
#     tokenized_sent = [word for word in tokenized_sent if re.sub(r'[0-9]', '', word)]
#
#     tokenized_sent = [word for word in tokenized_sent if not word[0].isupper()]
#
#     num = randint(0, len(tokenized_sent)-1)
#
#     word = tokenized_sent[num]
#
#     fill_in_blank = sentence.replace(' '+word, ' _____ ')
#
#     #print('Word1: '+word)
#     #print("blank1: "+fill_in_blank)
#
#     lemmatized = v.analyze(word)[0]
#
#     word_baseform = lemmatized['BASEFORM']
#     word_class = lemmatized['CLASS']
#
#     #print('Lemm: '+word_baseform, word_class)
#
#     #Extract the base form
#     #word_baseform = voikko_dict[0]['BASEFORM']
#     cases = []
#
#     wikiurl = ''
#
#     if word_class == 'teonsana':
#         wikiurl = 'https://fi.wiktionary.org/wiki/Liite:Verbitaivutus/suomi/'+ word_baseform
#     elif word_class == 'nimisana':
#         wikiurl = 'https://fi.wiktionary.org/wiki/'+ word_baseform + '#Taivutus'
#     elif word_class == 'laatusana':
#         wikiurl = 'https://fi.wiktionary.org/wiki/Liite:Adjektiivitaivutus/suomi/'+ word_baseform
#     elif word_class == 'asemosana':
#         wikiurl = 'https://fi.wiktionary.org/wiki/'+ word_baseform
#     else: wikiurl = 'https://fi.wiktionary.org'
#
#     # get the response in the form of html
#
#
#     table_class="wikitable sortable jquery-tablesorter"
#
#     response=requests.get(wikiurl)
#
#     # parse data from the html into a beautifulsoup object
#
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     wikitable=soup.find('table',{'class':"wikitable"})
#
#     if wikitable is None:
#         table_contents = ''
#     else: table_contents = wikitable.findAll(text=True)
#
#     unwanted_chars = [word, '+ ', '–', '\n', '–\n', 'Taivutus\n', 'sijamuoto', 'nominatiivi', 'genetiivi', 'partitiivi', \
#                       'akkusatiivi', 'sisäpaikallissijat', 'inessiivi', 'elatiivi', 'illatiivi', 'ulkopaikallissijat', \
#                       'adessiivi', 'ablatiivi', 'allatiivi', 'essiivi', 'translatiivi', 'abessiivi', 'instruktiivi', \
#                       'komitatiivi', 'positiivi', 'sijamuoto', 'yksikkö', 'monikko', 'kieliopilliset sijamuodot\n', \
#                       'sisäpaikallissijat\n', 'ulkopaikallissijat\n', 'muut sijamuodot\n', 'omistusliite', 'monikko\n', \
#                       'Positiivi', 'Komparatiivi', 'Superlatiivi', 'muut\n','(',')', ')\n', ';', 'Indikatiivi\n', 'preesens\n', \
#                       'perfekti\n', 'persoona\n', 'myönteinen\n', 'kielteinen\n', 'persoona\n', 'myönteinen\n', 'kielteinen\n', 'minä\n', \
#                       'sinä\n','hän\n','me\n','-"-\n','te', 'Te\n','he\n','passiivi','imperfekti\n','pluskvamperfekti\n', '; ']
#
#     negatives = ['en ', 'olen ', 'en ole ', 'et ', 'olet ', 'et ole ', 'ei ',  'on ', 'ei ole ', 'emme ', 'olemme ', 'emme ole ',\
#                  'ette ', 'olette ',  'ette ole ', 'ette ole ', 'eivät ', 'ovat ', 'eivät ole ', 'olin ', 'en ollut ', 'olit ', \
#                  'et ollut ', 'oli ',  'ei ollut ', 'olimme ', 'emme olleet ', 'olitte ', 'ette olleet ', 'ette olleet ',  'olivat ', \
#                  'eivät olleet ']
#
#     if len(table_contents) > 0:
#         cases = [char for char in table_contents if char not in unwanted_chars]
#
#         cases = [char for char in cases if char not in negatives]
#
#         cases = list(dict.fromkeys(cases))
#
#     #print(wikiurl)
#     #print(cases)
#
#     #set options from selected word and randomly selected cases
#     if len(cases) > 0:
#         num = randint(0, len(cases)-1)
#         option_2 = cases[num].replace('-', '').replace('(', '').replace(')', '')
#
#         num = randint(0, len(cases)-1)
#         option_3 = cases[num].replace('-', '').replace('(', '').replace(')', '')
#
#         options = [word, option_2, option_3]
#
#         options = random.sample(options, len(options))
#
#         return fill_in_blank, options, word
#     else: return practice()

def practice():

    yle_url = 'https://yle.fi/uutiset/osasto/selkouutiset/'

    response=requests.get(yle_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find("div", {"class": "text"})

    yle_articles = results.findAll(text=True)

    #removing headlines and cleaning characters from scraped text
    h3s = results.findAll('h3')
    headlines = []

    for h3 in h3s:
        temp = str(h3)
        temp = temp.replace('<h3>', '')
        temp = temp.replace('</h3>', '')
        headlines.append(temp)
        del temp

    unwanted_text = ['+ ', '–', '\n', '–\n', 'TV:n selkouutisilla on kesätauko. ', \
                      '(',')', ')\n', ';', '-"-\n', '; ']

    unwanted_text = unwanted_text + headlines

    article_list = [char for char in yle_articles if char not in unwanted_text]

    article_list = [sent for sent in article_list if not '\n' in sent]

    pattern = RegexpTokenizer(r'\w+')

    # Split into sentences

    num = randint(0, len(article_list)-1)

    sentence = article_list[num]

    # Tokenize sentence, remove punctuation, numbers, and capitalized words (to avoid proper nouns).

    tokenized_sent = pattern.tokenize(sentence)

    tokenized_sent = [word for word in tokenized_sent if re.sub(r'[0-9]', '', word)]

    tokenized_sent = [word for word in tokenized_sent if not word[0].isupper()]

    num = randint(0, len(tokenized_sent)-1)

    word = tokenized_sent[num]

    fill_in_blank = sentence.replace(' '+word, ' _____ ')

    word_baseform = 'asia'
    word_class = 'nimisana'

    cases = []

    wikiurl = ''

    if word_class == 'teonsana':
        wikiurl = 'https://fi.wiktionary.org/wiki/Liite:Verbitaivutus/suomi/'+ word_baseform
    elif word_class == 'nimisana':
        wikiurl = 'https://fi.wiktionary.org/wiki/'+ word_baseform + '#Taivutus'
    elif word_class == 'laatusana':
        wikiurl = 'https://fi.wiktionary.org/wiki/Liite:Adjektiivitaivutus/suomi/'+ word_baseform
    elif word_class == 'asemosana':
        wikiurl = 'https://fi.wiktionary.org/wiki/'+ word_baseform
    else: wikiurl = 'https://fi.wiktionary.org'

    # get the response in the form of html


    table_class="wikitable sortable jquery-tablesorter"

    response=requests.get(wikiurl)

    # parse data from the html into a beautifulsoup object

    soup = BeautifulSoup(response.text, 'html.parser')

    wikitable=soup.find('table',{'class':"wikitable"})

    if wikitable is None:
        table_contents = ''
    else: table_contents = wikitable.findAll(text=True)

    unwanted_chars = [word, '+ ', '–', '\n', '–\n', 'Taivutus\n', 'sijamuoto', 'nominatiivi', 'genetiivi', 'partitiivi', \
                      'akkusatiivi', 'sisäpaikallissijat', 'inessiivi', 'elatiivi', 'illatiivi', 'ulkopaikallissijat', \
                      'adessiivi', 'ablatiivi', 'allatiivi', 'essiivi', 'translatiivi', 'abessiivi', 'instruktiivi', \
                      'komitatiivi', 'positiivi', 'sijamuoto', 'yksikkö', 'monikko', 'kieliopilliset sijamuodot\n', \
                      'sisäpaikallissijat\n', 'ulkopaikallissijat\n', 'muut sijamuodot\n', 'omistusliite', 'monikko\n', \
                      'Positiivi', 'Komparatiivi', 'Superlatiivi', 'muut\n','(',')', ')\n', ';', 'Indikatiivi\n', 'preesens\n', \
                      'perfekti\n', 'persoona\n', 'myönteinen\n', 'kielteinen\n', 'persoona\n', 'myönteinen\n', 'kielteinen\n', 'minä\n', \
                      'sinä\n','hän\n','me\n','-"-\n','te', 'Te\n','he\n','passiivi','imperfekti\n','pluskvamperfekti\n', '; ']

    negatives = ['en ', 'olen ', 'en ole ', 'et ', 'olet ', 'et ole ', 'ei ',  'on ', 'ei ole ', 'emme ', 'olemme ', 'emme ole ',\
                 'ette ', 'olette ',  'ette ole ', 'ette ole ', 'eivät ', 'ovat ', 'eivät ole ', 'olin ', 'en ollut ', 'olit ', \
                 'et ollut ', 'oli ',  'ei ollut ', 'olimme ', 'emme olleet ', 'olitte ', 'ette olleet ', 'ette olleet ',  'olivat ', \
                 'eivät olleet ']

    if len(table_contents) > 0:
        cases = [char for char in table_contents if char not in unwanted_chars]

        cases = [char for char in cases if char not in negatives]

        cases = list(dict.fromkeys(cases))

    #set options from selected word and randomly selected cases
    if len(cases) > 0:
        num = randint(0, len(cases)-1)
        option_2 = cases[num].replace('-', '').replace('(', '').replace(')', '')

        num = randint(0, len(cases)-1)
        option_3 = cases[num].replace('-', '').replace('(', '').replace(')', '')

        options = [word, option_2, option_3]

        options = random.sample(options, len(options))

        return fill_in_blank, options, word
    else: return practice()

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
