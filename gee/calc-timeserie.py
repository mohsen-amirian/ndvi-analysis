import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv('./data-11-10/Germany_Quarterly_NDVI_L8.csv')

# Convert time (in milliseconds) to a datetime format
data['time'] = pd.to_datetime(data['time'], unit='ms')

# Plot the NDVI time series
plt.figure(figsize=(10, 6))
plt.plot(data['time'], data['mean_NDVI'], color='green', marker='o')
plt.title('Quarterly NDVI Time Series for Germany')
plt.xlabel('Date')
plt.ylabel('Mean NDVI')
plt.grid(True)
plt.show()