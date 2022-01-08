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


BASEURL = 'https://www.metal-archives.com/browse/ajax-country/c/'
RELURL = '/json/1/'
response_len = 500
 
def replace_punctuation(raw, replacement=' '):
    """Replaces all punctuation in the input string `raw` with a space.
    Returns the new string."""
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    output = regex.sub(replacement, raw)
    return output

def split_genre_terms(raw):
    """Splits the terms in the input string `raw` on all spaces and punctuation.
    Returns a list of the terms in the string."""
    replaced = replace_punctuation(raw, replacement=' ')
    output = tuple(replaced.split())
    return output

def get_country_codes():
    if exists('./country_codes.json'):
        return
    else:
        countries = dict();
        countries_html = requests.get("https://www.metal-archives.com/browse/country")
        soup = BeautifulSoup(countries_html.content, 'html.parser')
        country_columns = soup.find_all("div", {"class": "countryCol"})
        for column in country_columns:
            for country in column:
                if str(country).startswith('<a'):
                    code = str(country).replace('<a href="https://www.metal-archives.com/lists/', '').split('">')[0]
                    name = str(country).split('">')[1].replace('</a>', '');
                    countries[code] = name
        with open('country_codes.json', 'w') as json_file:
            json.dump(countries, json_file)
 
def get_url(country='AF', start=0, length=500):
    """Gets the listings displayed as alphabetical tables on M-A for input
    `country`, starting at `start` and ending at `start` + `length`.
    Returns a `Response` object. Data can be accessed by callingt the `json()`
    method of the returned `Response` object."""
    
    payload = {'sEcho': 0,  # if not set, response text is not valid JSON
               'iDisplayStart': start,  # set start index of band names returned
               'iDisplayLength': length} # only response lengths of 500 work
    headers = {'user-agent': 'Metal-Map'}

    r = requests.get(BASEURL + country + RELURL, headers=headers, params=payload)
    
    return r

def get_country_latitude(code):
    with open('./country_data.json') as file:
        countries_dict = json.load(file)
    country_dict = {x['alpha2']: x for x in countries_dict['countries']}
    return country_dict[code]['latitude']

def get_country_longitude(code):
    with open('./country_data.json') as file:
        countries_dict = json.load(file)
    country_dict = {x['alpha2']: x for x in countries_dict['countries']}
    return country_dict[code]['longitude']

def get_all_bands():
    # Data columns returned in the JSON object
    with open('./country_data.json') as file:
        countries = json.load(file)
    column_names = ['NameLink', 'Genre', 'Location', 'Status', 'CountryCode', 'CountryName']
    data = DataFrame() # for collecting the results
    date_of_scraping = datetime.datetime.utcnow().strftime('%Y-%m-%d')

    # Retrieve the data
    for countryCode, countryName in countries.items():
        # Get total records for given country & calculate number of chunks
        print('Current country = ', countryName)
        r = get_url(country=countryCode, start=0, length=response_len)
        js = r.json()
        n_records = js['iTotalRecords']
        n_chunks = int(n_records / response_len) + 1
        print('Total records = ', n_records)

        # Retrieve chunks
        for i in range(n_chunks):
            start = response_len * i
            if start + response_len < n_records:
                end = start + response_len
            else:
                end = n_records
            print('Fetching band entries ', start, 'to ', end)
            
            for attempt in range(10):
                time.sleep(3) # Obeying robots.txt "Crawl-delay: 3"
                try:
                    r = get_url(country=countryCode, start=start, length=response_len)
                    js = r.json()
                    # Store response
                    df = DataFrame(js['aaData'])
                    df['CountryCode'] = countryCode
                    df['CountryName'] = countryName
                    data = data.append(df)

                # If the response fails, r.json() will raise an exception, so retry 
                except JSONDecodeError:
                    print('JSONDecodeError on attempt ', attempt, ' of 10.')
                    print('Retrying...')
                    continue
                break

    # Set informative names
    data.columns = column_names

    # Current index corresponds to index in smaller chunks concatenated
    # Reset index to start at 0 and end at number of bands
    data.index = range(len(data))

    data['NameSoup'] = data['NameLink'].map(lambda raw_html: BeautifulSoup(raw_html, 'html.parser'))
    data['BandName'] = data['NameSoup'].map(lambda soup: soup.text)      # extracts band name
    data['BandLink'] = data['NameSoup'].map(lambda soup: soup.a['href']) # extracts link to band's page on M-A
    data['StatusSoup'] = data['Status'].map(lambda raw_html: BeautifulSoup(raw_html, 'html.parser'))
    data['Status'] = data['StatusSoup'].map(lambda soup: soup.text)
    data['GenreTerms'] = data['Genre'].str.replace('Metal', '').map(split_genre_terms) 
    data['CountryLatitude'] = data['CountryCode'].map(get_country_latitude)
    data['CountryLongitude'] = data['CountryCode'].map(get_country_longitude)

    data.drop(columns=['NameSoup', 'StatusSoup'])

    # Save to CSV
    f_name = 'MA-bands-{}.csv'.format(date_of_scraping)
    print('Writing band data to csv file:', f_name)
    data.to_csv(f_name)
    print('Complete!')
    print(data[['BandName', 'Genre', 'Status', 'Status', 'CountryName', 'Location', 'CountryLatitude', 'CountryLongitude']].head())
    return data

get_country_codes()
get_all_bands()
 
 