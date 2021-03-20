import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
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
        date_today = dt.datetime.today().date()
        for record in self.records:
            if record.date == date_today:
                result += record.amount
        return result

    def get_week_stats(self):
        result = 0
        date_today = dt.datetime.today().date()
        week_ago = date_today - dt.timedelta(days=7)
        for record in self.records:
            if record.date >= week_ago and record.date <= date_today:
                result += record.amount
        return result


class CashCalculator (Calculator):
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        if currency == "rub" or currency == "usd" or currency == "eur":
            pass
        else:
            raise ZeroDivisionError()
        today = self.get_today_stats()
        slovar = {
            'rub': 'руб',
            'usd': 'USD',
            'eur': 'Euro'
        }
        rates = {
            'rub': self.RUB_RATE,
            'usd': self.USD_RATE,
            'eur': self.EURO_RATE
        }
        ostatok = round((self.limit - today) / rates[currency], 2)
        if today < self.limit:
            return (f'На сегодня осталось '
                    f'{ostatok} {slovar[currency]}')
        elif today == self.limit:
            return ('Денег нет, держись')
        else:
            return (f'Денег нет, держись: твой долг - '
                    f'{-ostatok} {slovar[currency]}')


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today = self.get_today_stats()
        ostatok = self.limit - today
        if today < self.limit:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {ostatok} кКал')
        else:
            return ('Хватит есть!')
