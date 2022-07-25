from multiprocessing.sharedctypes import Value
import os
import datetime
import re

import pandas as pd

from dictionaries import category_fund


class DataKeeper:

    TRANSACTION_DATA_PATH = os.path.join('data', 'transaction.csv')
    BALANCE_DATA_PATH = os.path.join('data', 'balance.csv')


    def __init__(self):
        self.month_date = DataKeeper.__compute_current_month()

        self.df_transaction = pd.read_csv(self.TRANSACTION_DATA_PATH, 
                                          parse_dates=['datetime', 'month_date'])

        self.df_balance = pd.read_csv(self.BALANCE_DATA_PATH, 
                                      parse_dates=['month_date'], 
                                      index_col=['month_date', 'fund'])


    def __compute_current_month():
        today_date = datetime.date.today()
        year, month, day = today_date.year, today_date.month, today_date.day
        return datetime.datetime(year, month, 7) if day >= 7 else datetime.datetime(year, month-1, 7)

    
    def parse_money_input(money_input):
        money_input = money_input.lower()
        pattern = re.compile(r"(-?[0-9]+) (.+)")
        
        result = pattern.match(money_input)
        if result is None: raise ValueError('Некоректний ввід. Вкажіть к-сть грошей та валюту, зразок: 1234 грн')
        money_value, currency = result.groups()
        money_value = int(money_value)
        
        if 'e' in currency: currency = 'EUR'
        if 'г' in currency or 'ua' in currency: currency = 'UAH'
        if 'd' in currency or '$' in currency: currency = 'USD'
        
        return money_value, currency


    def get_transaction_data(self):
        return self.df_transaction


    def get_balance_data(self):
        return self.df_balance


    def get_current_month(self):
        return self.month_date


    def add_transaction(self, money_input, is_income, category, fund):
        money_value, currency = DataKeeper.parse_money_input(money_input)
        if not is_income: money_value = -money_value
        if fund == '': fund = category_fund[category]

        month_date = self.month_date

        # append to data/transaction.csv
        self.df_transaction.loc[len(self.df_transaction.index)] = [money_value, 
                                                                   currency,
                                                                   datetime.datetime.now(),
                                                                   category,
                                                                   fund,
                                                                   month_date]
        self.df_transaction.to_csv(self.TRANSACTION_DATA_PATH, index=False)
        
        # renew balance of funds
        self.df_balance.loc[(month_date, fund), f'value_{currency.lower()}'] += money_value
        self.df_balance.to_csv(self.BALANCE_DATA_PATH)

