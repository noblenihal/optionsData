from pandas.core.frame import DataFrame
import requests
from time import sleep
import pandas as pd
import datetime
from os import path

# we may need proxy rotation at some point when the apiCalls/minute will increase


# Cookie and session initialization
session = requests.Session()
originalURL = "https://www.nseindia.com/option-chain"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "DNT": "1",
}
request = session.get(originalURL, headers=headers, timeout=5)
cookies = dict(request.cookies)


def convertToCSV(df: DataFrame):
    today = datetime.datetime.now()
    date = today.strftime("%d-%b-%Y")

    if path.exists(f'OptionChain_{date}.csv'):
        df.to_csv(f'OptionChain_{date}.csv',
                  mode='a+', index=None, header=None)
        print("appending .. ")

    else:

        df.to_csv(f'OptionChain_{date}.csv',
                  mode='a+', index=None)
        print("first time ;)")


def jsonToDf(result):

    df = pd.json_normalize(  # Flattening the nested dictionaries and list
        result["records"],
        record_path=["data"],
        meta=["timestamp"]
    )

    # Finding next thursday
    today = datetime.datetime.now()

    if today.weekday() > 3:
        thursday = today + datetime.timedelta(days=-today.weekday()+3, weeks=1)
    else:
        thursday = today + datetime.timedelta(days=-today.weekday()+3)

    comingThursday = thursday.strftime("%d-%b-%Y")

    # Filtering data for upcoming expiry date i.e. coming thursday
    df = df[df['expiryDate'] == comingThursday]

    convertToCSV(df)


#global timestamp
gTime = "01-Dec-2021 15:30:00"


def extractChain(symbol):

    global session, cookies, gTime
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    response = session.get(url, headers=headers, cookies=cookies, timeout=25)
    print(response.status_code)

    if response.status_code == 401:
        session.close()
        session = requests.Session()

        request = session.get(originalURL, headers=headers, timeout=5)
        cookies = dict(request.cookies)
        response = requests.get(url, headers=headers,
                                cookies=cookies, timeout=25)
        print("cookie reset")

    result = response.json()

    timeStamp = result["records"]["timestamp"]
    if gTime == timeStamp:
        print("returning...")
        return

    gTime = timeStamp

    jsonToDf(result)


totalTime = 0
while(totalTime <= 25200):  # Ther
    waitTime = 15
    extractChain("NIFTY")
    totalTime += waitTime
    sleep(waitTime)
