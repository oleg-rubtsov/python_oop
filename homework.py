import datetime as dt


class Record:
    def __init__(self, amount, comment="Не регламентировано", date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        result = 0
        for record in self.records:
            if record.date == dt.datetime.now().date():
                result += record.amount
        return result

    def get_week_stats(self):
        result = 0
        for record in self.records:
            k = (dt.datetime.now().date() - record.date).days
            if k <= 7 and k >= 0:
                result += record.amount
        return result


class CashCalculator (Calculator):
    USD_RATE = 60.00
    EURO_RATE = 70.00

    def get_today_cash_remained(self, currency):
        today = self.get_today_stats()
        USD_RATE = 60.00
        EURO_RATE = 70.00
        if currency == 'rub':
            if today < self.limit:
                return f'На сегодня осталось {self.limit - today} руб'
            elif today == self.limit:
                return (f'Денег нет, держись')
            else:
                return (f'Денег нет, держись: твой долг - '
                        f'{-(self.limit - today)} руб')
        elif currency == 'usd':
            if today < self.limit:
                return (f'На сегодня осталось '
                        f'{round((self.limit - today)/USD_RATE, 2)} USD')
            elif today == self.limit:
                return (f'Денег нет, держись')
            else:
                return (f'Денег нет, держись: твой долг - '
                        f'{round((-(self.limit - today))/USD_RATE, 2)} USD')
        elif currency == 'eur':
            if today < self.limit:
                return (f'На сегодня осталось '
                        f'{round((self.limit - today)/EURO_RATE, 2)} Euro')
            elif today == self.limit:
                return (f'Денег нет, держись')
            else:
                return (f'Денег нет, держись: твой долг - '
                        f'{round((-(self.limit - today))/EURO_RATE, 2)} Euro')


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today = self.get_today_stats()
        if today < self.limit:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.limit - today} кКал')
        else:
            return (f'Хватит есть!')
