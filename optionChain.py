import requests
import schedule
from time import sleep
import datetime
import timeit
# we may need proxy rotation at some point when the apiCalls/minute will increase


def extract():

    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Referer": "https://www.google.com",
        "DNT": "1",
    }

    response = requests.get(url, headers=headers, timeout=25)

    result = response.json()
    timeStamp = result["records"]["timestamp"]
    print(timeStamp)

    # code for inserting into database after checking
    # the current timestamp with previous timestamp
    # so that there is no duplicate data


totalTime = 0
while(totalTime <= 25200):  # 25200 secs = 7 hours
    waitTime = 60
    extract()
    totalTime += waitTime
    sleep(waitTime)
