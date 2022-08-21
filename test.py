import csv
from fetch_tweets import process_query
import os

output_folder = "output/"
switch = False
with open('fortune500.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        name, query = process_query(row[0])
        if name == "apple":
            switch = True
        if os.path.exists(os.path.join(f"{output_folder}", f'{name}.csv')):
            if not switch:
                print(f'{name} tweets already exist.')
            else:
                os.remove(os.path.join(f"{output_folder}", f'{name}.csv'))