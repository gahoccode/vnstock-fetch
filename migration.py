from vnstock import Finance, Company
from rich import print
from rich.progress import Progress


company = Company(symbol='VCB')
company.insider_deals()
print(company.insider_deals())


#Migration from legacy vnstock to vnstock 3
#https://vnstocks.com/docs/tai-lieu/migration-chuyen-doi-sang-vnstock3
#Instantiate
report = Finance(symbol='ACB', period='quarter') #period must be 'quarter' or 'year'

#print(report.balance_sheet(lang='vi'))

report.income_statement(lang='vi')
#print(report.income_statement(lang='vi'))

report.cash_flow(lang='vi')
#print(report.cash_flow(lang='vi'))

from vnstock import Quote
#stock.trading.price_board(['ACB'])
from vnstock import Vnstock
stock = Vnstock().stock(symbol='ACB', source='VCI')
stock.quote.history(start='2024-01-01', end='2024-12-31')
#print(stock.quote.history(start='2024-01-01', end='2024-12-31'))

#Giá và khối lượng khớp lệnh
stock.quote.price_depth('ACB')
#print(stock.quote.price_depth('ACB'))

from vnstock.explorer.tcbs import Company
company = Vnstock().stock(symbol='VCB', source='TCBS').company
company.dividends()
#print(company.dividends())

# Get and save company news to CSV
company_news = company.news()

# import pandas as pd
# if not isinstance(company_news, pd.DataFrame):
#     company_news = pd.DataFrame(company_news)
# company_news.to_csv("company_news.csv", index=False, encoding="utf-8-sig")

# print("[bold green]Company news has been saved to company_news.csv with UTF-8 encoding for Excel compatibility.[/bold green]")
# print(company_news)


