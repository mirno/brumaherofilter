import pandas as pd

def combine_and_round_down(row, interval):
    full_datetime = pd.to_datetime(f"{row['datum']} {row['tijd']}")
    # Round down based on the interval
    if interval == 'hourly':
        return full_datetime.replace(minute=0, second=0, microsecond=0)
    else:
        # Round down to the nearest interval in minutes
        minute = (full_datetime.minute // interval) * interval
        return full_datetime.replace(minute=minute, second=0, microsecond=0)

def process_csv(input_file, output_file, delimiter, interval, first_or_last):
    # Read CSV file with the specified delimiter
    df = pd.read_csv(input_file, sep=delimiter)

    # Combine date and time columns and round down
    df['rounded_datetime'] = df.apply(lambda row: combine_and_round_down(row, interval), axis=1)

    # Drop duplicates, keeping the first or last occurrence based on user choice
    keep = 'first' if first_or_last.lower() == 'f' else 'last'
    df_filtered = df.drop_duplicates(subset='rounded_datetime', keep=keep)

    # Save the filtered data to the specified output CSV file
    df_filtered.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

if __name__ == "__main__":
    input_file = input("Enter input CSV file path (default: data/input.csv): ") or "data/input.csv"
    output_file = input("Enter output CSV file path (default: data/output.csv): ") or "data/output.csv"
    delimiter_choice = input("Choose delimiter - Comma (C) or Tab (T) [default: Comma]: ") or "C"
    delimiter = ',' if delimiter_choice.upper() == 'C' else '\t'
    interval_choice = input("Choose time interval - Hourly (H) or Minutes (M) [default: Hourly]: ") or "H"
    interval = 60 if interval_choice.upper() == 'H' else int(input("Enter the number of minutes for interval: "))
    first_or_last = input("Choose First (F) or Last (L) entry for each interval [default: First]: ") or "F"

    process_csv(input_file, output_file, delimiter, interval, first_or_last)
