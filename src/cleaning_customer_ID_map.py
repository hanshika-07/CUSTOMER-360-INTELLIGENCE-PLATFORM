import pandas as pd 
import numpy as np 
customer_id_map=pd.read_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/raw/customer_ID_map.csv")
print(customer_id_map.head())
#print(customer_id_map.dtypes)
print(customer_id_map.isna().sum())
print(customer_id_map.duplicated().sum())
customer_id_map["mapping_created_date"]=pd.to_datetime(customer_id_map["mapping_created_date"],errors='coerce')
print(customer_id_map.dtypes)
customer_id_map.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/clean/customer_ID_map.csv",index=False)