from __future__ import annotations

import datetime as dt
from typing import Optional, Union


class Record:
    """Класс Record, необходим для создания новой записи"""
    def __init__(self,
                 amount: Union[int, float],
                 comment: str,
                 date: Optional[str] = None) -> None:
        """Конструктор класса Record, на вход получает 3 аргумента
        (количество потраченных денег или полученных калорий, объект траты,
        дата)"""
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class Calculator:
    """Класс Calculator, родительский класс,
    осуществляет основную калькуляцию,
    содержит методы: -add_record (добавление новой записи в список)
                     -get_today_stats (перебирает список и считает
                     сумму за текущий день)
                     -get_today_remainder (считает остаток на сегодня)
                     -get_week_stats (сумма за неделю)"""
    def __init__(self, limit: Union[int, float]) -> None:
        """Конструктор класса Calculator,
        в качестве аргумента принимает дневной лимит."""
        self.limit = limit
        self.records: list[Record] = []

    def add_record(self, record: Record) -> None:
        """Метод add_record сохраняет новую запись о расходах в списке"""
        self.records.append(record)

    def get_today_stats(self) -> Union[int, float]:
        """Метод get_today_stats перебирает список и считает, сколько
        калорий уже съедено сегодня или сколько денег потрачено сегодня"""
        result: Union[int, float] = 0
        date_today: dt.date = dt.date.today()
        for record in self.records:
            if record.date == date_today:
                result += record.amount
        return result

    def get_today_remainder(self) -> Union[int, float]:
        """Метод get_today_remainder считает остаток на сегодня"""
        today: Union[int, float] = self.get_today_stats()
        return self.limit - today

    def get_week_stats(self) -> Union[int, float]:
        """Метод get_week_stats считает, сколько калорий
        получено за последние 7 дней или сколько денег потрачено
        за последние 7 дней"""
        result: Union[int, float] = 0
        date_today: dt.date = dt.datetime.today().date()
        week_ago: dt.date = date_today - dt.timedelta(days=7)
        for record in self.records:
            if record.date >= week_ago and record.date <= date_today:
                result += record.amount
        return result


class CashCalculator (Calculator):
    """Класс CashCalculator, необходим для подсчёта денег"""
    USD_RATE: float = 60.00
    EURO_RATE: float = 70.00
    RUB_RATE: float = 1

    def get_today_cash_remained(self, currency: str) -> str:
        """Метод get_today_cash_remained определяет, сколько ещё денег
        можно потратить сегодня в рублях, долларах или евро """
        rates: dict[str, tuple[float, str]] = {
            'rub': (self.RUB_RATE, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }
        if currency not in rates:
            raise ValueError()
        remainder: Union[int, float] = self.get_today_remainder()
        balance: Union[int, float] = round((remainder / rates[currency][0]), 2)
        if balance == 0:
            return ('Денег нет, держись')
        elif balance > 0:
            return (f'На сегодня осталось '
                    f'{balance} {rates[currency][1]}')
        else:
            return (f'Денег нет, держись: твой долг - '
                    f'{-balance} {rates[currency][1]}')


class CaloriesCalculator(Calculator):
    """Класс CaloriesCalculator необходим для подсчёта калорий"""
    def get_calories_remained(self):
        """Метод get_calories_remained определяет, сколько ещё
        калорий можно/нужно получить сегодня"""
        remainder: Union[int, float] = self.get_today_remainder()
        if remainder > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {remainder} кКал')
        else:
            return ('Хватит есть!')
