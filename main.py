import requests
import datetime
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

account_sid = "INSERT ACC SID"
auth_token = "INSERT AUTH TOKEN"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "interval": "5min",
    "datatype": "json",
    "apikey": "INSERT STOCK API KEY"
}

response = requests.get("https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()

today = datetime.datetime.today()

last_refreshed = response.json()["Meta Data"]["3. Last Refreshed"]

data_last_two = [(key, value) for (key, value) in response.json()['Time Series (Daily)'].items()][0:2]

yesterday_close_price = float(data_last_two[0][1]["4. close"])
before_yesterday_close_price = float(data_last_two[1][1]["4. close"])

diff_percentage = abs(round((yesterday_close_price - before_yesterday_close_price) / before_yesterday_close_price * 100, 2))

diff_direction = ""

if yesterday_close_price > before_yesterday_close_price:
    diff_direction = "📈"
else:
    diff_direction = "📉️"

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

if diff_percentage > 5:
    news_params = {
        "q": f"{COMPANY_NAME}",
        "from": f"2022-11-21",
        "sortBy": "popularity",
        "apiKey": "INSERT NEWS API KEY"
    }

    news_response = requests.get("https://newsapi.org/v2/everything", params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][0:3]

    ## STEP 3: Use https://www.twilio.com
    # Send a separate message with the percentage change and each article's title and description to your phone number.
    client = Client(account_sid, auth_token)
    for item in news_data:
        message = client.messages.create(
            body=f"""TSLA: {diff_direction} {diff_percentage}%
            Headline: {item["title"]}
            Brief: {item["description"]}
                """,
            from_='+13466372476',
            to='INSERT PHONE NUMBER'
        )