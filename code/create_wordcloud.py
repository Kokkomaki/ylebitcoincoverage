import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Define a color function for word cloud based on sentiment
def sentiment_color_func(theme, sentiment_dict):
    sentiment_colors = {
        'positive': '#4CAF51',
        'negative': '#FE4D4E',
        'neutral': '#FDD703'
    }
    sentiment = sentiment_dict.get(theme, 'neutral')
    return sentiment_colors.get(sentiment, '#FDD703')

# Function to generate the word cloud based on theme frequency and sentiment colors
def create_sentiment_wordcloud(csv_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Ensure the columns 'sentiment' and 'theme' exist in the CSV
    if 'sentiment' not in df.columns or 'theme' not in df.columns:
        raise ValueError("The CSV file must contain 'sentiment' and 'theme' columns.")
    
    # Create a dictionary of theme counts and corresponding sentiments
    theme_counts = df['theme'].value_counts().to_dict()
    theme_sentiments = df.set_index('theme')['sentiment'].to_dict()
    
    # Create the word cloud object with increased resolution
    wc = WordCloud(width=1600, height=800, background_color='white',
                   prefer_horizontal=1.0, color_func=lambda *args, **kwargs: sentiment_color_func(args[0], theme_sentiments))

    # Generate word cloud with the frequency of themes
    wc.generate_from_frequencies(theme_counts)

    # Display the word cloud without a title
    plt.figure(figsize=(20, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Usage
# Provide the path to your CSV file
csv_file_path = "insert path to wordcloud.csv"
create_sentiment_wordcloud(csv_file_path)
