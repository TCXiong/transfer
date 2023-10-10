import os
import pandas as pd

def preprocess_csv(input_path, output_folder):
    # Read the CSV file
    df = pd.read_csv(input_path)

    # Delete the previous three columns
    df = df.iloc[:, 3:]

    # Extract the filename (without extension) from the input path
    filename = os.path.splitext(os.path.basename(input_path))[0]

    # Create the output path with the "modified" prefix
    output_path = os.path.join(output_folder, f"modified_{filename}.csv")

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_path, index=False)

def preprocess_all_csv_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all CSV files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            input_path = os.path.join(input_folder, filename)

            # Preprocess the current CSV file
            preprocess_csv(input_path, output_folder)

if __name__ == "__main__":
    # Specify the input and output folders
    input_folder = "./data"
    output_folder = "./modified"

    # Preprocess all CSV files in the input folder
    preprocess_all_csv_files(input_folder, output_folder)
