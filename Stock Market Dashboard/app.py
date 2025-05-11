import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to fetch stock data
def fetch_stock_data():
    ticker = stock_entry.get().upper()
    if not ticker:
        messagebox.showerror("Error", "Please enter a stock ticker symbol!")
        return

    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        # Update stock information
        stock_name_label.config(text=f"Name: {stock_info.get('shortName', 'N/A')}")
        stock_price_label.config(text=f"Current Price: ${stock_info.get('regularMarketPrice', 'N/A')}")
        stock_high_label.config(text=f"Day High: ${stock_info.get('dayHigh', 'N/A')}")
        stock_low_label.config(text=f"Day Low: ${stock_info.get('dayLow', 'N/A')}")

        # Plot historical data
        plot_stock_data(ticker)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data for {ticker}. Please check the ticker symbol.")
        print(e)

# Function to plot stock data
def plot_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")  # Fetch 6 months of historical data

    # Clear the previous plot
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Create a new plot
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(hist.index, hist['Close'], label="Close Price", color="blue")
    ax.set_title(f"{ticker} Stock Price (Last 6 Months)", fontsize=12)
    ax.set_xlabel("Date", fontsize=10)
    ax.set_ylabel("Price (USD)", fontsize=10)
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Create the main Tkinter window
root = tk.Tk()
root.title("Stock Market Dashboard")
root.geometry("800x600")
root.configure(bg="#f0f4f7")

# Header
header_label = tk.Label(root, text="Stock Market Dashboard", font=("Arial", 20, "bold"), bg="#4CAF50", fg="white")
header_label.pack(fill=tk.X, pady=10)

# Stock Search Frame
search_frame = tk.Frame(root, bg="#f0f4f7")
search_frame.pack(pady=10)

stock_entry_label = tk.Label(search_frame, text="Enter Stock Ticker:", font=("Arial", 12), bg="#f0f4f7")
stock_entry_label.grid(row=0, column=0, padx=5)

stock_entry = tk.Entry(search_frame, font=("Arial", 12), width=15)
stock_entry.grid(row=0, column=1, padx=5)

search_button = tk.Button(search_frame, text="Search", font=("Arial", 12), bg="#4CAF50", fg="white", command=fetch_stock_data)
search_button.grid(row=0, column=2, padx=5)

# Stock Information Frame
info_frame = tk.Frame(root, bg="#f0f4f7", relief=tk.RIDGE, bd=2)
info_frame.pack(pady=10, fill=tk.X)

stock_name_label = tk.Label(info_frame, text="Name: N/A", font=("Arial", 12), bg="#f0f4f7")
stock_name_label.pack(anchor="w", padx=10)

stock_price_label = tk.Label(info_frame, text="Current Price: N/A", font=("Arial", 12), bg="#f0f4f7")
stock_price_label.pack(anchor="w", padx=10)

stock_high_label = tk.Label(info_frame, text="Day High: N/A", font=("Arial", 12), bg="#f0f4f7")
stock_high_label.pack(anchor="w", padx=10)

stock_low_label = tk.Label(info_frame, text="Day Low: N/A", font=("Arial", 12), bg="#f0f4f7")
stock_low_label.pack(anchor="w", padx=10)

# Chart Frame
chart_frame = tk.Frame(root, bg="#ffffff", relief=tk.RIDGE, bd=2)
chart_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Run the Tkinter main loop
root.mainloop()