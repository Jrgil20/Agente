import pandas as pd
import argparse
import os

def clean_tweet_data(input_file, output_file):
    """
    Reads a CSV file, removes duplicate rows based on tweet_id,
    and saves the cleaned data to a new file.
    """
    try:
        if not os.path.exists(input_file):
            print(f"Error: File not found at {input_file}")
            return

        print(f"Reading data from {input_file}...")
        df = pd.read_csv(input_file)

        initial_rows = len(df)
        print(f"Initial number of tweets: {initial_rows}")

        # Drop duplicates based on the 'tweet_id' column
        df.drop_duplicates(subset=['tweet_id'], inplace=True, keep='first')

        cleaned_rows = len(df)
        print(f"Number of tweets after cleaning: {cleaned_rows}")
        print(f"Number of duplicate tweets removed: {initial_rows - cleaned_rows}")

        # Save the cleaned data to the output file
        df.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean tweet data by removing duplicates.')
    parser.add_argument('input_file', help='The path to the input CSV file.')
    parser.add_argument('output_file', help='The path to the output CSV file.')
    args = parser.parse_args()
    
    clean_tweet_data(args.input_file, args.output_file) 