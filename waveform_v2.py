import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
file_path = 'test.csv'  # Replace with the actual file path
df = pd.read_csv(file_path, header=None)

# Define a window size for checking flatness
window_size = 10

# Calculate the standard deviation in a rolling window
rolling_std = df.iloc[:, 1].rolling(window=window_size).std()

# Find indices where the standard deviation is below a threshold
flat_part_indices = np.where(rolling_std < 0.00003)[0]

# Extract all corresponding y values
flat_y_values = df.iloc[flat_part_indices, 1]

# Print the corresponding y values
print("Corresponding y values in the flat part:")
print(flat_y_values)
