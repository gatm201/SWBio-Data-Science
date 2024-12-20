# SWBio-Data-Science

Baseline calculation of calcium activity traces

Find the Most Common Signal Value (Baseline Guess): Signals  usually spend a lot of time near the baseline, so the baseline value tends to be the most common (frequent) signal level. To find this, the signal is divided into bins (like creating a bar chart) and how many data points fall into each bin are counted. The bin with the highest count gives us our first guess for the baseline level.
Exclude Peaks: To ensure that the baseline isn’t affected by the large calcium peaks, we detect where the peaks are in the signal and temporarily ignore those regions while calculating the baseline. This avoids overestimating the baseline level.
Refine the Baseline Estimate: Since not all parts of the signal close to the baseline are perfectly steady, we look at points near our baseline guess and calculate their average. This refines the baseline estimate by ignoring outliers or minor deviations.
Handle Changing Baselines: If the baseline value changes over time (e.g., due to experimental drift), we split the signal into smaller time windows and repeat the baseline estimation for each segment. This allows us to calculate a "local" baseline for different parts of the data.
Stitch Together a Continuous Baseline: After estimating the baseline for each segment, we connect these points to form a smooth, continuous baseline for the entire signal. This makes the baseline follow gradual changes instead of being a series of steps.
Plot and export data: The calcium trace, and smoothed data, and estimated baseline is plotted for validation. The data is exported to a CSV file for future use.

The following libraries must be installed prior to running code:
- numpy
- scipy
- matplotlib
- pandas

Example calcium traces to be used in this data set can be found in the data.csv file.

