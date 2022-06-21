import requests
from pprint import pprint

letter = 'a'

res = requests.get(f"https://query1.finance.yahoo.com/v1/finance/lookup?formatted=true&lang=en-US&region=US&query={letter}*&type=equity&count=3000&start=0")

pprint(res)