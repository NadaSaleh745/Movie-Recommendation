import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import csv


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
}
url = f"https://editorial.rottentomatoes.com/guide/best-movies-of-all-time/"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    moviesLinks = soup.findAll('a', {'class': 'title'})
    moviesNames = [link.get_text() for link in moviesLinks]
    dates = soup.findAll('span', {'class': 'year'})
    movieDate = [date.get_text() for date in dates]
    rates = soup.findAll('strong')

    Genre = []
    i = 0
    for i, movieLink in enumerate(moviesLinks):
        urls = f'{movieLink['href']}'
        response = requests.get(urls, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        genres = soup.find_all("rt-text", {"slot": "metadataGenre"})
        genre_texts = [genre.get_text(strip=True) for genre in genres]
        Genre.append(', '.join(genre_texts))
        print(f'{i + 1}. {moviesNames[i]} scraped')
        time.sleep(2)

    min_length = min(len(moviesNames), len(movieDate), len(rates), len(Genre))
    moviesNames = moviesNames[:min_length]
    movieDate = movieDate[:min_length]
    rates = rates[:min_length]
    Genre = Genre[:min_length]

    df = pd.DataFrame({
        'Movie Name': moviesNames,
        'Movie Release Date': movieDate,
        'Movie Rate': rates,
        'Movie Genre': Genre,
    })
    print(df)

    df.to_csv('Movies.csv', index=False, encoding='UTF8')


else:
    print(f"Failed to fetch URL. Status code: {response.status_code}")

