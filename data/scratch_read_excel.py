import os
import pandas as pd

raw_dir = "d:\\Bluestock_Fintech\\nifty100-financial-intelligence\\data\\raw"
for file in os.listdir(raw_dir):
    if file.endswith('.xlsx'):
        path = os.path.join(raw_dir, file)
        try:
            df = pd.read_excel(path, header=1, nrows=0)
            print(f"--- {file} ---")
            print(list(df.columns))
        except Exception as e:
            print(f"Error reading {file}: {e}")
