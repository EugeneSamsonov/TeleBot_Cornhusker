import requests
from bs4 import BeautifulSoup

url = 'https://www.banki.ru/products/currency/cb/'


source = requests.get(url)
main_text = source.text
soup = BeautifulSoup(main_text, features="html.parser")

usd_text = soup.find('tr', {'data-currency-code': 'USD'}).text
eur_text = soup.find('tr', {'data-currency-code': 'EUR'}).text

rate_usd = float(usd_text[34:41])
rate_change_usd = usd_text[48:55]


rate_eur = float(eur_text[28:35])
rate_change_eur = eur_text[42:49]
