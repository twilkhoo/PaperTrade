import os
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from threading import Thread
from queue import Queue

load_dotenv()
mongo_conn_str = os.getenv("MONGO_CONNECTION_STRING")
client = MongoClient(mongo_conn_str)
db = client.get_database("user")

def printProgress():
  start_time = time.time()
  while not fetched:
    elapsed_time = time.time() - start_time
    print(f"\r{elapsed_time:.2f}s elapsed...", end="", flush=True)
    time.sleep(0.1)


def fetchEverythingWorker(queue):
  print("Let's fetch everything.")
  print(f"\n{db.general.find_one()}")
  global fetched
  fetched = True
  queue.put(db.general.find_one())

def fetchEverything():
  resultQueue = Queue()

  global fetched
  fetched = False
  fetchThread = Thread(target=fetchEverythingWorker, args=(resultQueue,))
  printThread = Thread(target=printProgress)

  fetchThread.start()
  printThread.start()

  fetchThread.join()
  printThread.join()

  return resultQueue.get()


