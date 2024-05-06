from datetime import datetime as dt


class Wallet:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.wallet_name = f"wallet_{self.owner.lower()}.txt"
        self.balance = 0
        self.transactions = {"income": [], "spend": [], "all": []}

        self.parse_wallet()

    def get_balance(self) -> None:
        print(f"Ваш баланс составляет {self.balance}")

    @staticmethod
    def create_transaction(
        category: str, amount: float, description: str | None = ""
    ) -> dict[str, str | float]:

        transaction = {
            "time": dt.now().strftime("%Y-%m-%d"),
            "category": category,
            "amount": amount,
            "description": description,
        }

        return transaction

    @staticmethod
    def get_string_transaction(transaction: dict[str, str | float]) -> str:
        string_transaction = (
            f"Дата: {transaction['time']}\n"
            f"Категория: {transaction['category']}\n"
            f"Сумма: {transaction['amount']}\n"
            f"Описание: {transaction['description']}\n"
            "--------------------------\n"
        )

        return string_transaction

    def add_transaction(self, transaction: dict[str, str | float]) -> None:

        transaction_type = "income" if transaction["category"] == "Доход" else "spend"

        self.transactions[transaction_type].append(transaction)
        self.transactions["all"].append(transaction)

        string_transaction = self.get_string_transaction(transaction)

        with open(self.wallet_name, "a", encoding="utf-8") as file:
            file.write(string_transaction)

    def income(self, amount: float, description: str | None = "") -> str:
        if amount <= 0:
            return "Ошибка платежа"

        transaction = self.create_transaction("Доход", amount, description)

        self.add_transaction(transaction)

        self.balance += amount

        return f"На баланс успешно зачислено {amount}"

    def spend(self, amount: float, description: str | None = "") -> str:
        if amount <= 0:
            return "Ошибка платежа"

        if self.balance < amount:
            return "Недостаточно средств"

        transaction = self.create_transaction("Расход", amount, description)

        self.add_transaction(transaction)

        self.balance -= amount

        return f"Оплата на сумму {amount} прошла успешно"

    def get_transactions(
        self,
        transaction_type: str | None = None,
        date_start: str | None = None,
        date_end: str | None = None,
        amount_start: float | None = None,
        amount_end: float | None = None,
    ) -> dict[str, str | float] | None:

        try:
            date_start = dt.strptime(date_start, "%Y-%m-%d") if date_start else dt.min
            date_end = dt.strptime(date_end, "%Y-%m-%d") if date_end else dt.now()

            amount_start = float(amount_start) if amount_start else 0
            amount_end = float(amount_end) if amount_end else float("inf")
        except ValueError:
            print("Данные для фильтрации введены неверно")
            return

        if not transaction_type:
            transactions = self.transactions["all"]
        else:
            transactions = self.transactions.get(transaction_type, 0)

        filtered_transactions = []

        if transactions:
            for transaction in transactions:
                transaction_date = dt.strptime(transaction["time"], "%Y-%m-%d")
                if (
                    date_start <= transaction_date <= date_end
                    and amount_start <= transaction["amount"] <= amount_end
                ):
                    filtered_transactions.append(transaction)

        if not filtered_transactions:
            print("Операций не найдено")
            return

        for i, transaction in enumerate(filtered_transactions):
            print(f"Транзакция #{i + 1}")
            print(self.get_string_transaction(transaction))

        print(f"Всего записей: {len(filtered_transactions)}")

        return filtered_transactions

    def parse_wallet(self) -> None:
        keys = {
            "Дата": "time",
            "Категория": "category",
            "Сумма": "amount",
            "Описание": "description",
        }
        try:
            with open(self.wallet_name, "r", encoding="utf-8") as file:
                cur_transaction = {}
                for line in file:
                    if line[0] != "-":
                        key, value = line.rstrip("\n").split(": ")
                        value = float(value) if key == "Сумма" else value
                        cur_transaction[keys[key]] = value
                    else:
                        category = (
                            "income"
                            if cur_transaction["category"] == "Доход"
                            else "spend"
                        )
                        self.transactions[category].append(cur_transaction)
                        self.transactions["all"].append(cur_transaction)

                        amount = cur_transaction["amount"]
                        self.balance += amount if category == "income" else amount * -1

                        cur_transaction = {}

        except FileNotFoundError:
            pass
