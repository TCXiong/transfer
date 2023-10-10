import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt

# Set the path to the directory containing the CSV files
directory_path = './'
files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

# Parameters
Cut_threshold = 1 / 2
N = 300

PW_ns = []
Raise_ns = []
Fall_ns = []

for filename in files:
    # Load data
    data = np.loadtxt(os.path.join(directory_path, filename), delimiter=',')
    time = data[:, 0] * 1e9  # time in ns

    intensity = data[:, 1]
    min_intensity = np.min(intensity)

    # Smooth data
    Smooth_intensity = filtfilt(*butter(4, 0.02), intensity)

    # Calculate Max_intensity
    Max_intensity = np.max(Smooth_intensity)
    threshold = Max_intensity * Cut_threshold

    # Pulse width
    peaks, _ = find_peaks(intensity > threshold)

    if len(peaks) < 2:
        print(f"Skipping {filename}: Not enough peaks found.")
        continue

    PW_points = peaks[[0, -1]]
    t1, t2 = time[PW_points]
    Y1, Y2 = intensity[PW_points]
    T1_PW = (threshold * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)

    t3, t4 = time[peaks[1:]+1]
    Y3, Y4 = intensity[peaks[1:]+1]
    T2_PW = (threshold * (t3 - t4) - t3 * Y4 + t4 * Y3) / (Y3 - Y4)

    PW_ns.append(np.abs(T2_PW - T1_PW))

    # Raise time 20-80
    cut1, cut2 = 0.2, 0.8
    Raise_points = find_peaks(intensity > Max_intensity * cut1)[0][:2]

    if len(Raise_points) < 2:
        print(f"Skipping {filename}: Not enough raise points found.")
        continue

    t1, t2 = time[Raise_points]
    Y1, Y2 = intensity[Raise_points]
    T1_Raise = (Max_intensity * cut1 * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)

    t3, t4 = time[Raise_points[1:]+1]
    Y3, Y4 = intensity[Raise_points[1:]+1]
    T2_Raise = (Max_intensity * cut2 * (t3 - t4) - t3 * Y4 + t4 * Y3) / (Y3 - Y4)

    Raise_ns.append(np.abs(T2_Raise - T1_Raise))

    # Fall time 20-80
    Fall_points = find_peaks(intensity > Max_intensity * cut2)[0][-2:]

    if len(Fall_points) < 2:
        print(f"Skipping {filename}: Not enough fall points found.")
        continue

    t1, t2 = time[Fall_points]
    Y1, Y2 = intensity[Fall_points]
    T1_Fall = (Max_intensity * cut2 * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)

    t3, t4 = time[Fall_points[1:]+1]
    Y3, Y4 = intensity[Fall_points[1:]+1]
    T2_Fall = (Max_intensity * cut1 * (t3 - t4) - t3 * Y4 + t4 * Y3) / (Y3 - Y4)

    Fall_ns.append(np.abs(T2_Fall - T1_Fall))

    # Plot figure
    plt.plot(time, intensity)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlim([time[0], time[-1]])
    plt.ylim([min_intensity - 0.005, np.max(intensity) * 1.1])
    plt.title('MZ Jean measurement 1Pulse')
    plt.xlabel('time (ns)')
    plt.ylabel('Intensity (V)')
    plt.plot(T1_Raise, Max_intensity * cut1, 'b*')
    plt.plot(T2_Raise, Max_intensity * cut2, 'b*')
    plt.plot(T1_Fall, Max_intensity * cut2, 'r*')
    plt.plot(T2_Fall, Max_intensity * cut1, 'r*')
    plt.plot(T1_PW, threshold, 'g*')
    plt.plot(T2_PW, threshold, 'g*')
    plt.axvline(x=T1_PW, color='g', linestyle='--')
    plt.axvline(x=T2_PW, color='g', linestyle='--')
    plt.legend([f'PW: {PW_ns[-1]:.5f} ns'])
    plt.title(filename)
    plt.savefig(f'{filename}_PW_{PW_ns[-1]:.5f}ns_Raise_{Raise_ns[-1]:.5f}ns_Fall_{Fall_ns[-1]:.5f}ns.png')
    plt.close()

# Display results
print('PW_ns:', PW_ns)
print('Raise_ns:', Raise_ns)
print('Fall_ns:', Fall_ns)
