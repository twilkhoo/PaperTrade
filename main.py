import customtkinter
from functions import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
  def __init__(self):
    super().__init__()
    self.title("PaperTrade")
    self.geometry("1200x800")
    self.resizable(False, False)

    label = customtkinter.CTkLabel(master=self, text="PaperTrade", font=customtkinter.CTkFont(size=40, weight="bold"))
    # label.pack(padx=50, pady=50)
    label.grid(row=0, column=0, padx=25, pady=25, sticky="W")

    tabView = customtkinter.CTkTabview(master=self, width=1000, height=600)
    tabView.grid(row=1, column=0, columnspan=3, padx=100)
    tabView.add("Stocks")
    tabView.add("ETFs")
    tabView.add("Options")
    tabView.add("Crypto")
    tabView.add("Settings")

if __name__ == "__main__":
  app = App()
  app.mainloop()
