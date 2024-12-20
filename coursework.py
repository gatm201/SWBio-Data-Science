# Import all the relevant libraries for this project
import numpy as np
from scipy.signal import find_peaks
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
import pandas as pd

# Import the data you are going to find the baseline for
data = pd.read_csv('data.csv')
num_columns = data.shape[1]

# Initialise a dictionary to store the results in
baseline_results = {}

for col in data.columns[3:]:
    test_data = data[col].to_numpy()

    # Mask the peaks in the data
    peaks, _ = find_peaks(test_data, prominence = 0.05) # Adjust prominence as needed
    mask = np.ones(len(test_data), dtype=bool)
    mask[peaks] = False
    baseline_data = test_data[mask]

    # Smooth the singal
    smooth_signal = uniform_filter1d(baseline_data, size = 5) # Adjust the window size as needed

    # Calculate histogram and find the baseline value
    counts, edges = np.histogram(smooth_signal, bins = 'fd') # Bin size optimized
    max_idx = np.argmax(counts) # Find the bin with the highest count
    baseline_value = (edges[max_idx] + edges[max_idx + 1])/2

    # Segment the signal around the baseline
    threshold = 0.1 * baseline_value # Change threshold as desired, +/- 10% chosen
    baseline_points = smooth_signal[np.abs(smooth_signal - baseline_value) < threshold]
    refined_baseline = np.mean(baseline_points)

    # Handle baseline drift
    segment_size = len(test_data) // 2 # Adjust segment size as needed
    num_segments = int(np.ceil(len(test_data) / segment_size))
    baseline_per_segment = []

    for i in range(num_segments):
        segment = test_data[i*segment_size : min((i+1) * segment_size, len(test_data))]
        smooth_segment = uniform_filter1d(segment, size=5)
        counts,edges = np.histogram(smooth_segment, bins='fd')
        max_idx = np.argmax(counts)
        segment_baseline = (edges[max_idx] + edges[max_idx + 1]) / 2
        baseline_per_segment.append(segment_baseline)

    # Interpolate between segments to get a continuous baseline estimate
    test_time = np.arange(len(test_data))
    segment_times = np.linspace(0, len(test_data), num_segments)
    interp_func = interp1d(segment_times, baseline_per_segment, kind = 'linear', fill_value='extrapolate')
    baseline_continuous = interp_func(test_time)
    
    # Store the baseline data
    baseline_results[col] = baseline_continuous

    # Plot the results
    plt.figure()
    plt.plot(test_data, label = 'Raw Data')
    plt.plot(smooth_signal, 'r', label = 'Smoothed Signal')
    plt.plot(baseline_continuous, 'k--', linewidth = 1.5, label = 'Estimated Baseline')
    plt.legend()
    plt.show()
    
baseline_df = pd.DataFrame(baseline_results)
baseline_df.to_csv('baseline_results.csv', index = False)