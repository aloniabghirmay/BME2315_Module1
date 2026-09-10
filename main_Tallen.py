import pandas as pd

df = pd.read_csv("C:/Users/tall1/Documents/GitHub/BME2315_Module1/Metadata and Protein Data for Module 1.csv")

for header in df.columns:
    print(header)