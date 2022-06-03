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

    def show_wallet_menu(self):
        frame = WalletMenu(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_transaction_menu(self):
        frame = TransactionMenu(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Main Menu", font=("Arial", 40), fg="black").pack()

        tk.Label(self, text="").pack() #space

        btn_price = tk.Button(self, text="Price", command=lambda: controller.show_price_menu())
        btn_price.pack()
        btn_wallet = tk.Button(self, text="Wallet", command=lambda: controller.show_wallet_menu())
        btn_wallet.pack()

        tk.Label(self, text="").pack() #space

        tk.Button(self, text="Quit", command=lambda: controller.destroy()).pack()




class PriceMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Price Menu", font=("Arial", 40), fg="black").pack()

        tk.Label(self, text="").pack() #space

        f = open("currency.txt", "r")
        while True:
            line = f.readline()
            if not line:
                f.close()
                break
            line = line.replace("\n", "")
            tk.Button(self, text=line, command=lambda currency=line: controller.show_print_menu(
                tk.Label(controller, text=controller.get_price(currency), font=("Arial", 40), fg="black"),
                tk.Label(controller, text=controller.get_24h_change(currency), font=("Arial", 40), fg="black")
            )).pack()



class WalletMenu(tk.Frame):
    def __init__(self, parent, controller):
        total = 0
        change24h = 0
        change7d = 0
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Wallet", font=("Arial", 40), fg="black").pack()

        tk.Label(self, text="", font=("Arial", 20), fg="black").pack() #space

        tk.Label(self, text="Total: " + str(total), font=("Arial", 40), fg="black").pack()
        tk.Label(self, text="24h change: " + str(change24h), font=("Arial", 40), fg="black").pack()
        tk.Label(self, text="7d change: " + str(change7d), font=("Arial", 40), fg="black").pack()

        tk.Label(self, text="", font=("Arial", 20), fg="black").pack() #space

        tk.Button(self, text="Add transaction", command=lambda: controller.show_transaction_menu()).pack()

        tk.Label(self, text="", font=("Arial", 20), fg="black").pack() #space

        tk.Button(self, text="Back", command=lambda: controller.show_main_menu()).pack()


class TransactionMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="New transaction", font=("Arial", 40), fg="black").pack()

        tk.Label(self, text="", font=("Arial", 20), fg="black").pack() #space

        tk.Label(self, text="From:", font=("Arial", 10), fg="black").pack()
        self.from_currency = tk.Entry(self)
        self.from_currency.pack()

        tk.Label(self, text="", font=("Arial", 5), fg="black").pack()  # space

        tk.Label(self, text="Amount($):", font=("Arial", 10), fg="black").pack()
        self.amount = tk.Entry(self)
        self.amount.pack()

        tk.Label(self, text="", font=("Arial", 5), fg="black").pack()  # space

        tk.Label(self, text="To:", font=("Arial", 10), fg="black").pack()
        self.to_currency = tk.Entry(self)
        self.to_currency.pack()

        tk.Label(self, text="", font=("Arial", 5), fg="black").pack()  # space

        tk.Label(self, text="At:", font=("Arial", 10), fg="black").pack()
        self.price = tk.Entry(self)
        self.price.pack()

        tk.Label(self, text="", font=("Arial", 5), fg="black").pack()  # space

        self.calcLabel = tk.Label(self, text="0", font=("Arial", 5), fg="black")
        self.calcLabel.pack()

        self.update_calcLabel()

        tk.Button(self, text="Add", command=lambda amount=self.amount, from_currency=self.from_currency, to_currency=self.to_currency, price=self.price: self.add_transaction(
            amount, from_currency, to_currency, price
        )).pack()

        tk.Button(self, text="Back", command=lambda: controller.show_wallet_menu()).pack()

        '''-----------------------------------------------------'''

        f = open("transaction.txt", "r")
        lines = []
        while True:
            line = f.readline()
            if not line:
                f.close()
                break
            line = line.replace("\n", "")
            lines.append(line)

        while len(lines) > 0:
            line = lines.pop(len(lines)-1)
            tk.Label(self, text=line).pack()

    def add_transaction(self, amount, from_currency, to_currency, price):
        f = open("transaction.txt", "a")
        data = amount.get() + " " + from_currency.get() + " to " + price.get() + " " + to_currency.get() + "\n"
        f.write(data)
        f.close()
        '''tk.Label(self, text=data).pack()'''
        self.controller.show_transaction_menu()



    def update_calcLabel(self):
        if self.amount.get() == "" or self.price.get() == "":
            self.calcLabel.config(text="0")
        else:
            try:
                float(self.amount.get())
                float(self.price.get())
                calc = float(self.amount.get()) / float(self.price.get())
                calc = str(calc)
                self.calcLabel.config(text=calc)
            except ValueError:
                self.calcLabel.config(text="0")
        self.calcLabel.after(1, self.update_calcLabel)

class PrintMenu(tk.Frame):
    def __init__(self, *args, parent):
        tk.Frame.__init__(self, parent)
        for arg in args:
            for foo in arg:
                foo.pack()

app = App()
app.mainloop()