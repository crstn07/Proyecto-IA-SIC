import pandas as pd

def merge_and_clean_csv(file_paths, output_file):
    """
    Combines multiple CSV files into a single CSV file and cleans the data.

    Args:
        file_paths: A list of file paths to the CSV files to be merged.
        output_file: The file path for the merged and cleaned CSV file.
    """
    try:
        # Create an empty list to store dataframes
        all_dataframes = []

        # Loop through file paths and read CSV files into dataframes
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path)
                all_dataframes.append(df)
            except FileNotFoundError:
                print(f"Error: File not found at {file_path}")
                return  # Exit if a file is not found

        # Concatenate all dataframes into a single dataframe
        merged_df = pd.concat(all_dataframes, ignore_index=True)

        # Remove duplicates
        merged_df.drop_duplicates(inplace=True)

        # Handle missing values (example: fill with empty string)
        merged_df.fillna('', inplace=True)

        # Save the merged and cleaned dataframe to a new CSV file
        merged_df.to_csv(output_file, index=False)
        print(f"Successfully merged and cleaned data into {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


file_paths = ['amazon_prime.csv', 'disney_plus.csv', 'hulu_plus.csv', 'netflix.csv']  # Replace with your file paths
output_file = 'dataset.csv'
merge_and_clean_csv(file_paths, output_file)