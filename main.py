import tkinter
import tkinter as tk
from pycoingecko import CoinGeckoAPI
import json


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("My Screener")
        self.geometry("1080x720")  # taille
        self.minsize(500, 300)  # taille minimal
        self.container = tkinter.Frame(self)
        self.container.pack()
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.api = CoinGeckoAPI()
        self.show_main_menu()

    def get_price(self, symbol):
        print(symbol)
        price = self.api.get_price(ids=symbol, vs_currencies='usd', include_24hr_change=True)
        return f"price = {price[symbol]['usd']}"
    def get_24h_change(self, symbol):
        change = self.api.get_price(ids=symbol, vs_currencies='usd', include_24hr_change=True)
        s = ""
        if(change[symbol]['usd_24h_change'] >= 0):
            s = '+'
        return f"24h change: {s}{change[symbol]['usd_24h_change']}%"

    def show_main_menu(self):
        frame = MainMenu(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_price_menu(self):
        frame = PriceMenu(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_print_menu(self, *args):
        frame = PrintMenu(args, parent=self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        btn_price = tk.Button(self, text="Price", command=lambda: controller.show_price_menu())
        btn_price.pack()

class PriceMenu(tk.Frame):
    def __init__(self, parent, controller):
        #self.read_currency_file(controller)
        tk.Frame.__init__(self, parent)
        f = open("currency.txt", "r")
        while True:
            line = f.readline()
            if not line:
                f.close()
                break
            line = line.replace("\n", "")
            btn = tk.Button(self, text=line, command=lambda currency=line: controller.show_print_menu(
                tk.Label(controller, text=controller.get_price(currency), font=("Arial", 40), fg="black"),
                tk.Label(controller, text=controller.get_24h_change(currency), font=("Arial", 40), fg="black")
            ))
            btn.pack()


class PrintMenu(tk.Frame):
    def __init__(self, *args, parent):
        tk.Frame.__init__(self, parent)
        for arg in args:
            for foo in arg:
                foo.pack()

app = App()
app.mainloop()