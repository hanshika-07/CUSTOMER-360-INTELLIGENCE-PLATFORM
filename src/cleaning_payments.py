import pandas as pd 
import numpy as np 
payments=pd.read_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/raw/payments.csv")
print(payments.head())
print(payments.dtypes)
print(payments.isna().sum())
print(payments.duplicated().sum())
payments["pay_date"]=pd.to_datetime(payments["pay_date"],errors='coerce')
print(payments.dtypes)
#print(payments.isna().sum())
#print(payments.duplicated().sum())
payments.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/clean/payments.csv",index=False)