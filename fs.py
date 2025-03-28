from vnstock import Vnstock
source = 'VCI' # 'VCI' hoặc 'TCBS'

stock = Vnstock().stock(symbol='VCI', source=source)
# Bảng cân đối kế toán - năm (period='quarter')
BalanceSheet = stock.finance.balance_sheet(period='year', lang='vi', dropna=True)

IncomeStatement = stock.finance.income_statement(period='year', lang='vi', dropna=True)
# Lưu chuyển tiền tệ
CashFlow = stock.finance.cash_flow(period='year', dropna=True)
# Chỉ số tài chính
Ratio = stock.finance.ratio(period='year', lang='vi', dropna=True)

def save_to_csv():
    BalanceSheet.to_csv('BalanceSheet.csv', index=False)
    IncomeStatement.to_csv('IncomeStatement.csv', index=False)
    CashFlow.to_csv('CashFlow.csv', index=False)
    Ratio.to_csv('Ratio.csv', index=False)
#save_to_csv()

#-------------------------------------------------




