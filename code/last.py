import datetime
import json
import os
import pandas as pd
import requests
import sqlalchemy

SRC_PATH = os.environ.get('SRC_PATH')  #  path to source code os.path.abspath('.')
DB_NAME = os.environ.get('DB_NAME')  #  [database will be one directory above source code]
IEX_KEY = os.environ.get('IEX_KEY')  # IEX api key to get market data


def get_last_price(engine):
    table_name = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S last')
    params = {'token':IEX_KEY}
    r = requests.get(f"https://cloud.iexapis.com/stable/tops/last", params=params)
    if r.status_code == 200:
        data = pd.DataFrame(r.json()).set_index('symbol')
        data.to_sql(table_name, engine)
    return data


if __name__ == '__main__':
    # Create engine
    engine = sqlalchemy.create_engine(f"sqlite:///{SRC_PATH.replace('/MarketView', '')}/{DB_NAME}")
    get_last_price(engine)


