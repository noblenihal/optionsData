import requests
from time import sleep
import datetime
import timeit
# we may need proxy rotation at some point when the apiCalls/minute will increase

session = requests.Session()

url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

originalURL = "https://www.nseindia.com/option-chain"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "DNT": "1",
}

request = session.get(originalURL, headers=headers, timeout=5)

cookies = dict(request.cookies)


def extract():

    global session, cookies
    response = requests.get(url, headers=headers, cookies=cookies, timeout=25)
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
    print(timeStamp)

    # code for inserting into database after checking
    # the current timestamp with previous timestamp
    # so that there is no duplicate data


totalTime = 0
while(totalTime <= 25200):  # 25200 secs = 7 hours
    waitTime = 7
    extract()
    totalTime += waitTime
    sleep(waitTime)
