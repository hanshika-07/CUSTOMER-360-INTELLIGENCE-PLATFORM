import pandas as pd 
import numpy as np 
marketing_interactions=pd.read_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/raw/marketing_interactions.csv")
#print(marketing_interactions.head())
#print(marketing_interactions.dtypes)
#print(marketing_interactions.isna().sum())
#print(marketing_interactions.duplicated().sum())
marketing_interactions["interaction_timestamp"]=pd.to_datetime(marketing_interactions["interaction_timestamp"],errors='coerce')
print(marketing_interactions.dtypes)
marketing_interactions.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/clean/marketing_interactions.csv",index=False)