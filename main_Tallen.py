import pandas as pd

df = pd.read_csv("C:/Users/tall1/Documents/GitHub/BME2315_Module1/Metadata and Protein Data for Module 1.csv")

i = 0
rows = len(df)

for row in df:
    cognitive_status = row['Cognitive Status']
    if cognitive_status == "Dementia":
        print("True")
    else:
        print("False")