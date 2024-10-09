import pandas as pd

# Load the CSV file
file_path = 'insert path to scraped_wordcount_sentiment_theme_articles.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Keep only the 'sentiment' and 'Date of Publishing' columns
data = data[['sentiment', 'Date of Publishing']]

# Convert 'Date of Publishing' to datetime with UTC handling and extract the year
data['Date of Publishing'] = pd.to_datetime(data['Date of Publishing'], utc=True).dt.year

# Rename 'Date of Publishing' to 'year'
data.rename(columns={'Date of Publishing': 'year'}, inplace=True)

# Save the cleaned data to a new CSV file
output_file_path = 'cleaned_data_for_regr.csv'  # Specify your output file path
data.to_csv(output_file_path, index=False)

print("Data cleaned and saved to", output_file_path)

