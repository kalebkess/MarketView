####
####    Script to interact with database.
####    $ python3 -i explore_db.py
####
####
import os
import sqlalchemy

# python3 -i explore_db.py

SRC_PATH = os.environ.get('SRC_PATH')  #  path to source code os.path.abspath('.')
DB_NAME = os.environ.get('DB_NAME')  #  [database will be one directory above source code]
IEX_KEY = os.environ.get('IEX_KEY')  # IEX api key to get market data


engine = sqlalchemy.create_engine(f"sqlite:///{SRC_PATH.replace('/MarketView', '')}/{DB_NAME}")