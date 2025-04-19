import pandas as pd
df = pd.read_csv("car_data.csv")
print("\n--- Cars with Buy Price > 3000 ---")
print(df[df['Buy Price'] > 3000])
print("\n--- Cars Sorted by Buy Price (Ascending) ---")
print(df.sort_values(by='Buy Price'))
print("\n--- Grouped Data by 'Model' ---")
grouped = df.groupby('Model')

for name, group in grouped:
    print(f"\n{name} Cars:")
    print(group)
