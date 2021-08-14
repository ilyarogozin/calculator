'''Модуль для подсчёта денег, либо калорий.'''
import datetime as dt


class Calculator:
    '''Родительский класс для калькуляторов.'''

    def __init__(self, limit):
        '''Конструктор родительского класс Calculator.'''
        self.limit = limit
        self.records = []

    def add_record(self, Record):
        '''Метод используется для добавления записей в список.'''
        self.records.append(Record)

    def get_today_stats(self):
        '''Метод используется для подсчёта сегодняшней статистики.'''
        today = dt.datetime.now().date()
        today_stats = 0
        for record in self.records:
            if record.date == today:
                today_stats += record.amount
            else:
                continue
        return today_stats

    def get_week_stats(self):
        '''Метод используется для подсчёта статистики за последние 7 дней.'''
        week = dt.timedelta(days=7)
        today = dt.datetime.now().date()
        one_week_ago = today - week
        week_stats = 0
        for record in self.records:
            if record.date <= today and record.date >= one_week_ago:
                week_stats += record.amount
            else:
                continue
        return week_stats


class CaloriesCalculator(Calculator):
    '''Дочерний класс CaloriesCalculator используется для подсчёта калорий.'''

    def get_calories_remained(self):
        '''Метод используется для подсчёта калорий,
        которые можно получить сегодня.
        '''
        if self.get_today_stats() < self.limit:
            calories_left = self.limit - self.get_today_stats()
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_left} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    '''Дочерний класс CashCalculator используется для подсчёта денег.'''

    USD_RATE = 73.20
    EURO_RATE = 86.37

    def get_today_cash_remained(self, currency):
        '''Метод используется для подсчёта денег,
        которые можно потратить сегодня.
        '''
        if self.get_today_stats() < self.limit:
            money_left = self.limit - self.get_today_stats()
            if currency == 'usd':
                currency = 'USD'
                money = format(money_left / self.USD_RATE, '.2f')
            elif currency == 'eur':
                currency = 'Euro'
                money = format(money_left / self.EURO_RATE, '.2f')
            elif currency == 'rub':
                currency = 'руб'
                money = money_left
            return f'На сегодня осталось {money} {currency}'
        elif self.get_today_stats() == self.limit:
            return 'Денег нет, держись'
        else:
            money_over = self.get_today_stats() - self.limit
            if currency == 'usd':
                currency = 'USD'
                money = format(money_over / self.USD_RATE, '.2f')
            elif currency == 'eur':
                currency = 'Euro'
                money = format(money_over / self.EURO_RATE, '.2f')
            elif currency == 'rub':
                currency = 'руб'
                money = money_over
            return f'Денег нет, держись: твой долг - {money} {currency}'


class Record:
    '''Родительский класс для хранения событий.'''

    def __init__(self, amount, comment,
                 date=None):
        '''Конструктор родительского класса Record.'''
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
