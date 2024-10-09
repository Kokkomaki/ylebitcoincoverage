import pandas as pd

# Load the CSV file
file_path = 'insert path to cleaned_data_for_wordcloud.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Extract only the 'theme' and 'sentiment' columns
extracted_df = df[['theme', 'sentiment']]

# Save the cleaned data to a new CSV file
extracted_df.to_csv('wordcloud.csv', index=False)

print("Successfully extracted 'theme' and 'sentiment' columns to wordcloud.csv")
