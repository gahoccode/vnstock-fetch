from vnstock import Vnstock
source = 'VCI' # 'VCI' hoặc 'TCBS'

stock = Vnstock().stock(symbol='VCI', source='VCI')
# Bảng cân đối kế toán - năm (period='quarter')
BalanceSheet = stock.finance.balance_sheet(period='year', lang='vi', dropna=True)

IncomeStatement = stock.finance.income_statement(period='year', lang='vi', dropna=True)
# Lưu chuyển tiền tệ
CashFlow = stock.finance.cash_flow(period='year', dropna=True)
# Chỉ số tài chính
Ratio = stock.finance.ratio(period='year', lang='vi', dropna=True)

def save_to_csv(BalanceSheet, IncomeStatement, CashFlow, Ratio):
    BalanceSheet.to_csv('BalanceSheet.csv')
    IncomeStatement.to_csv('IncomeStatement.csv')
    CashFlow.to_csv('CashFlow.csv')
    Ratio.to_csv('Ratio.csv')
save_to_csv(BalanceSheet, IncomeStatement, CashFlow, Ratio)
