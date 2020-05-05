from bs4 import BeautifulSoup
import requests
from csv import writer

res = requests.get("https://etfdb.com/etfs/asset-class/#etfs__expenses&sort_name=assets_under_management&sort_order=desc&page=1")

soup = BeautifulSoup(res.text, 'html.parser')



etfs = soup.find_all('tr')

with open('etfs.csv', 'w') as csv_file:
    cvs_writer = writer(csv_file)
    headers=['symbol', 'name', 'category', 'expense_ratio']
    cvs_writer.writerow(headers)

    
    for etf in etfs:
        symbols = etf.find_all("td", attrs={'data-th': 'Symbol'})
        for symbol in symbols:
            sym = symbol.get_text()
            
        

        etf_names = etf.find_all("td", attrs={'data-th': 'ETF Name'})
        for etf_name in etf_names:
            name = etf_name.get_text()

        etf_categories = etf.find_all("td", attrs={'data-th': 'ETFdb.com Category'})
        for etf_category in etf_categories:
            category = etf_category.get_text()

        etf_ers = etf.find_all("td", attrs={'data-th': 'ER'})
        for etf_er in etf_ers:
            er = etf_er.get_text()
            cvs_writer.writerow([sym, name,category, er])


            
    



    



