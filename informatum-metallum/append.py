#! /usr/bin/env python
import os
from os.path import exists
import sys, getopt
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

 
def addGeojonBorders():
    if exists('./country_data.json'):
        with open('./country_data.json') as file:
            countries_dict = json.load(file)

            for country in countries_dict['countries']:
                try:
                    # if country['_geojson'] is None:
                    country['_geojson'] =  {
                        "type": "Feature",
                        "properties": {
                            "ADMIN": country['country'],
                            "ISO_A3": country['alpha3']
                        },
                            "geometry": {
                            "type": "MultiPolygon",
                            "coordinates": []
                        }
                    }
                except:
                    print('Could not add geojson field for '.format(country['country']))
                     
            with open('./country_data.json', 'w') as json_file:
                json.dump(countries_dict, json_file)

def addCountryMetrics():
    if exists('./countries.geojson') and exists('./country_data.json'):
        with open ('./country_data.json') as country_data:
            country_data_dict = json.load(country_data)

        with open('./countries.geojson') as geojson:
            geojson_dict = json.load(geojson) 
            for country in geojson_dict['features']:
                try:
                    for data in country_data_dict['countries']:
                        if country['properties']['ISO_A3'] is not None:
                            if country['properties']['ISO_A3'] == data['alpha3']:
                                country['properties']['totalPopulation'] = data['totalPopulation']
                                country['properties']['totalBands'] = data['totalBands']
                                country['properties']['bandsPerCapita'] = data['bandsPerCapita']
                                country['properties']['bandsPer10kPeople'] = data['bandsPer10kPeople']
                                country['properties']['bandsPer100kPeople'] = data['bandsPer100kPeople']
                                country['properties']['bandsPer1kPeople'] = data['bandsPer1kPeople'] 
                            else:
                                continue
                except:
                    print('Could not add country metrics')
        
        with open('./countries.geojson', 'w') as updatedGeojson:
                json.dump(geojson_dict, updatedGeojson)
    else:
        print('countries.geojson not found!')

def main(argv):
   # addGeojonBorders()
   addCountryMetrics()


if __name__ == "__main__":
   main(sys.argv[1:])
