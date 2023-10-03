import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
file_path = 'your_file.csv'  # Replace with the actual file path
df = pd.read_csv(file_path, header=None)

# Find the index where the y values are relatively flat
flat_part_index = np.where(np.gradient(df.iloc[:, 1].values) < 0.001)[0]

# Find the average y value in the flat part
average_y = np.mean(df.iloc[flat_part_index, 1])

# Find the corresponding x value (or the closest x if not exact)
closest_x_index = np.argmin(np.abs(df.iloc[:, 1].values - average_y))
closest_x = df.iloc[closest_x_index, 0]

# Print the results
print(f"Average y value in the flat part: {average_y}")
print(f"Corresponding x value (or closest x): {closest_x}")
