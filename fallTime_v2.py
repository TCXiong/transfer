import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt

# Set the path to the directory containing the CSV files
directory_path = './modified'
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
    # print(data)


    time = data[:, 0] * 1e9  # values in column x (time in ns)

    print("time",time)

    pas_time = time[1] - time[0]  # ns/point
    # print(pas_time)


    intensity = data[:, 1]

    # print(intensity)    # values in column y

    min_intensity = np.min(intensity)

    # Smooth data (pending !!)
    # Smooth_intensity = filtfilt(*butter(4, 0.02), intensity)
    # Smooth data using Gaussian filter
    Smooth_intensity = np.convolve(intensity, np.exp(-np.linspace(-3, 3, N) ** 2), mode='same') / np.sum(np.exp(-np.linspace(-3, 3, N) ** 2))

    # print(Smooth_intensity)

    # Calculate Max_intensity
    Max_intensity = np.max(Smooth_intensity)
    print("max intensity: ", Max_intensity)
    threshold = Max_intensity * Cut_threshold
    print("threshold: ", threshold)

    # Pulse width
    # PW_points = find_peaks(intensity > threshold)[0][[0, -1]]
    # Pulse width
    above_threshold = np.where(intensity > threshold)[0]
    PW_points = [above_threshold[0], above_threshold[-1]]
    print(PW_points)

    # t1, t2 = time[PW_points]
    # print(t1, t2)
    # Y1, Y2 = intensity[PW_points]
    # T1_PW = (threshold * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)
    t1 = time[PW_points[0] - 1]
    t2 = time[PW_points[0]]
    Y1 = intensity[PW_points[0] - 1]
    Y2 = intensity[PW_points[0]]
    T1_PW = (threshold * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)
    print(t1, t2, Y1, Y2, T1_PW)

    # t3, t4 = time[PW_points + 1]
    # Y3, Y4 = intensity[PW_points + 1]
    # T2_PW = (threshold * (t3 - t4) - t3 * Y4 + t4 * Y3) / (Y3 - Y4)
    t3 = time[PW_points[1]]
    t4 = time[PW_points[1] + 1]
    Y3 = intensity[PW_points[1]]
    Y4 = intensity[PW_points[1] + 1]
    T2_PW = (threshold * (t3 - t4) - t3 * Y4 + t4 * Y3) / (Y3 - Y4)
    print(T2_PW)

    PW_ns.append(np.abs(T2_PW - T1_PW))
    print("PW_ns", PW_ns)
    PW_ns_str = "{:.5f}".format(PW_ns[-1])
    print("PW_ns_str", PW_ns_str)

    # Raise time 20-80
    cut1, cut2 = 0.2, 0.8
    # Raise_points = find_peaks(intensity > Max_intensity * cut1)[0][[0, 1]]
    # t1, t2 = time[Raise_points]
    # Y1, Y2 = intensity[Raise_points]
    # T1_Raise = (Max_intensity * cut1 * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)

    Raise_points = [np.where(intensity > Max_intensity * cut1)[0][0], np.where(intensity > Max_intensity * cut2)[0][0]]
    print("Raise_points",Raise_points)
    t1 = time[Raise_points[0] - 1]
    t2 = time[Raise_points[0]]
    Y1 = intensity[Raise_points[0] - 1]
    Y2 = intensity[Raise_points[0]]
    T1_Raise = (Max_intensity * cut1 * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)
    print("T1_Raise", T1_Raise)

    # t3, t4 = time[Raise_points + 1]
    # Y3, Y4 = intensity[Raise_points + 1]
    # T2_Raise = (Max_intensity * cut2 * (t3 - t4) - t3 * Y4 + t4 * Y3) / (Y3 - Y4)
    # Raise_ns.append(np.abs(T2_Raise - T1_Raise))
    # Continue from the previous code snippet...

    t3 = time[Raise_points[1] - 1]
    t4 = time[Raise_points[1]]
    Y3 = intensity[Raise_points[1] - 1]
    Y4 = intensity[Raise_points[1]]
    T2_Raise = (Max_intensity * cut2 * (t3 - t4) - t3 * Y4 + t4 * Y3) / (Y3 - Y4)
    Raise_ns.append(np.abs(T2_Raise - T1_Raise))
    Raise_ns_str = "{:.5f}".format(Raise_ns[-1])
    print("Raise_ns_str:",Raise_ns_str)


    # Fall time 20-80
    # Fall_points = find_peaks(intensity > Max_intensity * cut2)[0][[1, 0]]
    # t1, t2 = time[Fall_points]
    # Y1, Y2 = intensity[Fall_points]
    # T1_Fall = (Max_intensity * cut2 * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)

    # t3, t4 = time[Fall_points + 1]
    # Y3, Y4 = intensity[Fall_points + 1]
    # T2_Fall = (Max_intensity * cut1 * (t3 - t4) - t3 * Y4 + t4 * Y3) / (Y3 - Y4)

    # Fall_ns.append(np.abs(T2_Fall - T1_Fall))
    # Fall time 20-80
    Fall_points = [np.where(intensity > Max_intensity * cut2)[0][-1], np.where(intensity > Max_intensity * cut1)[0][-1]]
    t1 = time[Fall_points[0]]
    t2 = time[Fall_points[0] + 1]
    Y1 = intensity[Fall_points[0]]
    Y2 = intensity[Fall_points[0] + 1]
    T1_Fall = (Max_intensity * cut2 * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)

    t3 = time[Fall_points[1]]
    t4 = time[Fall_points[1] + 1]
    Y3 = intensity[Fall_points[1]]
    Y4 = intensity[Fall_points[1] + 1]
    T2_Fall = (Max_intensity * cut1 * (t3 - t4) - t3 * Y4 + t4 * Y3) / (Y3 - Y4)

    Fall_ns.append(np.abs(T2_Fall - T1_Fall))

    Fall_ns_str = "{:.5f}".format(Fall_ns[-1])
    print("Fall_ns_str", Fall_ns_str)



    # ... (previous code)
    folder_name = 'measurements'
    os.makedirs(folder_name, exist_ok=True)
    # Save measurements into one text file
    file_path = os.path.join(folder_name, f'{filename}_measurements.txt')
    with open(file_path, 'w') as file:
        file.write(f'Fall_ns: {Fall_ns[-1]:.5f}\n')
        file.write(f'Raise_ns: {Raise_ns[-1]:.5f}\n')
        file.write(f'PW_ns: {PW_ns[-1]:.5f}\n')



    # Plot figure
    plt.figure()
    plt.plot(time, intensity)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlim([time[0], time[-1]])
    plt.ylim([min_intensity - 0.005, np.max(intensity) * 1.1])
    plt.title("Placeholder")
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
    # plt.savefig(f'{filename}_PW_{PW_ns[-1]:.5f}ns_Raise_{Raise_ns[-1]:.5f}ns_Fall_{Fall_ns[-1]:.5f}ns.png')
    plot_file_path = os.path.join(folder_name, f'{filename}_PW_{PW_ns[-1]:.5f}ns_Raise_{Raise_ns[-1]:.5f}ns_Fall_{Fall_ns[-1]:.5f}ns.png')
    plt.savefig(plot_file_path)
    plt.show()
    
    # plt.plot(time, intensity)
    # plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    # plt.xlim([time[0], time[-1]])
    # plt.ylim([min_intensity - 0.005, np.max(intensity) * 1.1])
    # plt.title('MZ Jean measurement 1Pulse')
    # plt.xlabel('time (ns)')
    # plt.ylabel('Intensity (V)')
    # plt.plot(T1_Raise, Max_intensity * cut1, 'b*')
    # plt.plot(T2_Raise, Max_intensity * cut2, 'b*')
    # plt.plot(T1_Fall, Max_intensity * cut2, 'r*')
    # plt.plot(T2_Fall, Max_intensity * cut1, 'r*')
    # plt.plot(T1_PW, threshold, 'g*')
    # plt.plot(T2_PW, threshold, 'g*')
    # plt.axvline(x=T1_PW, color='g', linestyle='--')
    # plt.axvline(x=T2_PW, color='g', linestyle='--')
    # plt.legend([f'PW: {PW_ns[-1]:.5f} ns'])
    # plt.title(filename)
    # plt.savefig(f'{filename}_PW_{PW_ns[-1]:.5f}ns_Raise_{Raise_ns[-1]:.5f}ns_Fall_{Fall_ns[-1]:.5f}ns.png')
    # plt.close()

# Display results
print('PW_ns:', PW_ns)
print('Raise_ns:', Raise_ns)
print('Fall_ns:', Fall_ns)
