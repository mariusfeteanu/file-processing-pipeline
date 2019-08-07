import pandas as pd
import numpy as np


countries = pd.read_csv('reference/countries.csv',
                   header=0,
                   dtype=str,
                   encoding='utf-8')[['alpha-2']]


currencies = pd.read_csv('reference/currencies.csv',
                   header=0,
                   dtype=str,
                   encoding='utf-8')[['AlphabeticCode']]


companies = pd.read_csv('reference/companies.csv',
                   header=0,
                   dtype=str,
                   encoding='utf-8')[['source_id']]

base_df = pd.DataFrame.from_dict({'open': [1.0],
                                  'high': [2.0],
                                  'low': [3.0],
                                  'close': [4.0],
                                  'volume': [5.0],
                                  'P/E': [6.0],
                                  'EPS': [7.0]})

countries['key'] = 1
currencies['key'] = 1
companies['key'] = 1
base_df['key'] = 1

big_df = pd.merge(pd.merge(pd.merge(base_df, currencies), countries), companies).drop(['key'], axis=1)
big_df = big_df.rename(columns={'alpha-2': 'country_code', 'AlphabeticCode': 'currency_code', 'source_id': 'company_source_id'})

nrows = big_df.shape[0]
big_df['open'] = np.random.randint(10, 90, nrows)/10.0
big_df['high'] = np.random.randint(20, 150, nrows)/10.0
big_df['low'] = np.random.randint(1, 70, nrows)/10.0
big_df['close'] = np.random.randint(20, 100, nrows)/10.0
big_df['volume'] = np.random.randint(100, 10000, nrows)
big_df['P/E'] = np.random.randint(30, 300, nrows)/10.0
big_df['EPS'] = np.random.randint(100, 10000, nrows)/10.0


print(big_df.head(100))

big_df.to_csv('input_root/big/end_of_day.csv',
              index=False,
              header=True,
              encoding='utf8')
