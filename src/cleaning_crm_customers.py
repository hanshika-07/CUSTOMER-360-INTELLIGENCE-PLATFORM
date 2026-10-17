import pandas as pd 
import numpy as np 
crm_customers=pd.read_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/raw/crm_customers.csv")
#print(crm_customers.head())
#print(crm_customers.dtypes)
#print(crm_customers.isna().sum())
#print(crm_customers.duplicated().sum())
#crm_customers["signup_date"]=pd.to_datetime(crm_customers["signup_date"],errors='coerce')
#print(crm_customers.dtypes)
crm_customers["city"]=crm_customers["city"].fillna(crm_customers["city"].mode()[0])
print(crm_customers.isna().sum())
crm_customers.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/clean/crm_customers.csv",index=False)