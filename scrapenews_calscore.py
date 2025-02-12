import pandas as pd
from bs4 import BeautifulSoup
import requests


def get_news():
    ticker = input("Please input the stock abbreviation: ")
    n = input("Please input the number of pages of news you wish to scrape: ")
    url = f"https://markets.businessinsider.com/news/{ticker}-stock"
    response = requests.get(url)
    webcontent = response.text
    soup = BeautifulSoup(webcontent, 'lxml')

    columns = ['datetime', 'title', 'source', 'link', 'top_sentiment', 'sentiment_score']
    df = pd.DataFrame(columns=columns)

    # should i make it global?
    sentiment_dict = {
        'strong_positive': {
            'soars': 2, 'jumps': 2, 'surge': 2, 'rallies': 2, 'skyrockets': 2,
            'outperform': 2, 'beats': 2, 'exceeds': 2,
            'strong buy': 2, 'upgrade': 2, 'bullish': 2, 'overweight': 2,
            'breakthrough': 2, 'wins': 2, 'major contract': 2, 'acquisition': 2,
            'patent win': 2, 'settlement win': 2, 'record high': 2
        },
        'positive': {
            'gains': 1, 'rises': 1, 'climbs': 1, 'higher': 1, 'up': 1,
            'launches': 1, 'expands': 1, 'partnership': 1, 'collaboration': 1,
            'investment': 1, 'growth': 1, 'new product': 1,
            'optimistic': 1, 'positive': 1, 'momentum': 1, 'opportunity': 1,
            'confident': 1, 'boost': 1
        },
        'strong_negative': {
            'plunges': -2, 'crashes': -2, 'tumbles': -2, 'plummets': -2,
            'downgrade': -2, 'sell rating': -2, 'strong sell': -2,
            'lawsuit': -2, 'investigation': -2, 'probe': -2, 'warning': -2,
            'cuts forecast': -2, 'missed estimates': -2, 'bankruptcy': -2
        },
        'negative': {
            'falls': -1, 'drops': -1, 'declines': -1, 'slips': -1, 'lower': -1,
            'weak': -1, 'concerns': -1, 'risk': -1, 'volatile': -1,
            'competition': -1, 'pressure': -1, 'challenging': -1,
            'cautious': -1, 'uncertainty': -1, 'bearish': -1
        },
        'neutral': {
            'holds': 0, 'steady': 0, 'stable': 0, 'unchanged': 0, 'flat': 0,
            'maintains': 0, 'reiterates': 0, 'neutral': 0, 'hold rating': 0,
            'announces': 0, 'plans': 0, 'considers': 0, 'reports': 0
        }
    }

    all_news = soup.find_all('div', class_='latest-news__story')

    rows = []
    count = 0
    for page in range(1, int(n) + 1):
        for news in all_news:
            datetime = news.find('time', class_='latest-news__date').get('datetime')
            title = news.find('a', class_='news-link').text
            source = news.find('span', class_='latest-news__source').text
            link = news.find('a', class_='news-link').get('href')

            title_lower = title.lower()
            found_keywords = []
            sentiment_score = 0

            for sentiment_category, keywords in sentiment_dict.items():
                for keyword, score in keywords.items():
                    if keyword.lower() in title_lower:
                        found_keywords.append(keyword)
                        sentiment_score += score

            top_sentiment = ', '.join(found_keywords) if found_keywords else 'neutral'

            new_row = {
                'datetime': datetime,
                'title': title,
                'source': source,
                'link': link,
                'top_sentiment': top_sentiment,
                'sentiment_score': sentiment_score
            }

            rows.append(new_row)
            count += 1

        print(f'{count} articles scraped from page {page} for {ticker}.')

    df = pd.DataFrame(rows)
    df.reset_index(drop=True, inplace=True)
    print(df)
    df.to_csv(f"{ticker}_news.csv", index=False)
    return df


