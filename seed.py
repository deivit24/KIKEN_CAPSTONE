from csv import DictReader
from app import app
from models import db, Portfolios, User, ETFs

db.drop_all()
db.create_all()
db.session.rollback()

p1 = Portfolios(name='Preservation',  AGG=75, BIL=25, fees=.0006, desc="A preservation portfolio is most appropriate for those that are in retirement, very low tolerance for risk and/or looking for  consistent monthly interest. This portfolio is 100% weighted towards fixed income.")
p2 = Portfolios(name='Conservative', ITOT=20, AGG=60, VNQ=5, GLD=5, BIL=10, fees=.0007, desc="A conservative portfolio is most appropriate for those with short time horizons, close to retirement, or low tolerance for risk. This portfolio is weighted towards fixed income.")
p3 = Portfolios(name='Balanced', ITOT=30, VEA=10, VNQ=5, GLD=5,  AGG=45, BIL=5, fees=.0006, desc="A balanced portfolio is most appropriate for those with medium time horizons and moderate risk tolerance. This portfolio is balanced between equity and fixed income")
p4 = Portfolios(name='Aggressive', ITOT=50, VEA=15, VNQ=10, GLD=5, AGG=20, fees=.0006, desc="A aggressive portfolio is most appropriate for those with longer time horizons, young in age, and a higher risk tolerance.")
p5 = Portfolios(name='All Equity', ITOT=60, VEA=20, VNQ=15, GLD=5, fees=.0007, desc="A all equity portfolio is most appropriate for those with longer time horizons, young in age, higher risk tolerance and high capacity to take risk.This portfolio is 100% weighted towards equity")






db.session.add_all([p1, p2, p3, p4, p5])
db.session.commit()



with open('generator/etfs.csv') as etfs:
    db.session.bulk_insert_mappings(ETFs, DictReader(etfs))

db.session.commit()