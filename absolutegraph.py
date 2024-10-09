import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch  # For custom legend handles

# Load the CSV file (update the file path as necessary)
csv_file = 'insert path to cleaned_data_for_regr.csv'
data = pd.read_csv(csv_file)

# Convert 'year' column to datetime and extract the year part
data['year'] = pd.to_datetime(data['year']).dt.year

# Group data by 'year' and 'sentiment', and count the occurrences
yearly_sentiment = data.groupby(['year', 'sentiment']).size().unstack(fill_value=0)

# Select all years from 2011 to 2024 in intervals of 1
years = list(range(2011, 2025))
yearly_sentiment = yearly_sentiment.reindex(years, fill_value=0)

# Define custom colors
colors = ['#FF4C4C', '#FFD700', '#4CAF50']

# Plotting the stacked bar chart with custom colors
fig, ax = plt.subplots(figsize=(10, 6))
yearly_sentiment.plot(kind='bar', stacked=True, ax=ax, color=colors, width=0.9)

# Customizing the axis and graph appearance
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Set spine linewidth
ax.spines['left'].set_linewidth(3)
ax.spines['bottom'].set_linewidth(3)

# Making X and Y axis thick and ensuring they touch
ax.spines['left'].set_position(('outward', -0.5))  # Ensure X and Y axes touch the bars
ax.spines['bottom'].set_position(('outward', -0.5))

# Title for the graph
ax.set_title('Yle Absolute Coverage Of Bitcoin', fontsize=16)
ax.set_xlabel('Year', fontsize=14, labelpad=15)  # Add padding to x-label
ax.set_ylabel('Sentiment Counts', fontsize=14, labelpad=15)  # Updated y-label for absolute counts

# Tight layout for compact style
plt.tight_layout()

# Creating custom legend handles with colored boxes
legend_handles = [
    Patch(facecolor='#FF4C4C', label='negative (red-coloured box)'),
    Patch(facecolor='#FFD700', label='neutral (yellow-coloured box)'),
    Patch(facecolor='#4CAF50', label='positive (green-coloured box)')
]

# Adjust legend to be compact and not clipped
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title='Sentiment', frameon=False)

# Display the chart
plt.show()
