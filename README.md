# Wallet app

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Wallet app - простое консольное приложение, предоставляющее функционал личного финансового кошелька

### Инструменты

- Python

### Функционал

1) Просмотр баланса, доходов, расходов 
2) Добавление новых записей о доходах или расходах 
3) Фильтрация записей по категории, дате, сумме операции 
4) Редактирование существующих записей

## Run locally
    python main.py

## Run tests
    python tests.py


#### Docs:
`method`

    create_transaction(category: str, amount: float, description: str | None = "") -> dict[str, str | float]

    получает на вход параметры:
        category: str 
        amount: float 
        description: str | None = ""

    возвращает транзакцию в виде словаря для дальнейшего использования

`method`

    get_string_transaction(transaction: dict[str, str | float]) -> str

    получает на вход параметры:
        transaction: dict[str, str | float]

    возвращает транзакцию в виде строки для вывода в консоль, или записи в файл

`method`

    add_transaction(self, transaction: dict[str, str | float]) -> None

    получает на вход параметры:
        transaction: dict[str, str | float]

    добавляет новую транзакцию в общий словарь и записывает ее в файл

`method`

    income(self, amount: float, description: str | None = "") -> str

    получает на вход параметры:
        amount: float
        description: str | None = ""

    зачисляет на баланс указанную сумму 

`method`

    spend(self, amount: float, description: str | None = "") -> str

    получает на вход параметры:
        amount: float
        description: str | None = ""

    списывает с баланаса указанную сумму 

`method`

    get_transactions(
        self,
        transaction_type: str | None = None,
        date_start: str | None = None,
        date_end: str | None = None,
        amount_start: float | None = None,
        amount_end: float | None = None,
    ) -> dict[str, str | float] | None:

    возвращает все транзакции, сделанные пользователем с указанными параметрами 

`method`

    parse_wallet(self) -> None

    считывает все записи с файла при запуске приложения
