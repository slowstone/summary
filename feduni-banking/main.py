import tkinter as tk
from tkinter import messagebox

from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bankaccount import BankAccount

win = tk.Tk()
# Set window size here to '440x640' pixels
win.geometry("440x640")
# Set window title here to 'FedUni Banking'
win.winfo_toplevel().title("FedUni Banking")

# The account number entry and associated variable
account_number_var = tk.StringVar()
account_number_entry = tk.Entry(win, textvariable=account_number_var)
account_number_entry.focus_set()

# The pin number entry and associated variable.
# Note: Modify this to 'show' PIN numbers as asterisks (i.e. **** not 1234)
pin_number_var = tk.StringVar()
account_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var, show='*')

# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry = tk.Entry(win)

# The transaction text widget holds text of the accounts transactions
transaction_text_widget = tk.Text(win, height=10, width=48)
# The bank account object we will work with
account = BankAccount()

# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry(event):
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    # Clear the pin number entry here
    account_pin_entry.delete(0,'end')

def handle_pin_button(event):
    '''Function to add the number of the button clicked to the PIN number entry via its associated variable.'''    

    # Limit to 4 chars in length
    try:
        ss = pin_number_var.get()
        if len(ss) > 3:
            raise Exception("Limit to 4 chars in the length of PIN")
    # Set the new pin number on the pin_number_var
        ss = pin_number_var.get()
        ss = ss + event.widget['text']
        pin_number_var.set(ss)
    except Exception as e:
        tk.messagebox.showwarning('Warming', e)

def log_in(event):
    '''Function to log in to the banking system using a known account number and PIN.'''
    global account
    global pin_number_var
    global account_num_entry

    # Create the filename from the entered account number with '.txt' on the end
    filename = account_number_var.get() + ".txt"
    # Try to open the account file for reading
    try:
        # Open the account file for reading
        account_file = open(filename, "r")
        # First line is account number
        account.account_number = int(account_file.readline()[:-1])
        # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read
        if account_file.readline()[:-1] != pin_number_var.get():
            raise Exception
        account.pin_number = pin_number_var.get()
        # Read third and fourth lines (balance and interest rate) 
        account.balance = float(account_file.readline()[:-1])
        account.interest_rate = float(account_file.readline()[:-1])
        # Section to read account transactions from file - start an infinite 'do-while' loop here
        for line in account_file:
            # Attempt to read a line from the account file, break if we've hit the end of the file. If we
            # read a line then it's the transaction type, so read the next line which will be the transaction amount.
            # and then create a tuple from both lines and add it to the account's transaction_list
            order = line.replace('\n', '')
            value = account_file.readline().replace('\n', '')
            account.transaction_list.append((order, value))
        # Close the file now we're finished with it
        account_file.close()
    # Catch exception if we couldn't open the file or PIN entered did not match account PIN
    except Exception as e:
        # Show error messagebox and & reset BankAccount object to default...
        tk.messagebox.showwarning('Warming', "Invalid account number - please try again!")
        #  ...also clear PIN entry and change focus to account number entry
        account_number_entry.delete(0, 'end')
        account_pin_entry.delete(0, 'end')
        account_number_entry.focus_set()
    # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen
    else:
        remove_all_widgets()
        create_account_screen()

# ---------- Button Handlers for Account Screen ----------

def save_and_log_out():
    '''Function  to overwrite the account file with the current state of
       the account object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global account

    # Save the account with any new transactions
    account.save_to_file()
    # Reset the bank acount object
    account = BankAccount()
    # Reset the account number and pin to blank
    account_number_var.set('')
    pin_number_var.set('')
    # Remove all widgets and display the login screen again
    remove_all_widgets()
    create_login_screen()

def perform_deposit():
    '''Function to add a deposit for the amount in the amount entry to the
       account's transaction list.'''
    global account    
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    try:
        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        value = amount_entry.get()
        # Deposit funds
        account.deposit_funds(value)
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        transaction_text_widget.config(state='normal')
        transaction_text_widget.delete(0.0, 'end')
        transaction_text_widget.insert('end', account.get_transaction_string())
        transaction_text_widget.config(state='disabled')
        # Change the balance label to reflect the new balance
        balance_var.set("Balance: $"+str(account.balance))
        # Clear the amount entry
        amount_entry.delete(0, 'end')
        # Update the interest graph with our new balance
        plot_interest_graph()
    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
    except Exception as e:
        tk.messagebox.showwarning('Warming', e)

