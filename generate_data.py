import pandas as pd
import numpy as np

# Date range: Jan 2020 to Dec 2024
dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='MS')

records = []

# Base rates
base_food = 6.0
base_fuel = 5.0
base_health = 10.0

for date in dates:
    # Food: Seasonal fluctuations + slight upward trend
    food_noise = np.random.normal(0, 1.5)
    food_trend = (date.year - 2020) * 0.5
    food_rate = max(2.0, base_food + food_trend + food_noise)
    
    # Fuel: Volatile due to global events
    fuel_noise = np.random.normal(0, 3.0)
    fuel_shock = 5.0 if date.year == 2022 else 0 # 2022 shock
    fuel_rate = max(0.5, base_fuel + fuel_shock + fuel_noise)

    # Health: Steady high inflation
    health_noise = np.random.normal(0, 0.5)
    health_trend = (date.year - 2020) * 0.8
    health_rate = max(5.0, base_health + health_trend + health_noise)

    records.append({"date": date, "category": "Food", "rate": round(food_rate, 2)})
    records.append({"date": date, "category": "Fuel", "rate": round(fuel_rate, 2)})
    records.append({"date": date, "category": "Healthcare", "rate": round(health_rate, 2)})

df = pd.DataFrame(records)
df.to_csv('backend/data/inflation_history.csv', index=False)
print("CSV Generated")
