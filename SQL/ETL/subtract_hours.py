import pandas as pd
from datetime import timedelta

# load the CSV
df = pd.read_csv('absences_filtered.csv')

# ensure 'All day event' is boolean
df['All day event'] = df['All day event'].astype(bool)

# filter rows where 'All day event' is False
mask = ~df['All day event']

# define the time format
time_format = '%I:%M:%S %p'

# convert time strings to datetime (with dummy date) for the affected rows
start_times = pd.to_datetime(df.loc[mask, 'Start Time'], format=time_format)
end_times = pd.to_datetime(df.loc[mask, 'End Time'], format=time_format)

# subtract 3 hours
start_times_adjusted = start_times - timedelta(hours=3)
end_times_adjusted = end_times - timedelta(hours=3)

# format back to string with AM/PM
df.loc[mask, 'Start Time'] = start_times_adjusted.dt.strftime(time_format)
df.loc[mask, 'End Time'] = end_times_adjusted.dt.strftime(time_format)

# save the result to a new file
df.to_csv('adjusted_absences.csv', index=False)

print("adjusted times saved to 'adjusted_absences.csv'")