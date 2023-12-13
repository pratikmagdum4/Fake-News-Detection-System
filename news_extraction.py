import requests
from bs4 import BeautifulSoup
import csv

def extract_headlines_from_page(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract headlines from anchor (<a>) tags
        anchor_tags = soup.find_all('a')
        headlines_from_anchor = [anchor.text.strip() for anchor in anchor_tags if anchor.text.strip()]

        # Extract headlines from figcaption tags
        figcaption_tags = soup.find_all('figcaption')
        headlines_from_figcaption = [figcaption.text.strip() for figcaption in figcaption_tags if figcaption.text.strip()]

        # Extract headlines from span tags
        span_tags = soup.find_all('span')
        headlines_from_span = [span.text.strip() for span in span_tags if span.text.strip()]

        # Combine headlines from all sources
        all_headlines = headlines_from_anchor + headlines_from_figcaption + headlines_from_span

        return all_headlines

    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return []

def save_headlines_to_csv(headlines, filename='news_headlines_combined.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline'])  # Write the header row

        # Write each headline to the CSV file if it has more than 3 words
        for headline in headlines:
            words = headline.split()
            if len(words) > 3:
                writer.writerow([headline])

    print(f"Collected and saved headlines with more than 3 words to '{filename}'.")

if __name__ == "__main__":
    news_source_url = "https://timesofindia.indiatimes.com/home/headlines"  # Replace with the actual URL
    all_headlines = extract_headlines_from_page(news_source_url)
    save_headlines_to_csv(all_headlines, filename='news_headlines_combined.csv')
