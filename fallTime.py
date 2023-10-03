import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.interpolate import interp1d

# Set the path to the directory containing CSV files
data_path = '/path/to/your/data/directory'

# Get a list of CSV files in the directory
files = [f for f in os.listdir(data_path) if f.endswith('.csv')]

# Parameters
cut_threshold = 1/2
N = 300

PW_ns = []
Raise_ns = []
Fall_ns = []

for file in files:
    # Load data
    data = pd.read_csv(os.path.join(data_path, file))
    time = data.iloc[:, 0] * 1e9  # time in ns
    pas_time = time.iloc[1] - time.iloc[0]  # ns/point

    intensity = data.iloc[:, 1]
    min_intensity = np.min(intensity)

    # Smooth data
    smooth_intensity = np.convolve(intensity, np.ones(N)/N, mode='same')

    # Pulse width calculation
    max_intensity = np.max(smooth_intensity)
    threshold = max_intensity * cut_threshold

    pw_points = find_peaks(intensity > threshold)[0][:2]
    interp_func = interp1d(time.iloc[pw_points - 1], intensity.iloc[pw_points - 1], kind='linear')
    T1_PW = interp_func.inverse(threshold)

    pw_points = find_peaks(intensity > threshold)[0][1:]
    interp_func = interp1d(time.iloc[pw_points], intensity.iloc[pw_points], kind='linear')
    T2_PW = interp_func.inverse(threshold)

    pw_ns = np.abs(T2_PW - T1_PW)
    PW_ns.append(pw_ns)

    # Raise time 20-80
    cut1 = 0.2
    cut2 = 0.8

    raise_points = find_peaks(intensity > max_intensity * cut1)[0][:2]
    interp_func = interp1d(time.iloc[raise_points - 1], intensity.iloc[raise_points - 1], kind='linear')
    T1_Raise = interp_func.inverse(max_intensity * cut1)

    raise_points = find_peaks(intensity > max_intensity * cut2)[0][:2]
    interp_func = interp1d(time.iloc[raise_points - 1], intensity.iloc[raise_points - 1], kind='linear')
    T2_Raise = interp_func.inverse(max_intensity * cut2)

    raise_ns = np.abs(T2_Raise - T1_Raise)
    Raise_ns.append(raise_ns)

    # Fall time 20-80
    fall_points = find_peaks(intensity > max_intensity * cut2)[0][-2:]
    interp_func = interp1d(time.iloc[fall_points], intensity.iloc[fall_points], kind='linear')
    T1_Fall = interp_func.inverse(max_intensity * cut2)

    fall_points = find_peaks(intensity > max_intensity * cut1)[0][-2:]
    interp_func = interp1d(time.iloc[fall_points], intensity.iloc[fall_points], kind='linear')
    T2_Fall = interp_func.inverse(max_intensity * cut1)

    fall_ns = np.abs(T2_Fall - T1_Fall)
    Fall_ns.append(fall_ns)

    # Plot the figure with the points of the different cuts
    plt.figure()
    plt.plot(time, intensity)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlim([time.iloc[0], time.iloc[-1]])
    plt.ylim([min_intensity - 0.005, max_intensity * 1.1])
    plt.title(file)
    plt.xlabel('time (ns)')
    plt.ylabel('Intensity (V)')
    plt.plot(T1_Raise, max_intensity * cut1, 'b*')
    plt.plot(T2_Raise, max_intensity * cut2, 'b*')
    plt.plot(T1_Fall, max_intensity * cut2, 'r*')
    plt.plot(T2_Fall, max_intensity * cut1, 'r*')
    plt.plot(T1_PW, threshold, 'g*')
    plt.plot(T2_PW, threshold, 'g*')
    plt.axvline(T1_PW, color='g')
    plt.axvline(T2_PW, color='g')
    plt.legend([f'PW: {pw_ns:.5f} ns'])
    plt.title(file)

    plt.savefig(os.path.join(data_path, f"{file}_PW_{pw_ns:.5f}ns_Raise_{raise_ns:.5f}ns_Fall_{fall_ns:.5f}ns.png"))

# Display results
print("Pulse Widths:", PW_ns)
print("Raise Times:", Raise_ns)
print("Fall Times:", Fall_ns)
