import sys, getopt
import string
import re
from bs4 import BeautifulSoup
from geopy import location
import pandas as pd
from pandas import DataFrame
import numpy as np
np.random.seed(10)
from  geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='MA')
from csv import writer 

data = pd.read_csv('MA-US-bands_2021-10-06.csv', index_col=0)
michigan_bands = pd.read_csv('MA-US-Michigan-bands-cleaned.csv', index_col=0);
city_locations = pd.read_csv('uscities.csv');
 
def replace_punctuation(raw, replacement=' '):
    """Replaces all punctuation in the input string `raw` with a space.
    Returns the new string."""
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    output = regex.sub(replacement, raw)
    return output

def split_terms(raw):
    """Splits the terms in the input string `raw` on all spaces and punctuation.
    Returns a list of the terms in the string."""
    replaced = replace_punctuation(raw, replacement=' ')
    output = tuple(replaced.split())
    return output

def parse_state(raw):
    if pd.isna(raw):
        return "";
    if pd.isnull(raw):
        return "";
    if raw is None:
        return "";
    if raw==None:
        return "";
    location_chunks = raw.split(',')
    if (len(location_chunks) > 1):
        return location_chunks[1]

def parse_city(raw):
    if pd.isna(raw):
        return "";
    if pd.isnull(raw):
        return "";
    if raw is None:
        return "";
    if raw==None:
        return "";
    location_chunks = raw.split(',')
    if (len(location_chunks) > 1):
        return location_chunks[0]

def retrieve_latitude(raw):
    return 0;

def retrieve_longitude(raw):
    return 0;


def main(argv):
    inputfile = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
    except getopt.GetoptError:
      print('generateLocations.py -i <inputfile>')
      sys.exit(2)

    if len(opts) < 1:
        print('Usage: generateLocations.py -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
      if opt == '-h':
         print('generateLocations.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg      

    print('Processing ', inputfile)
    michigan_bands = pd.read_csv(inputfile, index_col=0);

    # data['NameSoup'] = data['NameLink'].map(lambda raw_html: BeautifulSoup(raw_html, 'html.parser'))
    # data['BandName'] = data['NameSoup'].map(lambda soup: soup.text)      # extracts band name
    # data['BandLink'] = data['NameSoup'].map(lambda soup: soup.a['href']) # extracts link to band's page on M-A
    # data['StatusSoup'] = data['Status'].map(lambda raw_html: BeautifulSoup(raw_html, 'html.parser'))
    # data['Status'] = data['StatusSoup'].map(lambda soup: soup.text)
    # data['GenreTerms'] = data['Genre'].str.replace('Metal', '').map(split_terms)
    michigan_bands['state_name'] = michigan_bands['Location'].map(parse_state);
    michigan_bands['city'] = michigan_bands['Location'].map(parse_city);
    michigan_bands['Latitude'] = michigan_bands['Location'].map(retrieve_latitude)
    michigan_bands['Longitude'] = michigan_bands['Location'].map(retrieve_longitude)


    # Save to CSV
    f_name = 'bands-with-locations.csv'.format( )
    print('Writing band data to csv file:', f_name)
    michigan_bands.to_csv(f_name)
    print('Complete!')


if __name__ == "__main__":
    main(sys.argv[1:])