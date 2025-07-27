import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import hashlib




#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f)

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']


def calculate_directory_hash(directory_path):
    """Write hash for directory contents to a file"""
    sha256_hash = hashlib.sha256()

    for filename in sorted(os.listdir(directory_path)):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256_hash.update(chunk)

    return sha256_hash.hexdigest()[:8]  # 처음 8자리만 사용


def data_integrity_check(df):
    """Run basic integrity checks on the data and return a list of issues"""
    integrity_issues = []

    # 중복 행 검사
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        integrity_issues.append(f"Found duplicates: {duplicates}")

    # Null 값 검사
    null_counts = df.isnull().sum()
    for column, count in null_counts.items():
        if count > 0:
            integrity_issues.append(f"at coulmn {column}, {count} number of Null values was found")

    return integrity_issues


#############Function for data ingestion
def merge_multiple_dataframe():
    #check for datasets, compile them together, and write to an output file
    # check if input_folder_path exist
    if not os.path.exists(input_folder_path):
        raise FileNotFoundError(f"Can't find directory: {input_folder_path}")

    # Create output directory if there isn't one
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # get the list of CSV files
    csv_files = [f for f in os.listdir(input_folder_path) if f.endswith('.csv')]
    if not csv_files:
        raise ValueError(f"No csv files found it input directory: {input_folder_path}")

    # get list of dataframes
    df_list = []
    for file in csv_files:
        file_path = os.path.join(input_folder_path, file)
        df = pd.read_csv(file_path)
        df_list.append(df)

    # merge the dataset and remove duplicates
    merged_df = pd.concat(df_list, axis=0, ignore_index=True)
    merged_df = merged_df.drop_duplicates()

    # basic integrity test
    integrity_issues = data_integrity_check(merged_df)

    # calculate hash for the directory
    dir_hash = calculate_directory_hash(input_folder_path)

    # the output will be saved in `output_folder_path/dir_hash`
    # this will ensure if data is changed we'll track the output
    hash_output_dir = os.path.join(output_folder_path, dir_hash)
    if not os.path.exists(hash_output_dir):
        os.makedirs(hash_output_dir)

    save_dirs = [hash_output_dir, output_folder_path]
    for save_dir in save_dirs:
        # save to finaldata.csv directly in the output folder
        output_file = os.path.join(save_dir, 'finaldata.csv')
        merged_df.to_csv(output_file, index=False)

        # create ingestedfiles.txt and save which files we've ingested
        ingested_files_path = os.path.join(save_dir, 'ingestedfiles.txt')
        with open(ingested_files_path, 'w') as f:
            f.write(f"Processed Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("List of ingested files:\n")
            for file in csv_files:
                f.write(f"- {file}\n")
            if integrity_issues:
                f.write("\nData integrity check:\n")
                for issue in integrity_issues:
                    f.write(f"- {issue}\n")

    print(f"Completed data ingestion. Output is saved in: {output_folder_path}")
    print(f"Number of ingested files: {len(csv_files)}")
    print(f"Number of records in final merged dataset: {len(merged_df)}")


if __name__ == '__main__':
    merge_multiple_dataframe()
