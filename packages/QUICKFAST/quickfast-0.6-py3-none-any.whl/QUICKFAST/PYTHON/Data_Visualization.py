#pip install pandas
#pip install matplotlib.pyplot or pip install matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file using pandas
data = pd.read_csv('mat_data.csv', parse_dates=['Date'])

# Display the first few rows of the data
print(data.head())

# to display multiple plots at once.figsize=(14, 10): This specifies the size of the overall figure in inches
fig, ax = plt.subplots(2, 2, figsize=(14, 10))

# Line Plot: Sales and Profit over Time
#marker='o'=to specify the shape of the markers that represent data points on a plot 'o':circle as the marker
ax[0, 0].plot(data['Date'], data['Sales'], label='Sales', color='b', marker='o')
ax[0, 0].plot(data['Date'], data['Profit'], label='Profit', color='g', marker='x')
ax[0, 0].set_title('Sales and Profit Over Time')
ax[0, 0].set_xlabel('Date')
ax[0, 0].set_ylabel('Amount')
ax[0, 0].legend()#A legend is used to label different plot elements (such as lines, markers, or bars)

# Bar Plot: Sales vs. Advertising
ax[0, 1].bar(data['Date'], data['Sales'], width=0.4, label='Sales', color='b', align='center')
ax[0, 1].bar(data['Date'], data['Advertising'], width=0.4, label='Advertising', color='orange', align='edge')
ax[0, 1].set_title('Sales vs Advertising')
ax[0, 1].set_xlabel('Date')
ax[0, 1].set_ylabel('Amount')
ax[0, 1].legend()

# Scatter Plot: Profit vs. Advertising
ax[1, 0].scatter(data['Advertising'], data['Profit'], color='r')
ax[1, 0].set_title('Profit vs Advertising')
ax[1, 0].set_xlabel('Advertising Spend')
ax[1, 0].set_ylabel('Profit')

# Histogram: Distribution of Sales
ax[1, 1].hist(data['Sales'], bins=5, edgecolor='black', color='skyblue')
ax[1, 1].set_title('Sales Distribution')
ax[1, 1].set_xlabel('Sales')
ax[1, 1].set_ylabel('Frequency')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()
