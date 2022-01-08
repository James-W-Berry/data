#! /usr/bin/env python
import sys, getopt
from bs4 import BeautifulSoup
import json
import pandas as pd

def country_populations():
    print('Calculating ranking by total populations')
    try:
        with open('./country_data.json') as file:
            countries_dict = json.load(file)
            sortedCountries = sorted(countries_dict['countries'], key = lambda i: i['totalPopulation'], reverse=True)
            for index, country in enumerate(sortedCountries):
                country['ranking'] = index + 1
            with open('./metrics/sortedby_population.json', 'w') as json_file:
                json.dump(sortedCountries, json_file)
        print('results stored in metrics/sortedby_population.json')
    except:
        print('Error occured while processing country data')


def bands_per_capita():
    print('Calculating ranking by bands per capita')
    try:
        with open('./country_data.json') as file:
            countries_dict = json.load(file)
            sortedCountries = sorted(countries_dict['countries'], key = lambda i: i['bandsPer100kPeople'], reverse=True)
            for index, country in enumerate(sortedCountries):
                country['ranking'] = index + 1
            with open('./metrics/sortedby_bands_per_capita.json', 'w') as json_file:
                json.dump(sortedCountries, json_file)
            print('results stored in metrics/sortedby_bands_per_capita.json')
    except:
        print('Error occured while processing country data')

def total_bands():
    print('Calculating ranking by total bands')
    try:
        with open('./country_data.json') as file:
            countries_dict = json.load(file)
            sortedCountries = sorted(countries_dict['countries'], key = lambda i: i['totalBands'], reverse=True)
            for index, country in enumerate(sortedCountries):
                country['ranking'] = index + 1
            with open('./metrics/sortedby_total_bands.json', 'w') as json_file:
                json.dump(sortedCountries, json_file)
            print('results stored in metrics/sortedby_total_bands.json')
    except:
        print('Error occured while processing country data')

def main(argv):
    metric = ''
    try:
        opts, args = getopt.getopt(argv,"hm:o:")
    except getopt.GetoptError:
        print('usage: results.py -m <metric>')
        sys.exit(2)
    if opts:
        for opt, arg in opts:
            if opt == '-h':
                print('results.py -m <metric>')
                print('Available metrics: country_populations | bands_per_capita')
                sys.exit()
            elif opt in ("-m"):
                metric = arg
                if metric == 'country_populations':
                    country_populations()
                elif metric == 'bands_per_capita':
                    bands_per_capita()
                elif metric == 'total_bands':
                    total_bands()
                elif metric == 'all':
                    country_populations()
                    bands_per_capita()
                    total_bands()
                else:
                    print('usage: results.py -c <metric>')
                    sys.exit()
            else:
                print('usage: results.py -c <metric>')
                sys.exit()
    else:
        print('usage: results.py -c <metric>')
        print('Available metrics: all | country_populations | bands_per_capita | total_bands')


if __name__ == "__main__":
   main(sys.argv[1:])
