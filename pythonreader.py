import pandas as pd

# Function to combine date and time and round down to the nearest hour
def combine_and_round_down(row):
    full_datetime = pd.to_datetime(f"{row['datum']} {row['tijd']}")
    return full_datetime.replace(minute=0, second=0, microsecond=0)

# Read CSV file
df = pd.read_csv('data/input.csv')

# Combine date and time columns and round down
df['rounded_datetime'] = df.apply(combine_and_round_down, axis=1)

# Drop duplicates, keeping the first occurrence per hour
df_filtered = df.drop_duplicates(subset='rounded_datetime', keep='first')

# Save the filtered data to a new CSV file
df_filtered.to_csv('data/filtered_data_hourly.csv', index=False)
