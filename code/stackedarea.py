import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
from matplotlib.ticker import PercentFormatter

# Load the CSV data
data = pd.read_csv('file path to cleaned_data_for_relative_graph.csv')

# Convert 'year' column to datetime
data['year'] = pd.to_datetime(data['year'])

# Extract year and month for better aggregation
data['year_month'] = data['year'].dt.to_period('M')

# Pivot the data to get the sentiment counts
pivot_data = data.pivot_table(index='year_month', columns='sentiment', aggfunc='size', fill_value=0)

# Convert PeriodIndex to DatetimeIndex for resampling
pivot_data.index = pivot_data.index.to_timestamp()

# Resample to monthly frequency to ensure smoothness
pivot_data = pivot_data.resample('M').sum()

# Calculate the relative values (proportions)
relative_data = pivot_data.div(pivot_data.sum(axis=1), axis=0)

# Initialize parameters
window_size = 9  # Set window size to 9
use_gaussian = True  # Enable Gaussian filter
sigma = 2.0  # Set Gaussian filter to 2.0

# Function to update the plot based on the current parameters
def update_plot():
    global window_size, use_gaussian, sigma

    # Apply a moving average to smooth the data
    smooth_data = relative_data.rolling(window=window_size, min_periods=1).mean()

    # Apply Gaussian filter for additional smoothing if selected
    if use_gaussian:
        smooth_data['negative'] = gaussian_filter1d(smooth_data['negative'], sigma=sigma)
        smooth_data['neutral'] = gaussian_filter1d(smooth_data['neutral'], sigma=sigma)
        smooth_data['positive'] = gaussian_filter1d(smooth_data['positive'], sigma=sigma)

    # Create a smooth curve for the stacked area
    smooth_dates = pd.date_range(start=smooth_data.index.min(), end=smooth_data.index.max(), freq='M')
    smoothed_data = smooth_data.reindex(smooth_dates).interpolate(method='linear')

    # Clear the current plot
    ax.cla()

    # Plot the smoothed data
    ax.stackplot(smoothed_data.index, 
                  smoothed_data['negative'], 
                  smoothed_data['neutral'], 
                  smoothed_data['positive'], 
                  labels=smoothed_data.columns,
                  colors=['#FF4C4C', '#FFD700', '#4CAF50'])  # Example colors for sentiments

    # Set the x-ticks to show every two years
    ax.set_xticks(pd.date_range(start='2011-01-01', end='2024-12-31', freq='2Y'))
    ax.set_xticklabels(pd.date_range(start='2011-01-01', end='2024-12-31', freq='2Y').year)

    # Set x-axis limits to start from 2011 with no extra space
    ax.set_xlim([smooth_data.index.min(), smooth_data.index.max()])  # Adjust to your data range

    # Customize y-axis to show percentages
    ax.yaxis.set_major_formatter(PercentFormatter(1))  # Use PercentFormatter to convert 0-1 to 0%-100%

    # Customize axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Set spine colors to dark grey
    dark_grey = '#242424'
    ax.spines['left'].set_color(dark_grey)  
    ax.spines['bottom'].set_color(dark_grey)  
    
    # Set spine linewidth
    ax.spines['left'].set_linewidth(3)
    ax.spines['bottom'].set_linewidth(3)

    # Increase the distance of the labels from the ticks
    ax.xaxis.set_tick_params(pad=10)  # Add padding to x-axis labels
    ax.yaxis.set_tick_params(pad=10)  # Add padding to y-axis labels

    # Title and Labels
    ax.set_title('Yle Relative Coverage Of Bitcoin', fontsize=16)
    ax.set_xlabel('Year', fontsize=14, labelpad=15)  # Add padding to x-label
    ax.set_ylabel('Sentiment Amounts (%)', fontsize=14, labelpad=15)  # Add padding to y-label

    # Adjust legend to be compact and symmetrical on the right side
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title='Sentiment', frameon=False)

    # Adjust layout to avoid clipping
    plt.tight_layout()
    plt.draw()  # Redraw the updated figure

# Create a figure for the plot
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.15)  # Adjust bottom to make space for potential future additions

# Initial plot
update_plot()

# Show the plot
plt.show()
