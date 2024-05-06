import unittest
from wallet import Wallet
import os

class TestWallet(unittest.TestCase):

    def setUp(self):
        self.wallet = Wallet("TestUser")
        self.wallet_file = self.wallet.wallet_name
        
    def tearDown(self):
        del self.wallet
        if os.path.exists(self.wallet_file):
            os.remove(self.wallet_file)

    def test_initial_balance(self):
        self.assertEqual(self.wallet.balance, 0)

    def test_income(self):
        self.wallet.income(100)
        self.assertEqual(self.wallet.balance, 100)

    def test_spend(self):
        self.wallet.income(100)
        self.wallet.spend(50)
        self.assertEqual(self.wallet.balance, 50)

    def test_invalid_income(self):
        result = self.wallet.income(-50)
        self.assertEqual(result, "Ошибка платежа")

    def test_insufficient_funds(self):
        result = self.wallet.spend(50)
        self.assertEqual(result, "Недостаточно средств")

    def test_parse_wallet(self):
        test_wallet = Wallet("TestUser")
        test_wallet.income(100)
        test_wallet.spend(50)
        test_wallet2 = Wallet("TestUser")
        self.assertEqual(test_wallet2.balance, 50)

    def test_get_transactions(self):
        self.wallet.income(100, "Test Income")
        self.wallet.spend(50, "Test Spend")
        transactions = self.wallet.get_transactions("all")
        self.assertEqual(len(transactions), 2)

    def test_filter_transactions(self):
        self.wallet.income(100, "Test Income")
        self.wallet.spend(50, "Test Spend")
        transactions = self.wallet.get_transactions(
            transaction_type="all",
            date_start="2024-01-01",
            date_end="2024-12-31",
            amount_start=0,
            amount_end=100
        )
        self.assertEqual(len(transactions), 2)

if __name__ == '__main__':
    unittest.main()
