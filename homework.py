import datetime as dt


class Calculator:
    WEEK = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, Record):
        self.records.append(Record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount for record in self.records if
                   record.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        one_week_ago = today - self.WEEK
        return sum(record.amount for record in self.records if
                   record.date <= today and record.date > one_week_ago)


class CaloriesCalculator(Calculator):
    PHRASE_ABOUT_REMAIN = ('Сегодня можно съесть что-нибудь ещё, но с общей'
                           ' калорийностью не более {calories_left} кКал')
    PHRASE_ABOUT_EXCESS = 'Хватит есть!'

    def get_calories_remained(self):
        today_stats = self.get_today_stats()

        if today_stats < self.limit:
            left = self.limit - today_stats
            return self.PHRASE_ABOUT_REMAIN.format(calories_left=left)
        elif today_stats >= self.limit:
            return self.PHRASE_ABOUT_EXCESS


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    PHRASE_ABOUT_REMAIN = 'На сегодня осталось {money} {currency}'
    PHRASE_NO_MONEY = 'Денег нет, держись'
    PHRASE_ABOUT_DEBT = ('Денег нет, держись: твой долг'
                         ' - {money} {currency}')
    CURRENCY_DICT = {'usd': ['USD', 1 / USD_RATE],
                     'eur': ['Euro', 1 / EURO_RATE],
                     'rub': ['руб', 1]
                     }

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()
        currency_text = self.CURRENCY_DICT[currency][0]
        ratio_rub_to_currency = self.CURRENCY_DICT[currency][1]

        if today_stats < self.limit:
            money_left = round((self.limit - today_stats)
                               * ratio_rub_to_currency, 2)
            return self.PHRASE_ABOUT_REMAIN.format(money=money_left,
                                                   currency=currency_text)
        elif today_stats == self.limit:
            return self.PHRASE_NO_MONEY
        elif today_stats > self.limit:
            money_over = round((today_stats - self.limit)
                               * ratio_rub_to_currency, 2)
            return self.PHRASE_ABOUT_DEBT.format(money=money_over,
                                                 currency=currency_text)


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