def cal_score(ticker):
    try:
        df = pd.read_csv(f"{ticker}_news.csv")
    except FileNotFoundError:
        return f"Error: No news data found for {ticker}. Please run get_news() first."

    sentiment_dict = {
        'strong_positive': {
            'soars': 2, 'jumps': 2, 'surge': 2, 'rallies': 2, 'skyrockets': 2,
            'outperform': 2, 'beats': 2, 'exceeds': 2,
            'strong buy': 2, 'upgrade': 2, 'bullish': 2, 'overweight': 2,
            'breakthrough': 2, 'wins': 2, 'major contract': 2, 'acquisition': 2,
            'patent win': 2, 'settlement win': 2, 'record high': 2
        },
        'positive': {
            'gains': 1, 'rises': 1, 'climbs': 1, 'higher': 1, 'up': 1,
            'launches': 1, 'expands': 1, 'partnership': 1, 'collaboration': 1,
            'investment': 1, 'growth': 1, 'new product': 1,
            'optimistic': 1, 'positive': 1, 'momentum': 1, 'opportunity': 1,
            'confident': 1, 'boost': 1
        },
        'strong_negative': {
            'plunges': -2, 'crashes': -2, 'tumbles': -2, 'plummets': -2,
            'downgrade': -2, 'sell rating': -2, 'strong sell': -2,
            'lawsuit': -2, 'investigation': -2, 'probe': -2, 'warning': -2,
            'cuts forecast': -2, 'missed estimates': -2, 'bankruptcy': -2
        },
        'negative': {
            'falls': -1, 'drops': -1, 'declines': -1, 'slips': -1, 'lower': -1,
            'weak': -1, 'concerns': -1, 'risk': -1, 'volatile': -1,
            'competition': -1, 'pressure': -1, 'challenging': -1,
            'cautious': -1, 'uncertainty': -1, 'bearish': -1
        },
        'neutral': {
            'holds': 0, 'steady': 0, 'stable': 0, 'unchanged': 0, 'flat': 0,
            'maintains': 0, 'reiterates': 0, 'neutral': 0, 'hold rating': 0,
            'announces': 0, 'plans': 0, 'considers': 0, 'reports': 0
        }
    }

    trend_score = 0
    matched_keywords = []

    for title in df['title']:
        title = str(title).lower()
        for sentiment_category in sentiment_dict:
            for keyword, score in sentiment_dict[sentiment_category].items():
                if keyword in title:
                    trend_score += score
                    matched_keywords.append((keyword, score, title))

    total_news = len(df)
    total_score = df['sentiment_score'].sum()
    avg_score = total_score / total_news if total_news > 0 else 0

    if avg_score > 1.5:
        sentiment = "Strongly Positive Sentiment"
    elif avg_score > 0.5:
        sentiment = "Positive Sentiment"
    elif avg_score < -1.5:
        sentiment = "Strongly Negative Sentiment"
    elif avg_score < -0.5:
        sentiment = "Negative Sentiment"
    else:
        sentiment = "Neutral Sentiment"

    response = [
        f"\n{'=' * 50}",
        f"SENTIMENT ANALYSIS FOR {ticker.upper()}",
        f"{'=' * 50}",
        f"Number of news articles analyzed: {total_news}",
        f"Total sentiment score: {total_score}",
        f"Average sentiment score: {avg_score:.2f}",
        f"Overall Sentiment: {sentiment}",
        f"\n{'-' * 50}",
        f"Keyword Matches Found:"
    ]

    for keyword, score, title in matched_keywords:
        response.append(f"Keyword: '{keyword}' (Score: {score}) in headline: '{title}'")

    response.append(f"{'-' * 50}")
    return "\n".join(response)


if __name__ == "__main__":
    #user interaction, exclude this part if put to tg bot
    while True:
        command = input("Enter command (getnews / cal_score / exit): ").strip().lower()
        if command == "getnews":
            get_news()
        elif command == "cal_score":
            ticker = input("Enter ticker symbol to calculate sentiment score: ").strip()
            print(cal_score(ticker))
        elif command == "exit":
            break
        else:
            print("Invalid command. Please enter 'getnews', 'cal_score', or 'exit'.")