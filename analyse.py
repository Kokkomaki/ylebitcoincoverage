import pandas as pd
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Load the CSV file containing the article data
input_csv_file = "scraped_articles.csv"
df = pd.read_csv(input_csv_file)

# Ensure required columns exist
required_columns = ['Index Number', 'Title', 'Content', 'Date of Publishing', 'URL']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# Add or initialize 'sentiment' and 'theme' columns
if 'sentiment' not in df.columns:
    df['sentiment'] = ''
if 'theme' not in df.columns:
    df['theme'] = ''

# Function to perform sentiment analysis using OpenAI Chat API
def analyze_sentiment(header, content):
    try:
        prompt = f"Analyze the sentiment of the following article as it relates to bitcoin. The sentiment can be positive, negative, or neutral. Provide only one word as the sentiment.\n\nTitle: {header}\n\nContent: {content}"

        response = client.chat.completions.create(model="gpt-4o-mini",  # Use "gpt-4" or "gpt-4o-mini" depending on your access
        messages=[{"role": "user", "content": prompt}])

        # Check for response validity
        if response.choices:
            return response.choices[0].message.content.strip().lower()  # Return sentiment
        else:
            print(f"No choices returned for sentiment analysis for header: {header}")
            return "error"

    except Exception as e:
        print(f"Error in sentiment analysis for header: {header}. Error: {e}")
        return "error"

# Function to identify the main theme using OpenAI Chat API
def analyze_theme(header, content):
    try:
        prompt = f"Identify the main theme of the following article. The theme cannot be bitcoin. Provide only one english word representing the most appropriate theme.\n\nTitle: {header}\n\nContent: {content}"

        response = client.chat.completions.create(model="gpt-4o-mini",  # Use "gpt-4" or "gpt-4o-mini" depending on your access
        messages=[{"role": "user", "content": prompt}])

        # Check for response validity
        if response.choices:
            return response.choices[0].message.content.strip().lower()  # Return theme
        else:
            print(f"No choices returned for theme analysis for header: {header}")
            return "error"

    except Exception as e:
        print(f"Error in theme analysis for header: {header}. Error: {e}")
        return "error"

# Loop through each article and analyze sentiment and theme
for index, row in df.iterrows():
    header = row['Title']  # Get the article title
    content = row['Content']  # Get the article content

    # Analyze and assign sentiment and theme
    df.at[index, 'sentiment'] = analyze_sentiment(header, content)
    df.at[index, 'theme'] = analyze_theme(header, content)

    # Display the progress
    print(f"Processed article {index + 1}/{len(df)}: Sentiment = {df.at[index, 'sentiment']}, Theme = {df.at[index, 'theme']}")

# Save the updated DataFrame to a new CSV file
output_csv_file = "articles_with_sentiment_and_theme.csv"
df.to_csv(output_csv_file, index=False)
print(f"Analysis complete. Updated data saved to {output_csv_file}.")

