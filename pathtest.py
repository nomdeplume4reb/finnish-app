import libvoikko
from libvoikko import Voikko
import os

dirname = os.path.dirname(os.path.abspath(__file__))
voikkoPath = 'r'+'"'+os.path.join(dirname, 'Voikko')+'"'
voikkoDictPath = 'r'+'"'+os.path.join(dirname, 'Voikko\dict')+'"'
# print(voikkoPath)
# print('r"C:\\Users\\rache\\Downloads\\data_science\\finnish-app\\Voikko"')
# print(voikkoDictPath)
# print('r"C:\\Users\\rache\\Downloads\\data_science\\finnish-app\\Voikko\\dict"')

# Voikko.setLibrarySearchPath(r"C:\Users\rache\Downloads\data_science\finnish-app\Voikko")
#
# v = libvoikko.Voikko("fi", r"C:\Users\rache\Downloads\data_science\finnish-app\Voikko\dict") # ERROR: 'Voikko' object has no attribute '_Voikko__handle'

#v = libvoikko.Voikko(u"fi") # ERROR: no valid dictionaries found

Voikko.setLibrarySearchPath(voikkoPath)

v = libvoikko.Voikko("fi", voikkoDictPath) # ERROR: 'Voikko' object has no attribute '_Voikko__handle'

lemmatized = v.analyze('kissa')[0]

print(lemmatized)
