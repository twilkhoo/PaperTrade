import customtkinter
import functions
import time
import threading
import mplcursors

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    #
    #
    # Local values of the data fetched from Mongo, to avoid refetches.
    #
    #

    # startingAmount is the amount the user has manually added.
    startingAmount = 1

    # current_ is of form {ticker: string => (amount: float, averagePrice: float, totalPrice: float, moneyInvested: float)}
    currentStocks = {}
    currentETFs = {}
    currentCrypto = {}

    # cashAvailable is the amount of money not invested (enforced to be >= 0 since we cannot invest < 0 dollars).
    cashAvailable = startingAmount - sum(
        sum(entry[3] for entry in data.values())
        for data in (currentStocks, currentETFs, currentCrypto)
    )

    # currentAmount totals the price of each stock with the amount of cash available.
    currentAmount = cashAvailable + sum(
        sum(entry[2] for entry in data.values())
        for data in (currentStocks, currentETFs, currentCrypto)
    )

    # percentUp is the percent gained (between starting and current).
    percentUp = f"{((currentAmount-startingAmount) / startingAmount) * 100}%"

    stocksValue = sum(entry[2] for entry in currentStocks.values())
    etfsValue = sum(entry[2] for entry in currentStocks.values())
    cryptoValue = sum(entry[2] for entry in currentStocks.values())

    # dailyPrices is the closing price of each day, form {date: string => amount: float}
    dailyPrices = {}

    #
    #
    # The main CustomTKinter Window.
    #
    #

    def __init__(self):
        super().__init__()
        self.title("PaperTrade")
        self.geometry("1200x800")
        self.resizable(False, False)

        #
        #
        # Top level functions used by multiple TKinter components.
        #
        #

        # Poll every 10 seconds for stock changes.
        def fetchPolling(stop):
            while not stop.is_set():
                print("Refetching (Polling)")
                refetchAll()
                time.sleep(10)

        # Adding funds.
        def actuallyAddFunds(amountToAdd, window):
            functions.addFunds(amountToAdd, self.currentAmount)
            window.destroy()

        def actuallyResetFunds(window):
            functions.resetFunds()
            window.destroy()

        # A function to handle all types of confirmation windows.
        def openConfirm(type, args):
            confirmWindow = customtkinter.CTkToplevel()
            confirmWindow.geometry("400x300")

            if type == "addFunds":
                amountToAdd = args[0]
                windowTitle = "Add funds?"
                windowLabel = f"Add ${amountToAdd}"
                confirmExec = lambda: actuallyAddFunds(amountToAdd, confirmWindow)

            if type == "reset":
                windowTitle = "Reset?"
                windowLabel = "Reset all data? DANGER: irreversible"
                confirmExec = lambda: actuallyResetFunds(confirmWindow)

            confirmWindow.title(windowTitle)
            confirmWindowInnerLabel = customtkinter.CTkLabel(
                master=confirmWindow,
                text=windowLabel,
                font=customtkinter.CTkFont(size=20),
            )
            confirmWindowInnerLabel.pack(padx=0, pady=50)
            confirmButton = customtkinter.CTkButton(
                master=confirmWindow, text="Confirm", command=confirmExec
            )
            confirmButton.place(x=50, y=100)
            cancelButton = customtkinter.CTkButton(
                master=confirmWindow,
                text="Cancel",
                fg_color="grey",
                command=lambda: confirmWindow.destroy(),
            )
            cancelButton.place(x=200, y=100)

        #
        #
        # Title.
        #
        #
        title = customtkinter.CTkLabel(
            master=self,
            text="PaperTrade",
            font=customtkinter.CTkFont(size=40, weight="bold"),
        )
        title.grid(row=0, column=0, padx=25, pady=25, sticky="W")

        #
        #
        # Tab Setup.
        #
        #
        tabView = customtkinter.CTkTabview(master=self, width=1000, height=600)
        tabView.grid(row=1, column=0, columnspan=3, padx=100)
        tabView.add("Overview")
        tabView.add("Stocks")
        tabView.add("ETFs")
        tabView.add("Crypto")
        tabView.add("Settings")

        #
        #
        # Overview.
        #
        #
        overviewFrame = customtkinter.CTkFrame(
            master=tabView.tab("Overview"), width=900, height=500
        )
        overviewFrame.pack(padx=0, pady=20)
        overviewTitleLabel = customtkinter.CTkLabel(
            master=overviewFrame,
            text="Overview",
            font=customtkinter.CTkFont(size=30, weight="bold"),
        )
        overviewTitleLabel.place(x=0, y=0)

        # self.currentAmount
        currentMoneyLabel = customtkinter.CTkLabel(
            master=overviewFrame,
            text=f"{self.currentAmount}",
            font=customtkinter.CTkFont(size=30, weight="bold"),
        )
        currentMoneyLabel.place(x=0, y=100)

        currentMoneyLabel = customtkinter.CTkLabel(
            master=overviewFrame,
            text="Current Value",
            font=customtkinter.CTkFont(size=15),
        )
        currentMoneyLabel.place(x=0, y=140)

        startingMoneyLabel = customtkinter.CTkLabel(
            master=overviewFrame,
            text=f"Starting amount: {self.startingAmount}",
            font=customtkinter.CTkFont(size=20),
        )
        startingMoneyLabel.place(x=0, y=200)

        percentLabel = customtkinter.CTkLabel(
            master=overviewFrame,
            text=f"Percent up/down: {self.percentUp}",
            font=customtkinter.CTkFont(size=20),
        )
        percentLabel.place(x=0, y=250)

        stocksValueLabel = customtkinter.CTkLabel(
            master=overviewFrame,
            text=f"Stocks amount: {self.stocksValue}",
            font=customtkinter.CTkFont(size=20),
        )
        stocksValueLabel.place(x=0, y=300)

        etfsValueLabel = customtkinter.CTkLabel(
            master=overviewFrame,
            text=f"ETFs amount: {self.etfsValue}",
            font=customtkinter.CTkFont(size=20),
        )
        etfsValueLabel.place(x=0, y=350)

        cryptoValueLabel = customtkinter.CTkLabel(
            master=overviewFrame,
            text=f"Crypto amount: {self.cryptoValue}",
            font=customtkinter.CTkFont(size=20),
        )
        cryptoValueLabel.place(x=0, y=400)

        # Displaying historical ending amounts using matplotlib.
        dates = list(self.dailyPrices.keys())
        values = list(self.dailyPrices.values())

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(6.25, 4))
        ax.plot(dates, values, marker="o")  # Plot the data
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.set_title("Daily Prices")
        ax.set_xticks([dates[0], dates[-1]])

        cursor = mplcursors.cursor(ax, hover=True)
        cursor.connect(
            "add", lambda sel: sel.annotation.set_text(f"Amount: {sel.target[1]:.2f}")
        )
        canvas = FigureCanvasTkAgg(fig, master=overviewFrame)
        canvas.draw()
        canvas.get_tk_widget().place(x=300, y=50)

        #
        #
        # Settings.
        #
        #
        settingsFrame = customtkinter.CTkFrame(
            master=tabView.tab("Settings"), width=900, height=500
        )
        settingsFrame.pack(padx=0, pady=20)
        settingsTitleLabel = customtkinter.CTkLabel(
            master=settingsFrame,
            text="Settings",
            font=customtkinter.CTkFont(size=30, weight="bold"),
        )
        settingsTitleLabel.place(x=0, y=0)

        addFundsLabel = customtkinter.CTkLabel(
            master=settingsFrame, text="Add funds", font=customtkinter.CTkFont(size=20)
        )
        addFundsLabel.place(x=0, y=60)
        addFundsSubLabel = customtkinter.CTkLabel(
            master=settingsFrame,
            text="Want to feel like a millionare? Lost all your money already? No problem, add more funds here.",
            font=customtkinter.CTkFont(size=15),
        )
        addFundsSubLabel.place(x=0, y=90)
        addFundsSubLabel2 = customtkinter.CTkLabel(
            master=settingsFrame,
            text="Note: this feature doesn't exist in the real world.",
            font=customtkinter.CTkFont(size=15),
        )
        addFundsSubLabel2.place(x=0, y=120)
        addFundsEntry = customtkinter.CTkEntry(
            master=settingsFrame, placeholder_text="$X.XX"
        )
        addFundsEntry.place(x=0, y=150)
        addFundsButton = customtkinter.CTkButton(
            master=settingsFrame,
            text="Add",
            command=lambda: openConfirm("addFunds", [addFundsEntry.get()]),
        )
        addFundsButton.place(x=150, y=150)

        resetLabel = customtkinter.CTkLabel(
            master=settingsFrame, text="Reset", font=customtkinter.CTkFont(size=20)
        )
        resetLabel.place(x=0, y=260)
        resetSubLabel = customtkinter.CTkLabel(
            master=settingsFrame,
            text="Reset all your data and start afresh.",
            font=customtkinter.CTkFont(size=15),
        )
        resetSubLabel.place(x=0, y=290)
        resetSubLabel2 = customtkinter.CTkLabel(
            master=settingsFrame,
            text="WARNING: Irreversible. This also doesn't exist in the real world.",
            font=customtkinter.CTkFont(size=15),
        )
        resetSubLabel2.place(x=0, y=320)
        addFundsButton = customtkinter.CTkButton(
            master=settingsFrame, text="Reset", command=lambda: openConfirm("reset", [])
        )
        addFundsButton.place(x=0, y=350)

        #
        #
        # General callback functions requiring components to be instantiated.
        #
        #
        # Refetching all data from Mboum and Mongo.
        def refetchAll():
            data = functions.fetchEverything()
            self.startingAmount = data["startingAmount"]
            self.currentAmount = data["currentAmount"]
            # currentMoneyLabel.configure(text=self.currentAmount)

        # Manual refetch.
        refetchButton = customtkinter.CTkButton(
            master=overviewFrame, text="refetch", command=refetchAll
        )
        refetchButton.place(x=0, y=450)

        # Logic to shutdown gracefully (for polling).
        stop = threading.Event()

        def on_closing():
            stop.set()
            fig.clf()
            plt.close(fig)
            app.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)

        # Fetch on load.
        refetchAll()

        # Begin the polling thread.
        thread = threading.Thread(target=fetchPolling, args=(stop,))
        thread.start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
