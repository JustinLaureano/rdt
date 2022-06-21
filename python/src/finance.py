import yfinance as yf
from pprint import pprint

ticker = yf.Ticker('A*')

# get stock info
pprint(ticker.info)
# pprint(ticker.actions)

# fields required to find

# sector            info.sector
# stock ticker      info.symbol
# price             info.currentPrice
# 52 week high      info.fiftyTwoWeekHigh
# fair value
# morning star value
# one year target   info.targetMeanPrice
# trailing p/e      info.trailingPE
# forward P/E       info.forwardPE
# PEG               info.pegRatio ??
# P/B               


# pprint('')
# pprint('')
# pprint(ticker.financials)

# pprint('')
# pprint('')
# pprint(ticker.earnings)


# get historical market data
# hist = ticker.history(period="max")

# # show actions (dividends, splits)
# ticker.actions

# # show dividends
# ticker.dividends

# # show splits
# ticker.splits

# # show financials
# ticker.financials
# ticker.quarterly_financials

# # show major holders
# ticker.major_holders

# # show institutional holders
# ticker.institutional_holders

# # show balance sheet
# ticker.balance_sheet
# ticker.quarterly_balance_sheet

# # show cashflow
# ticker.cashflow
# ticker.quarterly_cashflow

# # show earnings
# ticker.earnings
# ticker.quarterly_earnings

# # show sustainability
# ticker.sustainability

# # show analysts recommendations
# ticker.recommendations

# # show next event (earnings, etc)
# ticker.calendar

# # show all earnings dates
# ticker.earnings_dates

# # show ISIN code - *experimental*
# # ISIN = International Securities Identification Number
# ticker.isin

# # show options expirations
# ticker.options

# # show news
# ticker.news
