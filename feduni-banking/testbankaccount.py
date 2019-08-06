import unittest

from bankaccount import BankAccount

class TestBankAcount(unittest.TestCase):

    def setUp(self):
        # Create a test BankAccount object
        self.account = BankAccount()

        # test for save file
        self.account.account_number = 1100
        self.account.pin_number = 1100

        # Provide it with some property values        
        self.account.balance = 1000.0

    def test_legal_deposit_works(self):
        # Your code here to test that depsositing money using the account's
        # 'deposit_funds' function adds the amount to the balance.
        self.account.deposit_funds(2000)
        self.account.deposit_funds("3123")

    def test_illegal_deposit_raises_exception(self):
        # Your code here to test that depositing an illegal value (like 'bananas'
        # or such - something which is NOT a float) results in an exception being
        # raised.
        self.account.deposit_funds("fsdfsd")

    def test_legal_withdrawal(self):
        # Your code here to test that withdrawing a legal amount subtracts the
        # funds from the balance.
        self.account.withdraw_funds(200)
        self.account.withdraw_funds("300")

    def test_illegal_withdrawal(self):
        # Your code here to test that withdrawing an illegal amount (like 'bananas'
        # or such - something which is NOT a float) raises a suitable exception.
        self.account.withdraw_funds("sdfsad")

    def test_insufficient_funds_withdrawal(self):
        # Your code here to test that you can only withdraw funds which are available.
        # For example, if you have a balance of 500.00 dollars then that is the maximum
        # that can be withdrawn. If you tried to withdraw 600.00 then a suitable exception
        # should be raised and the withdrawal should NOT be applied to the account balance
        # or the account's transaction list.
        self.account.withdraw_funds("50000000000")

    def test_save_to_file(self):
        # Test the function of saving file
        self.account.save_to_file()


# Run the unit tests in the above test case
unittest.main(verbosity=2)