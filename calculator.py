import datetime as dt


class Calculator:

    WEEK_AGO = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount
                   for record in self.records
                   if record.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - self.WEEK_AGO
        return sum(record.amount
                   for record in self.records
                   if week_ago < record.date <= today)


class CaloriesCalculator(Calculator):

    REMAIN = ('Сегодня можно съесть что-нибудь ещё, но с общей'
              ' калорийностью не более {calories_left} кКал')
    EXCESS = 'Хватит есть!'

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        if today_stats < self.limit:
            left = self.limit - today_stats
            return self.REMAIN.format(calories_left=left)
        return self.EXCESS


class CashCalculator(Calculator):

    USD_RATE = 60.0
    EURO_RATE = 70.0
    REMAIN = 'На сегодня осталось {money} {currency}'
    NO_MONEY = 'Денег нет, держись'
    DEBT = ('Денег нет, держись: твой долг'
            ' - {money} {currency}')
    UNEXPECTED_CURRENCY = 'Неожиданная валюта: {unexpected_currency}'
    CURRENCIES = {'usd': ['USD', USD_RATE],
                  'eur': ['Euro', EURO_RATE],
                  'rub': ['руб', 1]
                  }

    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCIES:
            raise ValueError(
                self.UNEXPECTED_CURRENCY.format(unexpected_currency=currency))
        money_difference = self.limit - self.get_today_stats()
        if money_difference == 0:
            return self.NO_MONEY
        name, rate = self.CURRENCIES[currency]
        format_money = round(money_difference / rate, 2)
        if money_difference > 0:
            return self.REMAIN.format(money=format_money, currency=name)
        return self.DEBT.format(money=abs(format_money), currency=name)


class Record:

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment,
                 date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


if __name__ == '__main__':
    def test():
        calories = CaloriesCalculator(1500)
        cash = CashCalculator(3000)
        rec1 = Record(200, 'Макароны с картошкой')
        rec2 = Record(40, 'На хлеб')
        calories.add_record(rec1)
        cash.add_record(rec2)
        print(calories.get_calories_remained())
        print(cash.get_today_cash_remained('rub'))

    test()
