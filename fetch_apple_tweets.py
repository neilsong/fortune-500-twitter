from email import header
import time
import requests
import csv
import os
from dotenv import load_dotenv
load_dotenv()

query = {
    "start_time": "2022-01-01T00:00:00-00:00",
    "end_time": "2022-03-31T00:00:00-00:00",
    "query": "apple lang:en -is:retweet",
    "max_results": "500"
}

headers = {'Authorization' : f'Bearer {os.getenv("ACCESS_TOKEN")}'}

with open('apple.csv', 'w+', newline='') as csvfile:
    fieldnames = ['id', 'text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    response = requests.get("https://api.twitter.com/2/tweets/search/all", params=query, headers=headers).json()
    next_token = response["meta"]["next_token"]


    for row in response["data"]:
        writer.writerow(row)

    i = len(response["data"])
    print("Fetching tweets...")
    print("Number of fetched tweets:", i )

    while next_token:
        time.sleep(1)
        query["next_token"] = next_token
        response = requests.get("https://api.twitter.com/2/tweets/search/all", params=query, headers=headers).json()
        try:
            next_token = response["meta"]["next_token"]
        except:
            next_token = None
        i += len(response["data"])
        print("Number of fetched tweets:", i)
        for row in response["data"]:
            try:
                writer.writerow(row)
            except:
                writer.writerow({
                    'id': row['id'],
                    'text': row['text']
                })

    print("Finish fetching tweets.")