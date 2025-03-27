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

def save_to_csv():
    BalanceSheet.to_csv('BalanceSheet.csv', index=False)
    IncomeStatement.to_csv('IncomeStatement.csv', index=False)
    CashFlow.to_csv('CashFlow.csv', index=False)
    Ratio.to_csv('Ratio.csv', index=False)
#save_to_csv()

company = Vnstock().stock(symbol='VCB', source='TCBS').company

"""#### Tổng quan"""

CompanyOverview = company.overview()

"""#### Hồ sơ"""

CompanyProfile = company.profile()

"""#### Cổ đông"""

CompanyShareholders = company.shareholders()

"""#### Giao dịch nội bộ"""

CompanyInsiderDeals = company.insider_deals().head(3)

"""#### Công ty con, liên kết"""

CompanySubsidiaries = company.subsidiaries().head()

"""#### Ban lãnh đạo"""

CompanyOfficers = company.officers().head()

"""#### Sự kiện"""

CompanyEvents = company.events().head()

"""#### Tin tức"""

CompanyNews = company.news().head()

"""#### Cổ tức"""

CompanyDividends = company.dividends().head()

def save_company_data():
    CompanyOverview.to_csv('CompanyOverview.csv', index=False)
    CompanyProfile.to_csv('CompanyProfile.csv', index=False)
    CompanyShareholders.to_csv('CompanyShareholders.csv', index=False)
    CompanyInsiderDeals.to_csv('CompanyInsiderDeals.csv', index=False)
    CompanySubsidiaries.to_csv('CompanySubsidiaries.csv', index=False)
    CompanyOfficers.to_csv('CompanyOfficers.csv', index=False)
    CompanyEvents.to_csv('CompanyEvents.csv', index=False)
    CompanyNews.to_csv('CompanyNews.csv', index=False)
    CompanyDividends.to_csv('CompanyDividends.csv', index=False)
#save_company_data()
