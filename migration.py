from vnstock import Finance

#Migration from legacy vnstock to vnstock 3
#Instantiate
report = Finance(symbol='ACB', period='year')
from rich import print
print(report.balance_sheet(lang='vi'))