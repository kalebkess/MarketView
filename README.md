# MarketView
Market data visualization tool with jupyter prototyping environment.

## Setup environment 



Create virtual environment
<br>

<code>python3 -m venv lab_venv</code>
<br>

Activate virtual environment

<code>source lab_venv/bin/activate</code>
<br>

install requirements

<code>$pip install -r requirements.txt</code>
<br>

launch jupyter

<code>$jupyter lab --ip 0.0.0.0</code>
<br>

Local host for jupyter http://127.0.0.1/8501
<br>

Streamlit default port is 8501
Default jupyter port is 8888


## Running cron jobs

Use last.py to get overnight price (previous close for next day) “at 00:00 on every day-of-week from Monday through Friday.”

<code>0 0 * * 1-5</code>

Use quote.py to get quotes every minute: <br>

“At every minute past every hour from 14 through 20 on every day-of-week from Monday through Friday.”

<code>* 14-20 * * 1-5</code>

“At every minute from 31 through 59 past every hour from 13 through 14 on every day-of-week from Monday through Friday.” <br>
<code>31-59 13 * * 1-5</code>