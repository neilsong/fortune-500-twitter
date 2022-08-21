# Fortune 500 Tweet Extraction

This repository contains the code for extracting tweets from the Fortune 500 companies. The code is written in Python 3.7. The code is written in a modular fashion so that it can be easily extended to extract tweets from other companies, just modify `fortune500.csv`

## Environment Setup
1. Make sure `conda` is installed
2. Run `./scripts/init_env.sh` to create the environment and install dependencies

## Fetch Tweets
1. Run `conda activate f500` to activate the environment
2. Run `python fetch_tweets.py` or `./scripts/nohup.sh` to fetch tweets
