# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 07:30:04 2022

Updated at Mon Jun 20 20:30:04 2022

@author: kpritche

@contributor: gravatron
"""

import yfinance as yf
import pandas as pd
from finvizfinance.group.valuation import Valuation
from pprint import pprint
import json
from datetime import datetime

now = datetime.now()

valuation = Valuation()
sector_averages = valuation.screener_view().set_index('Name')

try:
    sp_500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
except:
    sys.exit('could not fetch S&P 500 data')

sp_500.to_csv('S&P500-Info.csv')
sp_500.to_csv("S&P500-Symbols.csv", columns=['Symbol'])

report_columns = [
    'Stock', 'Price', '52-Week High', 'Target Low', 
    'Target Median', 'Target High',
    'Target Low Distance', 'Target Median Distance',
    'Target High Distance', 'Average Value Distance',
    'Trailing P/E', 'Forward P/E', 'PEG', 'P/B', 
    'Trailing P/E Distance ', 'Forward P/E Distance', 
    'PEG Distance', 'P/B Distance', 
    'Average Fundamental Distance', 'Total Average Score',
    'Distance from 52-Week High'
]

sectors = {
    'Basic Materials': pd.DataFrame(columns=report_columns), 
    'Communication Services': pd.DataFrame(columns=report_columns),
    'Consumer Cyclical': pd.DataFrame(columns=report_columns), 
    'Consumer Defensive': pd.DataFrame(columns=report_columns),
    'Energy': pd.DataFrame(columns=report_columns),
    'Financial': pd.DataFrame(columns=report_columns), 
    'Healthcare': pd.DataFrame(columns=report_columns),
    'Industrials': pd.DataFrame(columns=report_columns), 
    'Real Estate': pd.DataFrame(columns=report_columns), 
    'Technology': pd.DataFrame(columns=report_columns),
    'Utilities': pd.DataFrame(columns=report_columns)
}

index = 1
for symbol in sp_500['Symbol']:
    print(f"{index}: Calculating {symbol}...")
    index += 1

    ticker = yf.Ticker(symbol)

    info = ticker.get_info()

    f = open("symbol_info_" + now.strftime("%m%d%Y_%H%M%S") + ".json", "a")
    f.write(json.dumps(info))
    f.close()

    required_fields = [
        'currentPrice', 'fiftyTwoWeekHigh', 'forwardPE', 'pegRatio',
        'priceToBook', 'sector', 'targetLowPrice',
        'targetMedianPrice', 'targetHighPrice', 'trailingPE'
    ]

    if not all(field in info and info[field] and field != None for field in required_fields):
        print(f"{symbol} is missing required data")
        continue

    sector = 'Financial' if info['sector'] == 'Financial Services' else info['sector']

    price = info['currentPrice']
    tld = (info['targetLowPrice'] - price) / price
    tmd = (info['targetMedianPrice'] - price) / price
    thd = (info['targetHighPrice'] - price) / price
    avd = (tld + tmd + thd) / 3

    tped = (sector_averages['P/E'].loc[sector] - info['trailingPE']) / info['trailingPE']
    fped = (sector_averages['Fwd P/E'].loc[sector] - info['forwardPE']) / info['forwardPE']
    pegd = (sector_averages['PEG'].loc[sector] - info['pegRatio']) / info['pegRatio']
    pbd = (sector_averages['P/B'].loc[sector] - info['priceToBook']) / info['priceToBook']
    afd = (tped + fped + pegd + pbd) / 4
    tas = (avd + afd) / 2
    d52 = (info['fiftyTwoWeekHigh'] - info['currentPrice']) / info['currentPrice']

    data = [
        symbol, info['currentPrice'], info['fiftyTwoWeekHigh'], 
        info['targetLowPrice'], info['targetMedianPrice'], 
        info['targetHighPrice'], tld, tmd, thd, avd,
        info['trailingPE'], info['forwardPE'], info['pegRatio'],
        info['priceToBook'], tped, fped, pegd, pbd, afd, tas, d52
    ]

    sectors[sector].loc[len(sectors[sector].index)] = data

for sec in sectors:
    price_avg_score = sectors[sec]['Average Value Distance'].mean()
    fund_avg_score = sectors[sec]['Average Fundamental Distance'].mean()
    tot_avg_score = sectors[sec]['Total Average Score'].mean()
    dist_high_avg = sectors[sec]['Distance from 52-Week High'].mean()

    sectors[sec]['Adjusted Price Score'] = (sectors[sec]['Average Value Distance'] - price_avg_score) / price_avg_score
    sectors[sec]['Adjusted Fund Score'] = (sectors[sec]['Average Fundamental Distance'] - fund_avg_score) / fund_avg_score
    sectors[sec]['Adjusted Total Score'] = (sectors[sec]['Total Average Score'] - tot_avg_score) / tot_avg_score
    sectors[sec]['Adjusted D52 Score'] = (sectors[sec]['Distance from 52-Week High'] - dist_high_avg) / dist_high_avg

    sectors[sec]['Total Score'] = (
        sectors[sec]['Adjusted Price Score'] + 
        sectors[sec]['Adjusted Fund Score'] +
        sectors[sec]['Adjusted Total Score'] +
        sectors[sec]['Adjusted D52 Score']
    )

    sectors[sec].sort_values('Total Score', inplace=True, ascending=False)

with pd.ExcelWriter('SP500 Rebound Analysis v2.xlsx') as writer:
    for df_name, df in sectors.items():
        df.to_excel(writer, sheet_name=df_name)