def perform_withdrawal():
    '''Function to withdraw the amount in the amount entry from the account balance and add an entry to the transaction list.'''
    global account    
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    try:
        # Get the cash amount to deposit. Note: We check legality inside account's withdraw_funds method
        value = amount_entry.get()
        # Withdraw funds        
        account.withdraw_funds(value)
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        transaction_text_widget.config(state='normal')
        transaction_text_widget.delete(0.0, 'end')
        transaction_text_widget.insert('end', account.get_transaction_string())
        transaction_text_widget.config(state='disabled')
        # Change the balance label to reflect the new balance
        balance_var.set("Balance: $"+str(account.balance))
        # Clear the amount entry
        amount_entry.delete(0, 'end')
        # Update the interest graph with our new balance
        plot_interest_graph()
    # Catch and display any returned exception as a messagebox 'showerror'
    except Exception as e:
        tk.messagebox.showwarning('Warming', e)

# ---------- Utility functions ----------

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_account_file():
    '''Function to read a line from the accounts file but not the last newline character.
       Note: The account_file must be open to read from for this function to succeed.'''
    global account_file
    return account_file.readline()[0:-1]

def plot_interest_graph():
    '''Function to plot the cumulative interest for the next 12 months here.'''

    # YOUR CODE to generate the x and y lists here which will be plotted
    value_add = account.balance * account.interest_rate / 12
    x = [1,2,3,4,5,6,7,8,9,10,11,12]
    y = [account.balance+value_add*1, account.balance+value_add*2, account.balance+value_add*3,
         account.balance+value_add*4, account.balance+value_add*5, account.balance+value_add*6,
         account.balance+value_add*7, account.balance+value_add*8, account.balance+value_add*9,
         account.balance+value_add*10, account.balance+value_add*11, account.balance+value_add*12
         ]

    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    figure = Figure(figsize=(5, 2), dpi=100)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)
    a.plot(x, y, marker='o')
    a.grid()
    
    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='nsew')


# ---------- UI Screen Drawing Functions ----------

