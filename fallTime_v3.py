import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt
from tkinter import Tk, filedialog, Label, Listbox, Button, Text, Scrollbar
import tkinter as tk


# Global variable to store selected file paths
selected_files = []
# Parameters
Cut_threshold = 1 / 2
N = 300

PW_ns = []
Raise_ns = []
Fall_ns = []

def browse_button():
    # Function to handle the Browse button click event
    global selected_files
    files = filedialog.askopenfilenames(initialdir="./", title="Select CSV files", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
    selected_files.extend(files)
    
    # Display selected files in the listbox
    listbox.delete(0, 'end')
    for file_path in selected_files:
        listbox.insert('end', os.path.basename(file_path))
    print("Selected files:", selected_files)

def process_files():
    # Function to process the selected CSV files and generate subplots
    for file_path in selected_files:
        filename = os.path.basename(file_path)
        print(filename)
        data = np.loadtxt(os.path.join('./modified', filename), delimiter=',')
        print(data)

        # Rest of your code for processing the CSV file, similar to the original code...

        time = data[:, 0] * 1e9  # values in column x (time in ns)
        pas_time = time[1] - time[0]  # ns/point

        intensity = data[:, 1]
        min_intensity = np.min(intensity)

        # Smooth data (pending !!)
        Smooth_intensity = np.convolve(intensity, np.exp(-np.linspace(-3, 3, N) ** 2), mode='same') / np.sum(np.exp(-np.linspace(-3, 3, N) ** 2))

        # Calculate Max_intensity
        Max_intensity = np.max(Smooth_intensity)
        print("max intensity: ", Max_intensity)
        threshold = Max_intensity * Cut_threshold
        print("threshold: ", threshold)

        # Pulse width
        above_threshold = np.where(intensity > threshold)[0]
        PW_points = [above_threshold[0], above_threshold[-1]]
        print(PW_points)

        t1 = time[PW_points[0] - 1]
        t2 = time[PW_points[0]]
        Y1 = intensity[PW_points[0] - 1]
        Y2 = intensity[PW_points[0]]
        T1_PW = (threshold * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)
        print(t1, t2, Y1, Y2, T1_PW)

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
        Raise_points = [np.where(intensity > Max_intensity * cut1)[0][0], np.where(intensity > Max_intensity * cut2)[0][0]]
        print("Raise_points",Raise_points)
        t1 = time[Raise_points[0] - 1]
        t2 = time[Raise_points[0]]
        Y1 = intensity[Raise_points[0] - 1]
        Y2 = intensity[Raise_points[0]]
        T1_Raise = (Max_intensity * cut1 * (t1 - t2) - t1 * Y2 + t2 * Y1) / (Y1 - Y2)
        print("T1_Raise", T1_Raise)

        t3 = time[Raise_points[1] - 1]
        t4 = time[Raise_points[1]]
        Y3 = intensity[Raise_points[1] - 1]
        Y4 = intensity[Raise_points[1]]
        T2_Raise = (Max_intensity * cut2 * (t3 - t4) - t3 * Y4 + t4 * Y3) / (Y3 - Y4)
        Raise_ns.append(np.abs(T2_Raise - T1_Raise))
        Raise_ns_str = "{:.5f}".format(Raise_ns[-1])
        print("Raise_ns_str:",Raise_ns_str)


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


        # Plot subplot
        # plt.plot(time, intensity, label=filename)
        plt.plot(time, intensity, label=f'{filename}')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        # plt.xlim([time[0], time[-1]])
        # plt.ylim([min_intensity - 0.005, np.max(intensity) * 1.1])
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
        
 
        # plt.legend([f'{filename}'])


    # Customize plot
    # plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    # # plt.xlim([time[0], time[-1]])
    # # plt.ylim([min_intensity - 0.005, np.max(intensity) * 1.1])
    # plt.title("Combined Subplots")
    # plt.xlabel('time (ns)')
    # plt.ylabel('Intensity (V)')
    # plt.legend()
    plt.legend()
    plt.show()

    # Clear selected files after processing
    selected_files.clear()
    
    # Clear the listbox
    listbox.delete(0, 'end')
    print("Selected files cleared.")

# Create the main GUI window
root = Tk()
root.title("Fall Time Calculation")
root.geometry("600x600") 



# Text widget to display instructions
instructions_text = """Instructions:
1. Click the 'Browse' button to select CSV files.
2. Selected files will be displayed in the list.
3. Click 'Process Files' to generate plots.
4. Legends will be added for each curve.
5. Close the plot window after viewing.
6. Usually select two csv files and process them.
"""

text_widget = Text(root, height=8, width=60, state="normal")
text_widget.insert('1.0', instructions_text)
text_widget.config(state="disabled")  # Make the text widget non-editable
text_widget.pack(pady=10)

# Scrollbar for the text widget
scrollbar = Scrollbar(root, command=text_widget.yview)
scrollbar.pack(side='right', fill='y')
text_widget['yscrollcommand'] = scrollbar.set


# Browse button
browse_button = Button(root, text="Browse", command=browse_button)
browse_button.pack(pady=20)

# Listbox to display selected files
listbox_label = Label(root, text="Selected Files:")
listbox_label.pack(pady=10)
# listbox = Listbox(root)
# listbox.pack(pady=10)


max_filename_length = max(len(os.path.basename(file_path)) for file_path in selected_files) if selected_files else 40

listbox = Listbox(root, width=max_filename_length)
listbox.pack(pady=10)


# Process button
process_button = Button(root, text="Process Files", command=process_files)
process_button.pack(pady=20)

# Start the GUI main loop
root.mainloop()