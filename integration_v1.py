import pandas as pd
from scipy.integrate import trapz
import matplotlib.pyplot as plt
import numpy as np

# Load your data from the file
# Assuming your data file is a CSV file without column names
data = pd.read_csv('test_integration.csv', header=None, names=['column1', 'column2'])

# Extract 'x' and 'y' values from the DataFrame
x = data['column1'].values
y = data['column2'].values

# Plot the curve
plt.plot(x, y, label='Curve')
plt.title('Select two points to integrate the area between them')

# Allow the user to select two points on the plot
selected_points = plt.ginput(2, timeout=-1, show_clicks=True)
plt.close()

# Extract x-coordinates of selected points
x1, x2 = [point[0] for point in selected_points]

# Find the index of the closest point in the data to the selected x-values
index_x1 = np.argmin(np.abs(x - x1))
index_x2 = np.argmin(np.abs(x - x2))

# Extract the corresponding y-values for the closest x-values
y1 = y[index_x1]
y2 = y[index_x2]

# Create a mask for the selected region
selected_region = (x >= x1) & (x <= x2)

# Integrate the area between the selected points
integrated_area = trapz(y[selected_region], x[selected_region])


print('Integrated Area between {} and {} is {}'.format(x1, x2, integrated_area))


# Plot the selected area
plt.plot(x, y, label='Curve')
plt.fill_between(x[selected_region], y[selected_region], color='yellow', alpha=0.3, label='Selected Area')
plt.scatter([x1, x2], [y1, y2], color='red', marker='o', label='Selected Points')
plt.legend()
plt.title('Integrated Area between {} and {}'.format(x1, x2))
plt.show()

# Print the integrated area
