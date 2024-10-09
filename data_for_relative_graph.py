import pandas as pd

# Load the CSV file
file_path = 'insert here path to scraped_wordcount_sentiment_theme_articles.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Check the columns in the DataFrame
print("Columns in the DataFrame:", df.columns.tolist())

# Strip any whitespace from column names
df.columns = df.columns.str.strip()

# Check if 'Date of Publishing' and 'sentiment' exist
if 'Date of Publishing' in df.columns and 'sentiment' in df.columns:
    # Keep only the 'sentiment' and 'Date of Publishing' columns
    df = df[['sentiment', 'Date of Publishing']]
    
    # Rename 'Date of Publishing' to 'year'
    df.rename(columns={'Date of Publishing': 'year'}, inplace=True)
    
    # Convert the 'year' column to datetime with UTC and format to 'YYYY-MM'
    df['year'] = pd.to_datetime(df['year'], utc=True).dt.strftime('%Y-%m')
    
    # Save the modified DataFrame to a new CSV file
    output_file_path = 'cleaned_data_for_relative_graph.csv'  # Replace with your desired output file path
    df.to_csv(output_file_path, index=False)
    
    print("DataFrame modified and saved successfully.")
else:
    print("Required columns not found in the DataFrame.")
