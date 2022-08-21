from email import header
from http.client import responses
import time
import requests
import csv
import os
from dotenv import load_dotenv
import sys
load_dotenv()

output_folder = "output/"
access_token_array = os.getenv("ACCESS_TOKEN_ARRAY")
access_token_array = access_token_array.split(",")
print(access_token_array)

def collect_tweets(name, query, token_num=0):
    query = {
        "start_time": "2022-01-01T00:00:00-00:00",
        "end_time": "2022-03-31T00:00:00-00:00",
        "query": f"{query} lang:en -is:retweet",
        "max_results": "500"
    }

    headers = {'Authorization' : f'Bearer {access_token_array[token_num]}'}
    with open(os.path.join(f"{output_folder}", f'{name}.csv'), 'w+', newline='') as csvfile:
        fieldnames = ['id', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        response = requests.get("https://api.twitter.com/2/tweets/search/all", params=query, headers=headers).json()
        request_i = 1
        while "title" in response:
            if response["title"] ==  "Too Many Requests":
                time.sleep(request_i)
                response = requests.get("https://api.twitter.com/2/tweets/search/all", params=query, headers=headers).json()
                request_i += 1
            elif response["title"] ==  'UsageCapExceeded':
                time.sleep(request_i)
                print(response)
                token_num += 1
                try:
                    headers = {'Authorization' : f'Bearer {access_token_array[token_num]}'}
                except:
                    sys.exit("All tokens used up.")
                response = requests.get("https://api.twitter.com/2/tweets/search/all", params=query, headers=headers).json()
                

        try:
            next_token = response["meta"]["next_token"]
        except:
            next_token = None


        try:
            for row in response["data"]:
                writer.writerow(row)
        except:
            print(response)
            return

        i = len(response["data"])
        print(f"Fetching {name} tweets...")
        print(f"Number of fetched {name} tweets:", i)

        while next_token:
            time.sleep(2)
            query["next_token"] = next_token
            request_i = 1
            response = requests.get("https://api.twitter.com/2/tweets/search/all", params=query, headers=headers).json()
            while "title" in response:
                if response["title"] == "Too Many Requests":
                    time.sleep(request_i)
                    response = requests.get("https://api.twitter.com/2/tweets/search/all", params=query, headers=headers).json()
                    request_i += 1
                elif response["title"] == 'UsageCapExceeded':
                    time.sleep(request_i)
                    token_num += 1
                    try:
                        headers = {'Authorization' : f'Bearer {access_token_array[token_num]}'}
                    except:
                        sys.exit("All tokens used up.")
                    response = requests.get("https://api.twitter.com/2/tweets/search/all", params=query, headers=headers).json()
            try:
                next_token = response["meta"]["next_token"]
            except:
                next_token = None
            try:
                i += len(response["data"])
            except:
                print(response)
                break
            print(f"Number of fetched {name} tweets:", i)
            for row in response["data"]:
                try:
                    writer.writerow(row)
                except:
                    writer.writerow({
                        'id': row['id'],
                        'text': row['text']
                    })

        print(f"Finish fetching {name} tweets.")
    return token_num

def process_query(raw):
    query = raw.split("|")
    query_delim = " OR "
    for i, term in enumerate(query):
        term = term.strip()
        query[i] = term
    
    return query[0].lower(), query_delim.join(query)

if __name__ == "__main__":
    token_num = 0
    with open('fortune500.csv', 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name, query = process_query(row[0])
            if os.path.exists(os.path.join(f"{output_folder}", f'{name}.csv')):
                print(f'{name} tweets already exist.')
                continue
            token_num = collect_tweets(name, query, token_num=token_num)
            time.sleep(2)