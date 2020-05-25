import pandas as pd
import numpy as np
from geopy import distance

df = pd.read_csv('201809-citibike-tripdata.csv')

# total number of rows and columns in the dataset
_shape = df.shape
# Find the average trip length in minutes (tripduration column) accurate to 2 digits
_apply = df['tripduration'].apply(lambda x: x / 60)
_mean = round(_apply.mean(), 2)

# How many trips started and ended at the same station?
df_same_1 = df.where(df['start station name'] == df['end station name']).notnull()
_list = [station_name for station_name in df_same_1['start station name'] if station_name is True]
stations_value = len(_list)

# What is the most used bikeid in the city by the number of rides?
s = df['bikeid'].value_counts().head()

# bike id (bikeid), which on average has longer rides than all others
df_group = df.groupby('bikeid')[['tripduration']].sum().sort_values(['tripduration'], ascending=False)


# How many rows are missing start station id data?
_list = [station_name for station_name in df['start station name'].notnull() if station_name is False]
empty_rows = len(_list)

# average trip duration in minutes depending on the type of subscription
df_group = df.groupby('usertype')[['tripduration']].mean()
_apply = round(df_group.apply(lambda x: x/60), 2)

# the average length of trips in kilometers with an accuracy of 2 digits, previously throwing closed trajectories
df_rc = df.drop(np.where(df['start station name'] == df['end station name'])[0])
df['start'] = list(zip(df['start station latitude'], df['start station longitude']))
df['end'] = list(zip(df_rc['end station latitude'], df_rc['end station longitude']))

