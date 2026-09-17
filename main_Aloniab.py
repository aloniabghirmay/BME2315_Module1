import pandas as pd

df = pd.read_csv(r"C:\Users\aloni\OneDrive\Aloniab - University of Virginia\Undergraduate\BME2315 Fall 2026\Module1\BME2315_Module1\BME2315_Module1\BME2315_Module1\Metadata and Protein Data for Module 1.csv")

for header in df.columns:
    print(header)