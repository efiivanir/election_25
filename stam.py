import pandas as pd
#Define the csv URL
file_url = 'https://raw.githubusercontent.com/PacktWorkshops/The-Pandas-Workshop/master/Chapter07/Data/grouping.csv'
data_frame = pd.read_csv(file_url)

# Grouping the data
grouped = data_frame.groupby('store_id')[['sales']]
grouped
# Sum aggregation
a = grouped.sum()

#Define the csv URL
file_url = 'https://raw.githubusercontent.com/PacktWorkshops/The-Pandas-Workshop/master/Chapter07/Data/pivot.csv'
data_frame = pd.read_csv(file_url)
#Display the DataFrame
data_frame
a = pd.pivot_table(data_frame, index = 'brand', values = 'sales',aggfunc='sum')
