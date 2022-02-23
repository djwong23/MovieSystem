# FILL IN ALL THE FUNCTIONS IN THIS TEMPLATE
# MAKE SURE YOU TEST YOUR FUNCTIONS WITH MULTIPLE TEST CASES
# ASIDE FROM THE SAMPLE FILES PROVIDED TO YOU, TEST ON YOUR OWN FILES

# WHEN DONE, SUBMIT THIS FILE TO CANVAS

import math
from collections import defaultdict
from collections import Counter


# YOU MAY NOT CODE ANY OTHER IMPORTS

# ------ TASK 1: READING DATA  --------

# 1.1
def read_ratings_data(f):
    # parameter f: movie ratings file name f (e.g. "movieRatingSample.txt")
    # return: dictionary that maps movie to ratings
    # WRITE YOUR CODE BELOW
    out = {}
    file = open(f)
    for line in file:
        arr = line.split('|')
        if arr[0] not in out:
            out[arr[0]] = [float(arr[1])]
        else:
            out[arr[0]].append(float(arr[1]))
    return out


# 1.2
def read_movie_genre(f):
    # parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
    # return: dictionary that maps movie to genre
    # WRITE YOUR CODE BELOW
    file = open(f)
    out = {}
    for line in file:
        arr = line.split('|')
        genre = arr[0].strip()
        movie = arr[2].strip()
        if movie not in out:
            out[movie] = genre

    return out


# ------ TASK 2: PROCESSING DATA --------

# 2.1
def create_genre_dict(d):
    # parameter d: dictionary that maps movie to genre
    # return: dictionary that maps genre to movies
    # WRITE YOUR CODE BELOW
    out = {}
    for item in d.items():
        if item[1] not in out:
            out[item[1]] = [item[0]]
        else:
            out[item[1]].append(item[0])
    return out


# 2.2
def calculate_average_rating(d):
    # parameter d: dictionary that maps movie to ratings
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    out = {}
    for item in d.items():
        sum = float()
        for rating in item[1]:
            sum += rating
        out[item[0]] = sum / len(item[1])
    return out


# ------ TASK 3: RECOMMENDATION --------

# 3.1
def get_popular_movies(d, n=10):
    # parameter d: dictionary that maps movie to average rating
    # parameter n: integer (for top n), default value 10
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    if len(d.keys()) <= n:
        return d
    movies = sorted(d.items(), reverse=True, key=lambda x: x[1])
    return {movies[i][0]: movies[i][1] for i in range(0, n)}


# 3.2
def filter_movies(d, thres_rating=3):
    # parameter d: dictionary that maps movie to average rating
    # parameter thres_rating: threshold rating, default value 3
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    movies = [x for x in d.items() if x[1] >= thres_rating]
    return{x[0]: x[1] for x in movies}


# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    
    movies = genre_to_movies[genre]
    movies.sort(reverse=True, key=lambda name : movie_to_average_rating[name])
   
    return {movies[i]: movie_to_average_rating[movies[i]] for i in range(0, min(len(movies),n))}


# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
# parameter genre: genre name (e.g. "Comedy")
# parameter genre_to_movies: dictionary that maps genre to movies
# parameter movie_to_average_rating: dictionary  that maps movie to average rating
# return: average rating of movies in genre
# WRITE YOUR CODE BELOW

    movies = genre_to_movies[genre]
    average = 0
    for x in movies:
        average += movie_to_average_rating[x]  
    average /= len(movies)
    
    return average

# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
# parameter genre_to_movies: dictionary that maps genre to movies
# parameter movie_to_average_rating: dictionary  that maps movie to average rating
# parameter n: integer (for top n), default value 5
# return: dictionary that maps genre to average rating
# WRITE YOUR CODE BELOW

    genres = [x[0] for x in genre_to_movies.items()]
    genres.sort(reverse=True, key= lambda genre : get_genre_rating(genre, genre_to_movies, movie_to_average_rating))
    genreRatings = {genres[i]:get_genre_rating(genres[i], genre_to_movies, movie_to_average_rating) for i in range (0,min(len(genres),n))}
    
    return genreRatings

# ------ TASK 4: USER FOCUSED  --------

# 4.1
def read_user_ratings(f):
# parameter f: movie ratings file name (e.g. "movieRatingSample.txt")
# return: dictionary that maps user to movies and ratings
# WRITE YOUR CODE BELOW
    out = {}
    file = open(f)
    for line in file:
        arr = line.split('|')
        user = int(arr[2])
        
        if user not in out:
            out[user] = [tuple((arr[0], float(arr[1])))]
        else:
            out[user].append(tuple((arr[0], float(arr[1]))))
            
    return out

# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
# parameter user_id: user id
# parameter user_to_movies: dictionary that maps user to movies and ratings
# parameter movie_to_genre: dictionary that maps movie to genre
# return: top genre that user likes
# WRITE YOUR CODE BELOW

   genreRatings = defaultdict(int)
    genreCount = defaultdict(int)
    for movie in user_to_movies[user_id]:
        genreRatings[movie_to_genre[movie[0]]] += movie[1]
        genreCount[movie_to_genre[movie[0]]] += 1
            
    for genre in genreRatings.items():
        genreRatings[genre[0]] /= genreCount[genre[0]]
        
    return max(genreRatings, key=genreRatings.get)

# 4.3
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
# parameter user_id: user id
# parameter user_to_movies: dictionary that maps user to movies and ratings
# parameter movie_to_genre: dictionary that maps movie to genre
# parameter movie_to_average_rating: dictionary that maps movie to average rating
# return: dictionary that maps movie to average rating
# WRITE YOUR CODE BELOW
    
    topGenre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    watchedMovies = [movie[0] for movie in user_to_movies[user_id]]
    genreList = [movie[0] for movie in movie_to_genre.items() if movie[1] == topGenre and movie[0] not in watchedMovies]
    genreList.sort(key = lambda name : movie_to_average_rating[name], reverse=True)
    
    movieRec = {genreList[i]:movie_to_average_rating[genreList[i]] for i in range(0,(min(len(genreList),3))) }
    
    return movieRec

# -------- main function for your testing -----
def main():
    # print(create_genre_dict(read_movie_genre('genreMovieSample.txt')))
    # print(get_popular_movies(calculate_average_rating(read_ratings_data('movieRatingSample.txt')), 8))
    #print(filter_movies(calculate_average_rating(read_ratings_data('movieRatingSample.txt')),5))
    
    #my tests
    #print(get_genre_rating('Comedy', create_genre_dict(read_movie_genre('genreMovieSample.txt')), calculate_average_rating(read_ratings_data('movieRatingSample.txt'))))
    #print(genre_popularity(create_genre_dict(read_movie_genre('genreMovieSample.txt')), calculate_average_rating(read_ratings_data('movieRatingSample.txt')),2))
    #print(read_user_ratings('movieRatingSample.txt'))
    #print(get_user_genre(6, read_user_ratings('movieRatingSample.txt'), read_movie_genre('genreMovieSample.txt')))
    #print(recommend_movies(1, read_user_ratings('movieRatingSample.txt'), read_movie_genre('genreMovieSample.txt'),calculate_average_rating(read_ratings_data('movieRatingSample.txt'))))
# write all your test code here
# this function will be ignored by us when grading


# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions


# program will start at the following main() function call
# when you execute hw1.py
main()
