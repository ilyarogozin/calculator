import datetime as dt


class Calculator:
    PERIOD_FROM_TODAY_TO_WEEK_AGO = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, Record):
        self.records.append(Record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount
                   for record in self.records
                   if record.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        one_week_ago = today - self.PERIOD_FROM_TODAY_TO_WEEK_AGO
        return sum(record.amount
                   for record in self.records
                   if record.date <= today and one_week_ago < record.date)


class CaloriesCalculator(Calculator):
    REMAIN = ('Сегодня можно съесть что-нибудь ещё, но с общей'
              ' калорийностью не более {calories_left} кКал')
    EXCESS = 'Хватит есть!'

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        if today_stats < self.limit:
            left = self.limit - today_stats
            return self.REMAIN.format(calories_left=left)
        else:
            return self.EXCESS


class CashCalculator(Calculator):
    USD_RATE = 1 / 60.0
    EURO_RATE = 1 / 70.0
    REMAIN = 'На сегодня осталось {money} {currency}'
    NO_MONEY = 'Денег нет, держись'
    DEBT = ('Денег нет, держись: твой долг'
            ' - {money} {currency}')
    UNEXPECTED_CURRENCY = 'Неправильно введённая валюта.'
    CURRENCY = {'usd': ['USD', USD_RATE],
                'eur': ['Euro', EURO_RATE],
                'rub': ['руб', 1]
                }

    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCY:
            raise ValueError(self.UNEXPECTED_CURRENCY)
        today_stats = self.get_today_stats()
        currency_name, rate_rub_to_currency = self.CURRENCY[currency]
        money_difference = 0
        if today_stats < self.limit:
            money_difference = self.limit - today_stats
            phrase = self.REMAIN
        elif today_stats == self.limit:
            phrase = self.NO_MONEY
        else:
            money_difference = today_stats - self.limit
            phrase = self.DEBT
        format_money = round(money_difference * rate_rub_to_currency, 2)
        return phrase.format(money=format_money, currency=currency_name)


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
