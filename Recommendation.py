import pandas as pd

df = pd.read_csv('Movies.csv')

cleanData = pd.DataFrame({
    'Movie Name': df['Movie Name'],
    'Release Year': df['Movie Release Date'].str.strip('-'),
    'Rate': df['Movie Rate'].str.strip('</strong>'),
    'Genre': df['Movie Genre']
}).sort_values(by=['Rate', 'Release Year'], ascending=[True, False])


inputGenres = input("Enter the genres you want: ")
Num = int(input("How many movies do you want (max = 300): "))

genreList = [genre.strip().capitalize() for genre in inputGenres.split(",")]

filteredMovies = []
for _, row in cleanData.iterrows():
    rowGenres = [genre.strip().capitalize() for genre in row['Genre'].split(',')]
    matchCount = sum(genre in rowGenres for genre in genreList)
    if matchCount > 0:
        filteredMovies.append({
            'Movie Name': row['Movie Name'],
            'Release Year': row['Release Year'],
            'Rate': row['Rate'],
            'Genre': row['Genre'],
            'Match Count': matchCount
        })

filteredMovies = sorted(
    filteredMovies,
    key=lambda x: (x['Match Count'], x['Rate'], x['Release Year']),
    reverse=True
)

for i in range(min(Num, len(filteredMovies))):
    print(
        f"{filteredMovies[i]['Movie Name']}, {filteredMovies[i]['Release Year']}, "
        f"{filteredMovies[i]['Rate']}, {filteredMovies[i]['Genre']}"
    )

