import csv
import datetime
import chardet
import re
from textblob import TextBlob
import time
# Define the possible sentiment values
SENTIMENT_POSITIVE = 'positive'
SENTIMENT_NEGATIVE = 'negative'
SENTIMENT_NEUTRAL = 'neutral'

# Define a function to get the sentiment of a text blob
def get_sentiment(text):
    # Use TextBlob to get the polarity of the text (between -1 and 1)
    sentiment_value = 0
    sentences = TextBlob(text).sentences
    for sentence in sentences:
        polarity = sentence.sentiment.polarity

        # Determine the sentiment based on the polarity
        if polarity > 0:
            sentiment_value += 1
        elif polarity < 0:
            sentiment_value -= 1

    if sentiment_value > 0:
        return SENTIMENT_POSITIVE
    elif sentiment_value < 0:
        return SENTIMENT_NEGATIVE
    else:
        return SENTIMENT_NEUTRAL

# Define a function to parse a date string into a datetime object
def parse_date(date_str):
    # Use regular expressions to extract the date string
    match = re.search(r'on (\w+ \d+, \d+)', date_str)
    if match:
        date_str = match.group(1)

    # Convert the date string to a datetime object
    return datetime.datetime.strptime(date_str, '%B %d, %Y')

# Define a function to analyze a CSV file and return sentiment counts by month
def analyze_reviews_csv(filename):
    # Try opening the file with different encodings until we find one that works
    encodings = ['utf-8', 'utf-16', 'cp1252']
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                # Initialize a dictionary to hold the sentiment counts by month
                sentiment_counts = {}
                # Initialize total counts
                total_counts = {SENTIMENT_POSITIVE: 0, SENTIMENT_NEGATIVE: 0, SENTIMENT_NEUTRAL: 0}

                # Loop over each row in the CSV file
                for row in reader:
                    # Parse the date from the "Time" column
                    date = parse_date(row['date'])

                    # Get the sentiment of the "Body" column
                    body = row['customer_review'].strip()
                    if not body:
                        continue  # Skip rows where the "Body" column is empty or contains only whitespace
                    sentiment = get_sentiment(body)

                    # Only include sentiments from the last year
                    now = datetime.datetime.now()
                    one_year_ago = now - datetime.timedelta(days=365)
                    if date >= one_year_ago:
                        # Increment the sentiment count for this month
                        month = date.strftime('%Y-%m')
                        if month not in sentiment_counts:
                            sentiment_counts[month] = {SENTIMENT_POSITIVE: 0, SENTIMENT_NEGATIVE: 0, SENTIMENT_NEUTRAL: 0}
                        sentiment_counts[month][sentiment] += 1

                    # Increment the total count
                    total_counts[sentiment] += 1

                # Add the total counts to the sentiment counts
                sentiment_counts['total'] = total_counts

                # Return the sentiment counts by month


                return sentiment_counts 
        except UnicodeDecodeError:
            pass

