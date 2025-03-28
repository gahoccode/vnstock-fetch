CompanyDataSource='TCBS'
company = Vnstock().stock(symbol='VCB', source=CompanyDataSource).company

# Tổng quan
CompanyOverview = company.overview()
# Hồ sơ
CompanyProfile = company.profile()
# Cổ đông
CompanyShareholders = company.shareholders()
# Giao dịch nội bộ
CompanyInsiderDeals = company.insider_deals()
# Giao dịch ngoại bộ
CompanySubsidiaries = company.subsidiaries()
# Ban lãnh đạo
CompanyOfficers = company.officers()
# Sự kiện
CompanyEvents = company.events()
# Tin tức
CompanyNews = company.news()
# Cổ tức        
CompanyDividends = company.dividends()


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
