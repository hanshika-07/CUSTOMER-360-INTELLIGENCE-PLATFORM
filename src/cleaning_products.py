import pandas as pd 
import numpy as np 
products=pd.read_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/raw/products.csv")
print(products.head())
print(products.dtypes)
print(products.isna().sum())
print(products.duplicated().sum())
products.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/clean/products.csv",index=False)
