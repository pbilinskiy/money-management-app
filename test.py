import unittest

from DataKeeper import DataKeeper


class TestGlobal(unittest.TestCase):
    
    d = DataKeeper()

    def test_parse_money_input(self):
        money_value, currency = None, None
        for s in ['1200 e', '134 грн', '-250 $']:
            money_value, currency = DataKeeper.parse_money_input(s)
            self.assertTrue(isinstance(money_value, int))
            self.assertTrue(currency in ['EUR', 'UAH', 'USD'])
    
    def test_data_aggregation(self):
        df = self.d.get_transaction_data()
        df = df[df['money_value'] < 0]
        df.loc[:, 'money_value'] *= -1

        df_agg = df.groupby('category')['money_value'].sum().reset_index()
        # print(df_agg)

    def test_add_transaction(self):
        self.d.add_transaction('400 грн', False, 'road', None)

if __name__ == '__main__':
    unittest.main()