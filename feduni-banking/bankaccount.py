class BankAccount():

    def __init__(self):
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''
        self.account_number = 0      #int
        self.pin_number = ''         #string
        self.balance = 0.0           #float
        self.interest_rate = 0.0     #float
        self.transaction_list = []   #list of two-tuples

    def deposit_funds(self, amount):
        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        try:
            value = float(amount)
            self.balance += value
            self.transaction_list.append(("Deposit",value))
        except Exception:
            raise Exception("The amount cannot be cast to float")

    def withdraw_funds(self, amount):
        '''Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        try:
            value = float(amount)
            assert value < self.balance
            self.balance -= value
            self.transaction_list.append(("Withdrawal",value))
        except AssertionError :
            raise Exception("The amount to withdraw is greater than the available funds in the account")
        except Exception:
            raise Exception("The amount cannot be cast to float")
        
        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line.'''
        ss = ""
        for trans in self.transaction_list:
            ss = ss + str(trans[0]) + "\n" + str(trans[1]) + "\n"
        ss = ss[:-1]
        return ss

    def save_to_file(self):
        '''Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        file_name = str(self.account_number) + ".txt"
        with open(file_name,"w") as f:
            f.write(str(self.account_number)+"\n")
            f.write(str(self.pin_number)+"\n")
            f.write(str(self.balance)+"\n")
            f.write(str(self.interest_rate))
            if len(self.transaction_list) != 0:
                f.write("\n")
                f.write(self.get_transaction_string())