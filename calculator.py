import math
import tkinter as tk
from tkinter import messagebox, Toplevel
from tkcalendar import Calendar
from datetime import datetime
from scipy.stats import norm

def calendaropen():
    def dateset():
        selected_date = cal.get_date()
        entry_T.delete(0,tk.END)
        entry_T.insert(0, selected_date)
        top.destroy()

    top = Toplevel(root)
    top.title("Expiry Date")
    cal = Calendar(top,selectmode='day',year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)
    cal.pack(pady=20)
    tk.Button(top,text="Select",command=dateset).pack()

def calculate():
    try:
        S = float(entry_S.get())
        K = float(entry_K.get())
        R = entry_R.get()
        Vol =  entry_Vol.get()

        # Convert R and Vol into percentage
        if R.isdigit():
            R = float(R)/100
        else:
            R = float(R)

        if Vol.isdigit():
            Vol = float(Vol)/100
        else:
            Vol = float(Vol)

        expiry_date = entry_T.get()
        expiry_datetime = datetime.strptime(expiry_date,"%m/%d/%y")
        today_datetime = datetime.today()
        T = (expiry_datetime - today_datetime).days / 365
        time = (expiry_datetime - today_datetime).days
        d1 = (math.log(S/K) + (R + 0.5 * Vol**2)*T) / (Vol * math.sqrt(T))
        d2 = d1 - (Vol*math.sqrt(T))
        Call_Price = S * norm.cdf(d1) - K * math.exp(-R*T) * norm.cdf(d2)
        Put_Price = K * math.exp(-R*T)* norm.cdf(-d2) - S * norm.cdf(-d1)

        result_label.config(text=f"Call Price: {Call_Price:.4f}\nPut Price: {Put_Price:.4f}\n Days to Expiry:{time} days")
    except ValueError:
        messagebox.showerror("Error Input","Please Enter the Valid Numbers.")

def refresh():
    entry_S.delete(0, tk.END)
    entry_K.delete(0, tk.END)
    entry_R.delete(0, tk.END)
    entry_Vol.delete(0, tk.END)
    entry_T.delete(0, tk.END)
    result_label.config(text="")


#GUI Setup
root = tk.Tk()
root.title("Black-Scholes Option Pricing Model")


tk.Label(root, text="Spot Price:").grid(row=0,column=0)
tk.Label(root, text="Strike Price:").grid(row=1,column=0)
tk.Label(root, text="risk Free Rate:").grid(row=2,column=0)
tk.Label(root, text="Volatility:").grid(row=3,column=0)
tk.Label(root, text="Expiry Date:").grid(row=4,column=0)

entry_S = tk.Entry(root)
entry_K = tk.Entry(root)
entry_R = tk.Entry(root)
entry_Vol = tk.Entry(root)
entry_T = tk.Entry(root)
entry_T.bind("<Button-1>",lambda event: calendaropen())

entry_S.grid(row=0,column=1)
entry_K.grid(row=1,column=1)
entry_R.grid(row=2,column=1)
entry_Vol.grid(row=3,column=1)
entry_T.grid(row=4,column=1)

calculate_button = tk.Button(root,text="Calculate",command=calculate)
calculate_button.grid(row=5, column=0, columnspan=2)

refresh_button = tk.Button(root, text="Refresh", command=refresh)
refresh_button.grid(row=6, column=0, columnspan=2)

result_label = tk.Label(root,text="")
result_label.grid(row=5, column=0, columnspan=2)

root.mainloop()