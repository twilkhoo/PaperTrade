# PaperTrade
PaperTrade is a trading app (fake money) that uses the Mboum API for market information (real data).

# Features
Data is persisted in a MongoDB cluster. The GUI is made with CustomTKinter. Multithreading was used to have extra information logged to the terminal while fetching data (great for debugging), and to ensure long calls don't block the GUI.

# Usage
First, install some dependencies:
```
pip install customtkinter # The GUI
pip install dotenv # Environment Vars
pip install pymongo # MongoDB API for python
pip install requests # HTTP requests library
```

Then create a `.env` file at the root. Set `MONGO_CONNECTION_STRING` to a connection string of a blank MongoDB cluster, and `MBOUM_API_KEY` to a MBOUM API key.

Finally, run `python main.py` in a terminal.

# Images

# Next Steps
- Add an options tab.

Mboum does have an options REST endpoint, but integrating it with this app would be slightly different. To ensure strike prices are detected accordingly and expiration dates aren't missed, it would be important to have the option to keep this app running as a background process/thread. Historical data calls (as what's being done right now) would require several polls on startup to ensure we didn't miss reaching a strike price.

Currently, multithreading is used only for the API calls and MongoDB fetches, but we can set the main thread to be a daemon, polling Mboum routinely instead of polling several times on launch. To avoid polling entirely, we could alternatively use some websocket interface (not Mboum).

- Dockerize

It would be nice to keep the same database across all users of this app (which would imply restructuring the DB slightly to account for multiple users), but this would be easier and safer after dockerizing.

