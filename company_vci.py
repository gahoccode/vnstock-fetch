from vnstock.explorer.vci import Company
company = Company('ACB')
# Báo cáo
CompanyReports = company.reports()
CompanyAffiliate = company.affiliate()

WorkingStatus='working'
CompanyOfficers = company.officers(filter_by=WorkingStatus).head() # filter_by='all' hoặc 'working' hoặc 'resigned'

def save_to_csv():
    CompanyOfficers.to_csv('CompanyOfficers.csv', index=False)
    CompanyReports.to_csv('CompanyReports.csv', index=False)
    CompanyAffiliate.to_csv('CompanyAffiliate.csv', index=False)1
save_to_csv()