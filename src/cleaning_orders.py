import pandas as pd 
import numpy as np 
orders=pd.read_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/raw/orders.csv")
print(orders.head())
print(orders.dtypes)
print(orders.isna().sum())
print(orders.duplicated().sum())
orders["order_date"]=pd.to_datetime(orders["order_date"],errors='coerce')
print(orders.dtypes)
#orders["city"]=orders["city"].fillna(orders["city"].mode()[0])
print(orders.isna().sum())
orders.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/clean/orders.csv",index=False)