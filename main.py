import requests
from twilio.rest import Client


account_sid = "ACcd587c473e96c7d2e9fe4c0e11648ae7"
auth_token = "8e9ebf5ace7e76392ba7638e74a32a6c"


API_KEY_STOCK = "CSA9LHPL3F9ME7GL"

MY_STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": API_KEY_STOCK}

stock_request = requests.get(url="https://www.alphavantage.co/query", params=MY_STOCK_PARAMETERS)
stock_request.raise_for_status()
stock_data = stock_request.json()["Time Series (Daily)"]
stock_data_list = [value for (key,value) in stock_data.items()]
yesterday_data = stock_data_list[0]
yesterday_data_close = yesterday_data["4. close"]
day_before_yesterday_data = stock_data_list[1]
day_before_yesterday_data_close = day_before_yesterday_data["4. close"]

defference_stock = float(yesterday_data_close) - float(day_before_yesterday_data_close)
up_down_stock = None
if defference_stock > 1:
    up_down_stock = "🔺"
else:
    up_down_stock = "🔻"

percentage_diff = (defference_stock/float(yesterday_data_close))*100

API_KEY_NEWS = "c471dff0d57b4d7c8022d9ed12573781"
API_NEWS = "https://newsapi.org/v2/everything"

MY_NEWS_PARAMETERS = {
    "q": "Tesla",
    "apikey": API_KEY_NEWS,
}
news_request = requests.get(url=API_NEWS, params=MY_NEWS_PARAMETERS)
news_request.raise_for_status()
new_data = news_request.json()

news = new_data["articles"][0:3]


if abs(percentage_diff) > 0.7:
    for data in range(0, 1):
        title = news[data]["title"]
        decrip = news[data]["description"]
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"TESLA Stock : {round(abs(percentage_diff))}% {up_down_stock} \n\n News: \n\n Headline: {title} \n\n Description: {decrip} ",
            from_='+16614413360',
            to='+917001459154'
        )
        print(message.status)
