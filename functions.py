import os
import time
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from threading import Thread
from queue import Queue

# Loading env vars and connecting to Mongo.
load_dotenv()
mongo_conn_str = os.getenv("MONGO_CONNECTION_STRING")
client = MongoClient(mongo_conn_str)
db = client.get_database("user")


# According to the Mboum API, stocks, indexes/etfs are fetched simply using the ticker (e.g. AAPL), cryptocurrency appends a -USD (e.g. BTC-USD).
def mboumQuoteStr(symbols):
    return f"https://mboum.com/api/v1/qu/quote/?symbol={','.join(symbols)}&apikey={os.getenv('MBOUM_API_KEY')}"


# Printing thread.
def printProgress():
    start_time = time.time()
    while not fetched:
        elapsed_time = time.time() - start_time
        print(f"\r{elapsed_time:.2f}s elapsed...", end="", flush=True)
        time.sleep(0.1)


# Wrapper for threads we can time.
def runWhilePrinting(func):
    resultQueue = Queue()
    global fetched
    fetched = False
    runThread = Thread(target=func, args=(resultQueue,))
    printThread = Thread(target=printProgress)
    runThread.start()
    printThread.start()
    runThread.join()
    printThread.join()
    return resultQueue.get()


# Fetching all current data in Mongo.
def fetchEverything():
    def fetchEverythingWorker(queue):
        print("Let's fetch everything.")
        data = db.general.find_one()
        print(f"\n{data}")
        global fetched
        fetched = True
        queue.put(data)

    return runWhilePrinting(fetchEverythingWorker)


# Adding funds.
def addFunds(amountToAdd, currentAmount):
    newAmount = float(amountToAdd) + float(currentAmount)
    print(f"adding ${newAmount}")
    updateDoc = {"$set": {"startingAmount": newAmount}}
    result = db.general.update_one({}, updateDoc)
    print(result)


# Resetting funds.
def resetFunds():
    updateDoc = {"$set": {"startingAmount": 0.00}}
    result = db.general.update_one({}, updateDoc)
    print(result)


# Fetching data of specified tickers from Mboum, returned as a json object.
def fetchMboum(tickers):
    def fetchMboumWorker(queue):
        print(mboumQuoteStr(tickers))
        response = requests.get(mboumQuoteStr(tickers))
        if response.status_code == 200:
            print("Good fetch from Mboum")
            data = response.json()
            global fetched
            fetched = True
            queue.put(data)
        else:
            queue.put(f"Error {response.status_code}")

    return runWhilePrinting(fetchMboumWorker)


# Associating specified tickers with current prices, using Mboum, returning a dict.
def findCurrentPrices(tickers):
    currentPrices = {}
    currentData = fetchMboum(tickers)
    for result in currentData["data"]:
        currentPrices.update({result["symbol"]: result["regularMarketPrice"]})
    return currentPrices
