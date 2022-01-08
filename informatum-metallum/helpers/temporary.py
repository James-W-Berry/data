#! /usr/bin/env python
import time
import datetime
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import pandas as pd
import string
import json
import re
from os.path import exists

data = pd.read_csv('../MA-bands.csv')
print (data.head())

def replace_punctuation(raw, replacement=' '):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    output = regex.sub(replacement, raw)
    return output

def split_location_terms(raw):
    # "/" or ";" = additional location
    # "," 
    print(raw)


data['LocationTerms'] = data['Location'].map(split_location_terms)

print (data.head())