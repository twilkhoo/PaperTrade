import customtkinter
import functions

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):

  currentAmount = 0

  def __init__(self):
    super().__init__()
    self.title("PaperTrade")
    self.geometry("1200x800")
    self.resizable(False, False)

    # General callback functions.
    def refetchAll():
      functions.fetchEverything()

    def refetchCurrentAmount(label):
      data = functions.fetchEverything()
      print(f"currentAmount: {data['currentAmount']}")
      label.configure(text=data["currentAmount"])

    # Title.
    title = customtkinter.CTkLabel(master=self, text="PaperTrade", font=customtkinter.CTkFont(size=40, weight="bold"))
    title.grid(row=0, column=0, padx=25, pady=25, sticky="W")

    # Tab setup.
    tabView = customtkinter.CTkTabview(master=self, width=1000, height=600)
    tabView.grid(row=1, column=0, columnspan=3, padx=100)
    tabView.add("Overview")
    tabView.add("Stocks")
    tabView.add("ETFs")
    tabView.add("Crypto")
    tabView.add("Settings")

    # Overview.
    overviewFrame = customtkinter.CTkFrame(master=tabView.tab("Overview"), width=900, height=500)
    overviewFrame.pack(padx=0, pady=20)
    overviewTitleLabel = customtkinter.CTkLabel(master=overviewFrame, text="Overview", font=customtkinter.CTkFont(size=30, weight="bold"))
    overviewTitleLabel.place(x=0, y=0)

    currentMoneyLabel = customtkinter.CTkLabel(master=overviewFrame, text=self.currentAmount, font=customtkinter.CTkFont(size=30, weight="bold"))
    currentMoneyLabel.place(x=0, y=100)

    refetchButton = customtkinter.CTkButton(master=overviewFrame, text="refetch", command=lambda: refetchCurrentAmount(currentMoneyLabel))
    refetchButton.place(x=0, y=300)























    # Settings.
    settingsFrame = customtkinter.CTkFrame(master=tabView.tab("Settings"), width=900, height=500)
    settingsFrame.pack(padx=0, pady=20)
    settingsTitleLabel = customtkinter.CTkLabel(master=settingsFrame, text="Settings", font=customtkinter.CTkFont(size=30, weight="bold"))
    settingsTitleLabel.place(x=0, y=0)

    addFundsLabel = customtkinter.CTkLabel(master=settingsFrame, text="Add funds", font=customtkinter.CTkFont(size=20))
    addFundsLabel.place(x=0, y=60)
    addFundsSubLabel = customtkinter.CTkLabel(master=settingsFrame, text="Want to feel like a millionare? Lost all your money already? No problem, add more funds here.", font=customtkinter.CTkFont(size=15))
    addFundsSubLabel.place(x=0, y=90)
    addFundsSubLabel2 = customtkinter.CTkLabel(master=settingsFrame, text="Note: this feature doesn't exist in the real world.", font=customtkinter.CTkFont(size=15))
    addFundsSubLabel2.place(x=0, y=120)
    addFundsEntry = customtkinter.CTkEntry(master=settingsFrame, placeholder_text="$X.XX")
    addFundsEntry.place(x=0, y=150)
    addFundsButton = customtkinter.CTkButton(master=settingsFrame, text="Add")
    addFundsButton.place(x=150, y=150)

    resetLabel = customtkinter.CTkLabel(master=settingsFrame, text="Reset", font=customtkinter.CTkFont(size=20))
    resetLabel.place(x=0, y=260)
    resetSubLabel = customtkinter.CTkLabel(master=settingsFrame, text="Reset all your data and start afresh.", font=customtkinter.CTkFont(size=15))
    resetSubLabel.place(x=0, y=290)
    resetSubLabel2 = customtkinter.CTkLabel(master=settingsFrame, text="WARNING: Irreversible. This also doesn't exist in the real world.", font=customtkinter.CTkFont(size=15))
    resetSubLabel2.place(x=0, y=320)
    addFundsButton = customtkinter.CTkButton(master=settingsFrame, text="Reset")
    addFundsButton.place(x=0, y=350)

    refetchAll()


if __name__ == "__main__":
  app = App()
  app.mainloop()
