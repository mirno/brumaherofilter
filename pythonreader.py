import pandas as pd
import sys

def combine_and_round_down(row):
    full_datetime = pd.to_datetime(f"{row['datum']} {row['tijd']}")
    return full_datetime.replace(minute=0, second=0, microsecond=0)

def process_csv(input_file, output_file):
    # Read tab-separated CSV file
    df = pd.read_csv(input_file, sep='\t')

    # Combine date and time columns and round down
    df['rounded_datetime'] = df.apply(combine_and_round_down, axis=1)

    # Drop duplicates, keeping the first occurrence per hour
    df_filtered = df.drop_duplicates(subset='rounded_datetime', keep='first')

    # Save the filtered data to the specified output CSV file
    df_filtered.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file.csv output_file.csv")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        process_csv(input_file, output_file)
