from wallet import Wallet

def main() -> None:
    operations = {
        "1": {
            "name": "Посмотреть баланс", 
            "func": "get_balance"
        },
        "2": {
            "name": "Показать доходы",
            "func": "get_transactions",
            "value": "income",
        },
        "3": {
            "name": "Показать расходы",
            "func": "get_transactions",
            "value": "spend",
        },
        "4": {
            "name": "Добавить запись о доходе",
            "func": "income",
        },
        "5": {
            "name": "Добавить запись о расходе",
            "func": "spend",
        },
        "6": {
            "name": "Поиск записи",
            "func": "get_transactions",
        },
        "7": {
            "name": "Изменить запись",
            "func": "get_transactions",
        },
        "8": {"name": "Выйти"},
    }

    owner = input("Пожалуйста, введите имя кошелька\n").strip()
    wallet = Wallet(owner)

    while True:

        for i, data in operations.items():
            print(f"{i}. {data['name']}")

        query = input("Пожалуйста, введите номер действия\n").strip()

        try:
            op = operations[query]
        except KeyError:
            print("Такой команды нету, попробуйте еще раз")
        else:
            if query in ("1", "2", "3"):
                value = op.get("value", None)
                res = (
                    getattr(wallet, op["func"])()
                    if not value
                    else getattr(wallet, op["func"])(value)
                )

            elif query in ("4", "5"):
                try:
                    amount = float(input("Пожалуйста, введите сумму\n").strip())
                except ValueError:
                    print("Недопустимое значение")
                else:
                    description = input("Пожалуйста, введите описание\n").strip()
                    result = getattr(wallet, op["func"])(amount, description)
                    print(result)

            elif query == "6":

                answer = input(
                    "1. Доходы\n"
                    "2. Расходы\n"
                    "Выберите по какой категории вы хотите отфильтровать\n"
                ).strip()
                data = {"1": "income", "2": "spend"}
                category = data.get(answer, 0)

                date_start = input(
                    "Введите начальную дату в формате YYYY-MM-DD\n"
                ).strip()
                date_end = input("Введите конечную дату в формате YYYY-MM-DD\n").strip()
                amount_start = input("Введите начальную сумму\n").strip()
                amount_end = input("Введите конечную сумму\n").strip()
                wallet.get_transactions(
                    category, date_start, date_end, amount_start, amount_end
                )

            elif query == "7":
                transactions = wallet.get_transactions()
                transaction_id = int(
                    input(
                        "Пожалуйста, выберите номер транзакции для редактирования\n"
                    ).strip()
                )

                cur_transaction = wallet.get_string_transaction(
                    transactions[transaction_id - 1]
                )
                print(cur_transaction)

                new_description = input("Введите новое описание\n").strip()
                line_index = transaction_id * 5 - 2

                with open(wallet.wallet_name, "r+", encoding="utf-8") as file:
                    lines = file.readlines()
                    lines[line_index] = f"Описание: {new_description}\n"
                    file.seek(0)
                    file.writelines(lines)
                    file.truncate()

            elif query == "8":
                break


if __name__ == "__main__":
    main()
