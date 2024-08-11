import requests
import smtplib
from datetime import datetime, timedelta
import html

my_email = "<your email id>"
password = "<google app password>"

stock_api_key = "<api_key>"
news_api_key = "<api_key2>"

yest = datetime.now().date() - timedelta(1)
day_before_yest = datetime.now().date() - timedelta(2)

stock_params = {"function":"TIME_SERIES_DAILY",
                "symbol":"TSLA",
                "apikey":stock_api_key}

news_params = {"qInTitle":"Tesla",
               "sortBy":"datepublished",
               "apiKey":news_api_key,
               "from":f"{yest}",
               "language":"en"}

news = requests.get(url="https://newsapi.org/v2/everything?", params=news_params)
news.raise_for_status()
news_data = news.json()

articles = {}

for i in range(3):
    articles[f"Article {i + 1}"] = {}
    articles[f"Article {i + 1}"]["Title"] = news_data["articles"][i]["title"].replace("\xa0", " ").replace("\u2018", "").replace("\u2019", "").replace("\u2026", "")
    articles[f"Article {i + 1}"]["Description"] = news_data["articles"][i]["description"].replace("\xa0", " ").replace("\u2018", "").replace("\u2019", "").replace("\u2026", "")


stock = requests.get(url="https://www.alphavantage.co/query?", params=stock_params)
stock.raise_for_status()
stock_data = stock.json()

yest_stock_price = float(stock_data["Time Series (Daily)"][f"{yest}"]["4. close"])
day_b4_stock_price = float(stock_data["Time Series (Daily)"][f"{day_before_yest}"]["4. close"])

value_diff = abs(yest_stock_price - day_b4_stock_price)
percent_diff = round((value_diff / yest_stock_price) * 100, 2)


print(percent_diff)

if percent_diff > 0:
    up_or_down = "Up"
    message = (f"TSLA: {up_or_down} {percent_diff}%\n"
               f"\nHeadline:{articles[f"Article {1}"]["Title"]}\n"
            
               f"Brief:{articles[f"Article {1}"]["Description"]}\n"
               f""
               f"\nHeadline:{articles[f"Article {2}"]["Title"]}\n"
               
               f"Brief:{articles[f"Article {2}"]["Description"]}\n"
               f""
               f"\nHeadline:{articles[f"Article {3}"]["Title"]}\n"
               f"Brief:{articles[f"Article {3}"]["Description"]}\n"
               )

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f"Subject: Stock News\n\n{message}")

elif percent_diff < 0:
    up_or_down = "Down"
    message = (f"TSLA: {up_or_down} {percent_diff}%\n"
               f"Headline:{articles[f"Article {1}"]["Title"]}\n"
               f"Brief:{articles[f"Article {1}"]["Description"]}\n"
               f"Headline:{articles[f"Article {2}"]["Title"]}\n"
               f"Brief:{articles[f"Article {2}"]["Description"]}\n"
               f"Headline:{articles[f"Article {3}"]["Title"]}\n"
               f"Brief:{articles[f"Article {3}"]["Description"]}\n"
               )
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f"Subject: Stock News\n\n{message}")

    print(message)








