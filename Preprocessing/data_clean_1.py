import pandas as pd

ratings = pd.read_csv(
    "ml-latest/ratings.csv"
)  # contains ratings of movies by users (userId, movieId,rating)

movies = pd.read_csv(
    "ml-latest/movies.csv"
)  # contains movie description (movieId , title, genres)


# removing duplicates by title, if found
movies.drop_duplicates(subset="title", keep="first", inplace=True)

# extracting year
movies["year"] = movies["title"].str.extract(".*\((.*)\).*", expand=False)
movies["year"] = movies["year"].str.strip()

# getting count of people who voted for each movie
votes = ratings[["movieId", "rating"]].groupby("movieId", as_index=False).sum()
movies["total_votes"] = votes["rating"]

# getting average rating for each movie
average_rating = (
    ratings[["movieId", "rating"]].groupby("movieId", as_index=False).mean()
)
movies["rating"] = average_rating["rating"]

# deleting rows having atleast one null values
movies.dropna(axis=0, how="any", inplace=True)

# these movies didnt had release year, so manually handled them
movies.loc[movies["movieId"] == 107434, "year"] = 2009
movies.loc[movies["movieId"] == 171749, "year"] = 2006
movies.loc[movies["movieId"] == 165821, "year"] = 2016
movies.loc[movies["movieId"] == 141628, "year"] = 1957
movies.loc[movies["movieId"] == 87442, "year"] = 2010
movies.loc[movies["movieId"] == 79607, "year"] = 1970
movies.loc[movies["movieId"] == 87442, "year"] = 2010
movies.loc[movies["movieId"] == 98063, "year"] = 1983

# reducing size of dataset
movies["movieId"] = movies["movieId"].astype("int32")
movies["title"] = movies["title"].astype("str")
movies["genres"] = movies["genres"].astype("str")
movies["year"] = movies["year"].astype("float32")
movies["total_votes"] = movies["total_votes"].astype("int32")
movies["rating"] = movies["rating"].astype("float32")


def movie_title_clean(title):
    # if ', The' or ', A' is a the end of the string, move it to the front
    # e.g. change "Illusionist, The" to "The Illusionist"
    if title[-5:] == ", The":
        title = "The " + title[:-5]
    elif title[-4:] == ", An":
        title = "An " + title[:-4]
    elif title[-3:] == ", A":
        title = "A " + title[:-3]

    return title


movies["title"] = movies["title"].apply(movie_title_clean)

#    v is the number of votes for the movie
#    m is the minimum votes required to be listed in the chart
#    R is the average rating of the movie
#    C is the mean vote across the whole report
C = movies["rating"].mean()
m = movies["total_votes"].quantile(0.98)


def weighted_rating(x):
    v = x["total_votes"]
    R = x["rating"]
    return (v / (v + m) * R) + (m / (m + v) * C)


movies["wr"] = movies.apply(weighted_rating, axis=1)
movies.drop('rating',axis=1,inplace=True)


movies.to_pickle("mov1.pkl")
