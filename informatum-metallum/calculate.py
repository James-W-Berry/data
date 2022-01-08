#! /usr/bin/env python
import os
from os.path import exists
import sys, getopt
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

load_dotenv()
CENSUS_API_KEY = os.getenv('CENSUS_API_KEY')

def country_populations():
    with open('./country_data.json') as file:
        countries_dict = json.load(file)
        for country in countries_dict['countries']:
            population_sum = 0;
            countries_html = requests.get("https://api.census.gov/data/timeseries/idb/1year?get=AGE,NAME,POP&GENC={}&YR=2021&SEX=0&key={}".format(country['alpha2'],CENSUS_API_KEY))
            try:
                soup = BeautifulSoup(countries_html.content, 'html.parser')
                if (soup.text is not None):
                    soup_json=json.loads(soup.text)
                    for age in soup_json:
                        if(age[2] != 'POP'):
                            population_sum += int(age[2])
                    print('total population for {} is {}'.format(country['alpha2'], population_sum))
                    country['totalPopulation'] = population_sum
            except:
                print('Could not retrieve population data for {}'.format(country['country']))
                country['totalPopulation'] = 0
        with open('./country_data.json', 'w') as json_file:
            json.dump(countries_dict, json_file)

def bands_per_capita():
    if exists('./country_data.json'):
        data = pd.read_csv('MA-bands.csv', index_col=0, keep_default_na=False)
        totals = data["CountryCode"].value_counts()
    
        with open('./country_data.json') as file:
            countries_dict = json.load(file)
            for country in countries_dict['countries']:
                try:
                    if totals[country['alpha2']] is not None and country['totalPopulation'] is not None:
                        country['totalBands'] = int(totals[country['alpha2']])
                        country['bandsPerCapita'] = totals[country['alpha2']] / country['totalPopulation']
                        country['bandsPer1kPeople'] = totals[country['alpha2']] / (country['totalPopulation']/1000)
                        country['bandsPer10kPeople'] = totals[country['alpha2']] / (country['totalPopulation']/10000)
                        country['bandsPer100kPeople'] = totals[country['alpha2']] / (country['totalPopulation']/100000)
                except:
                    print('Could not calculate bands per capita for {}'.format(country['country']))
                    country['totalBands'] = 0
                    country['bandsPerCapita'] = 0
                    country['bandsPer1kPeople'] = 0
                    country['bandsPer10kPeople'] = 0
                    country['bandsPer100kPeople'] = 0
            with open('./country_data.json', 'w') as json_file:
                json.dump(countries_dict, json_file)

def main(argv):
    calculation = ''
    try:
        opts, args = getopt.getopt(argv,"hc:o:")
    except getopt.GetoptError:
        print('usage: calculate.py -c <calculation>')
        sys.exit(2)
    if opts:
        for opt, arg in opts:
            if opt == '-h':
                print('calculate.py -c <calculation>')
                print('Available calculations: country_populations | bands_per_capita')
                sys.exit()
            elif opt in ("-c"):
                calculation = arg
                print ('Calculating: {}'.format(calculation))
                if calculation == 'country_populations':
                    country_populations()
                elif calculation == 'bands_per_capita':
                    bands_per_capita()
            else:
                print('usage: calculate.py -c <calculation>')
                sys.exit()
    else:
        print('usage: calculate.py -c <calculation>')
        print('Available calculations: country_populations | bands_per_capita')


if __name__ == "__main__":
   main(sys.argv[1:])
