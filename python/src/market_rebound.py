# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 07:30:04 2022

@author: kpritche
"""

import yfinance as yf
import pandas as pd
from finvizfinance.group.valuation import Valuation
from pprint import pprint

valuation = Valuation()
sector_averages = valuation.screener_view()
sector_averages = sector_averages.set_index('Name')

# table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# sp = table[0]
# sp.to_csv('S&P500-Info.csv')
# sp.to_csv("S&P500-Symbols.csv", columns=['Symbol'])

basic_mats = pd.DataFrame(columns=['Stock', 'Price', '52-Week High', 'Target Low', 
                           'Target Median', 'Target High',
                           'Target Low Distance', 'Target Median Distance',
                           'Target High Distance', 'Average Value Distance',
                           'Trailing P/E', 'Forward P/E', 'PEG', 'P/B', 
                           'Trailing P/E Distance ', 'Forward P/E Distance', 
                           'PEG Distance', 'P/B Distance', 
                           'Average Fundamental Distance', 'Total Average Score',
                           'Distance from 52-Week High'])

com_serv = pd.DataFrame(columns=basic_mats.columns)
con_cyc = pd.DataFrame(columns=basic_mats.columns)
con_def = pd.DataFrame(columns=basic_mats.columns)
energy = pd.DataFrame(columns=basic_mats.columns)
fin = pd.DataFrame(columns=basic_mats.columns)
health = pd.DataFrame(columns=basic_mats.columns)
ind = pd.DataFrame(columns=basic_mats.columns)
real_estate = pd.DataFrame(columns=basic_mats.columns)
tech = pd.DataFrame(columns=basic_mats.columns)
util = pd.DataFrame(columns=basic_mats.columns)

sectors = {
    'Basic Materials': basic_mats, 
    'Communication Services': com_serv,
    'Consumer Cyclical': con_cyc, 
    'Consumer Defensive': con_def,
    'Energy': energy,
    'Financial': fin, 
    'Healthcare': health,
    'Industrials': ind, 
    'Real Estate': real_estate, 
    'Technology': tech,
    'Utilities': util
}

sp = {"Symbol": ['MMM', 'AOS']}

i=0
for tick in sp['Symbol']:
    print(tick)
    i += 1
    ticker = yf.Ticker(tick)
    info = ticker.get_info()
    
    try:
        info['targetLowPrice']
        info['trailingPE']
        info['sector']
        info['priceToBook']
        
    except:
        continue
    
    sector = info['sector']
    if sector == 'Financial Services':
        sector = 'Financial'
    print(sector)    
    if (info['targetLowPrice'] and info['priceToBook'] and info['pegRatio'] and info['trailingPE'] and info['forwardPE']) != None:
        price = info['currentPrice']
        tld = (info['targetLowPrice'] - price)/price
        tmd = (info['targetMedianPrice'] - price)/price
        thd = (info['targetHighPrice'] - price)/price
        avd = (tld + tmd + thd) / 3
        
        tped = (sector_averages['P/E'].loc[sector] - info['trailingPE']) / info['trailingPE']
        fped = (sector_averages['Fwd P/E'].loc[sector] - info['forwardPE']) / info['forwardPE']
        pegd = (sector_averages['PEG'].loc[sector] - info['pegRatio']) / info['pegRatio']
        pbd = (sector_averages['P/B'].loc[sector] - info['priceToBook']) / info['priceToBook']
        afd = (tped + fped + pegd + pbd)/4
        tas = (avd + afd) / 2
        d52 = (info['fiftyTwoWeekHigh'] - info['currentPrice'])/info['currentPrice']
        
        data = [tick, info['currentPrice'], info['fiftyTwoWeekHigh'], 
                info['targetLowPrice'], info['targetMedianPrice'], 
                info['targetHighPrice'],
                tld, tmd, thd, avd,
                info['trailingPE'],
                info['forwardPE'], info['pegRatio'], info['priceToBook'],
                tped, fped, pegd, pbd, afd,
                tas, d52]
        pprint(data)
        
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
    
    sectors[sec]['Total Score'] = (sectors[sec]['Adjusted Price Score'] + 
                                   sectors[sec]['Adjusted Fund Score'] +
                                   sectors[sec]['Adjusted Total Score'] +
                                   sectors[sec]['Adjusted D52 Score']
                                   )
    sectors[sec].sort_values('Total Score', inplace=True, ascending=False)

with pd.ExcelWriter('SP500 Rebound Analysis.xlsx') as writer:
    
    for df_name, df in sectors.items():
        df.to_excel(writer, sheet_name=df_name)