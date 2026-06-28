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

total_customers = df[df['is_conversion'] == 1]['user_id'].nunique()
cac = total_spend / total_customers #Customer Acquisition Cost
print("CAC:",round(cac,2))

total_regions = df['region'].nunique()
print("Total Regions:", total_regions)

total_touchpoints = df['touchpoint_number'].sum()
print(total_touchpoints)
