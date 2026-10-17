import pandas as pd 
import numpy as np 
support_tickets=pd.read_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/raw/support_tickets.csv")
print(support_tickets.head())
print(support_tickets.duplicated().sum())
support_tickets["created_date"]=pd.to_datetime(support_tickets["created_date"],errors='coerce')
support_tickets["resolution_time_hours"]=pd.to_numeric(support_tickets["resolution_time_hours"],errors='coerce')
print(support_tickets.dtypes)
support_tickets["resolution_time_hours"]=support_tickets["resolution_time_hours"].fillna(support_tickets["resolution_time_hours"].mean())
support_tickets["satisfaction_score"]=support_tickets["satisfaction_score"].fillna(support_tickets["satisfaction_score"].mode()[0])
print(support_tickets.isna().sum())
support_tickets.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/clean/support_tickets.csv",index=False)
