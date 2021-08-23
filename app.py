from flask import Flask, render_template, request, redirect

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from random import randint, shuffle
import random
import re
import requests
from bs4 import BeautifulSoup
import os
import libvoikko
from libvoikko import Voikko


#This library only loads locally on my machine, when I enter the file path. But I can't get it to deploy to Heroku.
dirname = os.path.dirname(os.path.abspath(__file__))
voikkoPath = 'r'+'"'+os.path.join(dirname, 'Voikko')+'"'
voikkoDictPath = 'r'+'"'+os.path.join(dirname, 'Voikko\\dict')+'"'
Voikko.setLibrarySearchPath(voikkoPath)
v = libvoikko.Voikko("fi", voikkoDictPath)
# Voikko.setLibrarySearchPath(r"C:\Users\rache\Downloads\data_science\finnish-app\Voikko")
# v = libvoikko.Voikko("fi", r"C:\Users\rache\Downloads\data_science\finnish-app\Voikko\dict")

app = Flask(__name__)

#TESTING WITHOUT YLE

def practice():
#Static variable until I figure out how to reliably scrape from https://yle.fi/uutiset/osasto/selkouutiset/
    article_list = ['TV:n selkouutisilla on kesätauko.', 'Selkouutiset nähdään TV:ssä taas maanantaina 23.8.', 'Radion selkouutiset tehdään joka päivä myös kesällä.', 'Suomi on lähettänyt 2 virkamiestä Kabulin lentokentälle Afganistaniin.', 'Virkamiehet auttavat, kun ihmisiä haetaan Afganistanista Suomeen.', 'Asiasta kertoo ulkoministeri Pekka Haavisto.', 'Haavisto sanoo, että lähes 70 Suomen kansalaista on pyytänyt apua.', 'He haluavat Suomeen Afganistanista.', 'Suomi yrittää tuoda Suomeen myös Afganistanin Suomen lähetystön työntekijät.', 'Mielenosoituksia Afganistanissa', 'Afganistanissa on osoitettu mieltä Talibania vastaan.', 'Mediatiedot kertovat, että talibanit ovat ampuneet mielenosoittajia kohti Jalalabadin kaupungissa.', 'Ainakin 2 ihmistä on kuollut ja noin 10 ihmistä on loukkaantunut.', 'Koronaluvut', 'Suomessa on 673 uutta koronatartuntaa.', 'THL kertoo, että uusia koronakuolemia on 2.', 'Sairaalassa on nyt 106 ihmistä.', 'Heistä 29 saa tehohoitoa.', '2 viikon aikana on ollut lähes 2700 koronatartuntaa enemmän kuin 2 viikkoa aikaisemmin.', 'Kokoomus koronarokotukset', 'Oppositiopuolue kokoomus ehdottaa hallitukselle, että koronatestejä tehdään jatkossa myös apteekeissa.', 'Kokoomus haluaa, että testauspaikkoja on tulevaisuudessa enemmän kuin nyt.', 'Testien pitää kokoomuksen mielestä myös olla halvempia kuin nyt.', 'Kokoomuksen ehdotuksesta kertoo puheenjohtaja Petteri Orpo.', 'Hän puhui kokoomuksen kesäkokouksessa Seinäjoella.', 'Orpon mielestä Suomen apteekit pystyvät tekemään koronatestejä.', 'Orpo sanoo, että muualla Euroopassa koronatestejä tehdään paljon enemmän kuin Suomessa.', 'Konkurssit', 'Yrityksiä menee konkurssiin vähemmän kuin aikaisemmin.', 'Tilastokeskus kertoo, että konkursseja oli alkuvuonna 1,6 prosenttia vähemmän kuin samaan aikaan viime vuonna.', 'Varsinkin ravintoloita ja hotelleja meni konkurssiin vähemmän kuin viime vuonna.', 'Ravintoloiden ja hotellien konkurssit vähentyivät yli 16 prosenttia.', 'Maataloudessa ja rakennusalalla konkursseja oli enemmän kuin aikaisemmin.']

    pattern = RegexpTokenizer(r'\w+')

    # Split into sentences

    num = randint(0, len(article_list)-1)

    sentence = article_list[num]

    # print('SENT: '+ sentence)

    # Tokenize sentence, remove punctuation, numbers, and capitalized words (to avoid proper nouns).

    tokenized_sent = pattern.tokenize(sentence)

    tokenized_sent = [word for word in tokenized_sent if re.sub(r'[0-9]', '', word)]

    tokenized_sent = [word for word in tokenized_sent if not word[0].isupper()]

    # print('TOK_SENT: ', tokenized_sent)

    num = randint(0, len(tokenized_sent)-1)

    word = tokenized_sent[num]

#   create a fill-in-the-blank from the sentence
    fill_in_blank = sentence.replace(' '+word, ' _____ ')

    # print("SENTENCE: ", sentence)

    #If the selected word is not in the voikko library, the function should repeat again until a new word is chosen

    if len(v.analyze(word)) > 0:
# Get the baseform of the selected word from the Voikko library
        lemmatized = v.analyze(word)[0]

        word_baseform = lemmatized['BASEFORM']
        word_class = lemmatized['CLASS']

        # print('LEMM: '+word_baseform, word_class)
# Look up the baseform on wikisanakirja and scrape other cases to use as multiple choice options
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

            cases = [''.join(e for e in case if e.isalnum()) for case in cases]

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
