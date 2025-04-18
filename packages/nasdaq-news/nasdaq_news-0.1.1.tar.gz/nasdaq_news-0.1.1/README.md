# nasdaq_news

Get JSON news data for NASDAQ-100 stocks using a simple Python method.

## Install

```bash
pip install nasdaq-news

import nasdaq_news
from nasdaq_news import get_news

# Fetch local news data for Apple
data = get_news("AAPL")

# View first few articles
print(data)

```


## Structure
Below is the project structure:

<pre>
nasdaq_news/
├── nasdaq_news/
│   ├── __init__.py
│   ├── fetcher.py
│   └── data/
│       ├── AAPL.json
│       ├── MSFT.json
│       └── ... (up to 100 files)
├── setup.py
├── README.md
├── LICENSE
└── .gitignore
</pre>