def create_login_screen():
    '''Function to create the login screen.'''    

    # ----- Row 0 -----
    # 'FedUni Banking' label here. Font size is 32.
    tk.Label(win, text="FedUni BanKing", font="Helvetica 32 bold").grid(row=0, columnspan=5, sticky='nsew')

    # ----- Row 1 -----
    # Acount Number / Pin label here
    tk.Label(win, text="Account Number/PIN", justify='left').grid(row=1, column=0, sticky='nsew')
    # Account number entry here
    account_number_entry.grid(row=1, column=1, columnspan=2, sticky='nsew')
    # Account pin entry here
    account_pin_entry.grid(row=1, column=3, columnspan=2, sticky='nsew')

    # ----- Row 2 -----
    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    Button_tmp = tk.Button(win, text="1")
    Button_tmp.bind('<Button-1>',handle_pin_button)
    Button_tmp.grid(row=2, column=0, sticky='nsew')
    Button_tmp = tk.Button(win, text="2")
    Button_tmp.bind('<Button-1>', handle_pin_button)
    Button_tmp.grid(row=2, column=1, columnspan=2, sticky='nsew')
    Button_tmp = tk.Button(win, text="3")
    Button_tmp.bind('<Button-1>', handle_pin_button)
    Button_tmp.grid(row=2, column=3, columnspan=2, sticky='nsew')

    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    Button_tmp = tk.Button(win, text="4")
    Button_tmp.bind('<Button-1>', handle_pin_button)
    Button_tmp.grid(row=3, column=0, sticky='nsew')
    Button_tmp = tk.Button(win, text="5")
    Button_tmp.bind('<Button-1>', handle_pin_button)
    Button_tmp.grid(row=3, column=1, columnspan=2, sticky='nsew')
    Button_tmp = tk.Button(win, text="6")
    Button_tmp.bind('<Button-1>', handle_pin_button)
    Button_tmp.grid(row=3, column=3, columnspan=2, sticky='nsew')

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    Button_tmp = tk.Button(win, text="7")
    Button_tmp.bind('<Button-1>', handle_pin_button)
    Button_tmp.grid(row=4, column=0, sticky='nsew')
    Button_tmp = tk.Button(win, text="8")
    Button_tmp.bind('<Button-1>', handle_pin_button)
    Button_tmp.grid(row=4, column=1, columnspan=2, sticky='nsew')
    Button_tmp = tk.Button(win, text="9")
    Button_tmp.bind('<Button-1>', handle_pin_button)
    Button_tmp.grid(row=4, column=3, columnspan=2, sticky='nsew')

    # ----- Row 5 -----

    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. Button calls 'clear_pin_entry' function.
    Button_tmp = tk.Button(win, text="Cancel/Clear", bg='red', activebackground='red')
    Button_tmp.bind('<Button-1>', clear_pin_entry)
    Button_tmp.grid(row=5, column=0, sticky='nsew')

    # Button 0 here
    Button_tmp = tk.Button(win, text="0")
    Button_tmp.bind('<Button-1>', handle_pin_button)
    Button_tmp.grid(row=5, column=1, columnspan=2, sticky='nsew')

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    Button_tmp = tk.Button(win, text="Login In", bg='green', activebackground='green')
    Button_tmp.bind('<Button-1>', log_in)
    Button_tmp.grid(row=5, column=3, columnspan=2, sticky='nsew')

    # ----- Set column & row weights -----

    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    for i in range(5):
        win.columnconfigure(i, weight=1)
    for i in range(6):
        win.rowconfigure(i, weight=1)

def create_account_screen():
    '''Function to create the account screen.'''
    global amount_text
    global amount_label
    global transaction_text_widget
    global balance_var
    
    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    tk.Label(win, text="FedUni BanKing", font='Helvetica 24 bold').grid(row=0, column=0, columnspan=5, sticky='nsew')

    # ----- Row 1 -----

    # Account number label here
    tk.Label(win, text="Account Number:"+str(account.account_number)).grid(row=1, column=0, sticky='nsew')
    # Balance label here
    balance_label.grid(row=1, column=2, sticky='nsew')
    balance_var.set("Balance: $"+str(account.balance))
    # Log out button here
    Button_tmp = tk.Button(win, text="Log Out", command=save_and_log_out)
    Button_tmp.grid(row=1, column=3, columnspan=2, sticky='nsew')

    # ----- Row 2 -----

    # Amount label here
    tk.Label(win, text="Account($):").grid(row=2, column=0, sticky='nsew')
    # Amount entry here
    amount_entry.grid(row=2, column=2, sticky='nsew')
    # Deposit button here
    Button_tmp = tk.Button(win, text="Deposit", command=perform_deposit)
    Button_tmp.grid(row=2, column=3, sticky='nsew')
    # Withdraw button here
    Button_tmp = tk.Button(win, text="Withdraw", command=perform_withdrawal)
    Button_tmp.grid(row=2, column=4, sticky='nsew')

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    # ----- Row 3 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    for child in transaction_text_widget.winfo_children():
        child.destroy()
    scroll = tk.Scrollbar(transaction_text_widget)
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited
    transaction_text_widget.config(yscrollcommand=scroll.set, state='normal')
    transaction_text_widget.delete(0.0, 'end')
    transaction_text_widget.insert('end', account.get_transaction_string())
    transaction_text_widget.config(state='disabled')
    transaction_text_widget.grid(row=3, columnspan=5, sticky='nsew')
    # Now add the scrollbar and set it to change with the yview of the text widget
    scroll.config(command=transaction_text_widget.yview)
    scroll.pack(side='right', fill='y')

    # ----- Row 4 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_interest_graph()

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    for i in range(5):
        win.columnconfigure(i, weight=1)
    for i in range(5):
        win.rowconfigure(i, weight=1)

# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
win.mainloop()
