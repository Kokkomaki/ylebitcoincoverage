import pandas as pd
import re

# Load the CSV file containing the article data
input_csv_file = "articles_with_sentiment_and_theme.csv"
df = pd.read_csv(input_csv_file)

# Ensure required columns exist
required_columns = ['Index Number', 'Title', 'Content', 'Date of Publishing', 'URL', 'sentiment', 'theme']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# Define a function to count wildcard word occurrences using regular expressions
def count_word_occurrences(text, patterns):
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, flags=re.IGNORECASE))
    return count

# Define the search patterns for each word category (including wildcards and varying cases)
patterns_bitcoin = [r'\bbitcoin\w*', r'\bBitcoin\w*']
patterns_virtuaalivaluutta = [r'\bvirtuaalivaluut\w*']
patterns_kryptovaluutta = [r'\bkryptovaluut\w*']

# Add or initialize columns to count each word group if they do not exist
if 'bitcoin' not in df.columns:
    df['bitcoin'] = 0  # Initialize with 0
if 'virtuaalivaluutta' not in df.columns:
    df['virtuaalivaluutta'] = 0
if 'kryptovaluutta' not in df.columns:
    df['kryptovaluutta'] = 0

# Loop through each article and count occurrences of each word group
for index, row in df.iterrows():
    # Combine Title and Content to perform a holistic count
    combined_text = str(row['Title']) + " " + str(row['Content'])
    
    # Count occurrences of each word group
    df.at[index, 'bitcoin'] = count_word_occurrences(combined_text, patterns_bitcoin)
    df.at[index, 'virtuaalivaluutta'] = count_word_occurrences(combined_text, patterns_virtuaalivaluutta)
    df.at[index, 'kryptovaluutta'] = count_word_occurrences(combined_text, patterns_kryptovaluutta)

    # Display the progress
    print(f"Processed article {index + 1}/{len(df)}: Bitcoin = {df.at[index, 'bitcoin']}, Virtuaalivaluutta = {df.at[index, 'virtuaalivaluutta']}, Kryptovaluutta = {df.at[index, 'kryptovaluutta']}")

# Save the updated DataFrame to a new CSV file
output_csv_file = "scraped_wordcount_sentiment_theme_articles.csv"
df.to_csv(output_csv_file, index=False)
print(f"Analysis complete. Updated data saved to {output_csv_file}.")

