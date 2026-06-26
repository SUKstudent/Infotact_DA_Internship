import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("/content/multi_touch_attribution_dataset_cleaned.csv")

totalspend = df['ad_spend'].sum()
totalrevenue = df['conversion_value'].sum()

print("Total Spend:", total_spend)
print("Total Revenue:", total_revenue)

roas = totalrevenue / totalspend
print("ROAS:", roas)

attributed_revenue = df["conversion_value"].sum()
print(attributed_revenue)
