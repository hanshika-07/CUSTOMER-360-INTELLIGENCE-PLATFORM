import pandas as pd 
import numpy as np 
product_usage=pd.read_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/raw/product_usage_events.csv")
#print(product_usage.head())
#print(product_usage.dtypes)
#print(product_usage.isna().sum())
#print(product_usage.duplicated().sum())
product_usage["event_timestamp"]=pd.to_datetime(product_usage["event_timestamp"],errors='coerce')
product_usage["session_duration_seconds"]=pd.to_numeric(product_usage["session_duration_seconds"],errors='coerce')
print(product_usage.dtypes)
product_usage.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/clean/product_usage.csv",index=False)
