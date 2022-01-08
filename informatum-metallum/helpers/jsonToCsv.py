import json
import csv
 
 
with open('../test.json') as json_file:
    data = json.load(json_file)
 
country_data = data['countries']
data_file = open('../test.csv', 'w')
csv_writer = csv.writer(data_file)
 
count = 0
 
for country in country_data:
    if count == 0:
        header = country.keys()
        csv_writer.writerow(header)
        count += 1
 
    csv_writer.writerow(country.values())
 
data_file.close()