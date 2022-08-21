# function to open every csv file in output and print the number of lines in each file

import os
import csv

def lines_per_csv():
    for file in os.listdir("output"):
        if file.endswith(".csv"):
            with open(os.path.join("output", file), 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                print(f"{file[:-3]},{len(data)}")

lines_per_csv()