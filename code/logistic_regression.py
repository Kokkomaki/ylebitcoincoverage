# Required Libraries
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.preprocessing import OrdinalEncoder

# Load the CSV File (Adjust the path if needed)
data = pd.read_csv('cleaned_data_for_regr.csv')

# Check the DataFrame Structure
print("Data Sample:")
print(data.head())

# Encode the Sentiment Column: Set Order [Negative, Neutral, Positive]
encoder = OrdinalEncoder(categories=[['negative', 'neutral', 'positive']])
data['sentiment_encoded'] = encoder.fit_transform(data[['sentiment']])

# Define the Ordinal Logistic Regression Model
model = smf.mnlogit("sentiment_encoded ~ year", data=data)
result = model.fit()

# Display the Results
print("\nModel Summary:")
print(result.summary())
