import pandas as pd

xlsx = pd.read_excel("50 Deutsche Lieder.xlsx")
xlsx.to_csv("50 Deutsche Lieder.csv")