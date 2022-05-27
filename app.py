from tmdbv3api import Movie
import streamlit as st

from time import time
import pandas as pd
import numpy as np
import datetime

import second


output = st.sidebar.radio("Nevigation", ["Movie", "Popular", "Top Rated", "Recently Released", "Rate the Movie"])

if output == "Movie":
    # to take input(movie name) from user
    selected_movie_name = second.title('Movie')

    if st.button("Recommend"):
        recommendations = second.recommend(selected_movie_name)

        list = []
        list.append(selected_movie_name)

        # it will show the selected movie details
        second.movie_details(list)

        # to display the Poster of recommended movies in sidebar
        second.side_bar_poster(recommendations)

        # to show the details of recommended movies
        st.header("Recommendations")
        second.movie_details(recommendations)


elif output == "Popular":
    second.title('Popular')

    # get popular movies on the basis of genre
    genre = second.get_genre()

    genre_id = {"Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35, "Crime": 80, "Documentary": 99, "Drama": 18, "Family": 10751, "Fantasy": 14, "History": 36,
                "Horror": 27, "Music": 10402, "Mystery": 9648, "Romance": 10749, "Science Fiction": 878, "TV Movie": 10770, "Thriller": 53, "War": 10752, "Western": 37}


    if st.button("Recommend") or st.sidebar.button("Recommend", key="pop"):
        tmdb_movie = Movie()
        result = tmdb_movie.popular()

        recommendations = []
        # from all popular movies get the movies of selected genre
        for i in range(len(result)):
            # check if the movie is of selected genre
            if genre_id[genre] in result[i]['genre_ids']:
                recommendations.append(result[i].title)

        # if no movie is found
        if len(recommendations) == 0:
            st.error("No recommendations found")
            st.sidebar.error("No recommendations found")
        else:
            # if movie is found then get the posters then display in sidebar
            second.side_bar_poster(recommendations)

            # to show the details of recommended movies
            st.header("Recommendations")
            second.movie_details(recommendations)


elif output == "Top Rated":
    second.title('Top Rated')

    movie = Movie()
    top_rated_movies = movie.top_rated()
    movie_list = []

    for i in range(len(top_rated_movies)):
        movie_list.append(top_rated_movies[i].title)

    second.side_bar_poster(movie_list)
    second.movie_details(movie_list)


elif output == "Recently Released":
    second.title('Recently Released')

    movie = Movie()
    upcoming_movies = movie.upcoming()
    movie_list = []
    for i in range(len(upcoming_movies)):
        movie_list.append(upcoming_movies[i].title)

    second.side_bar_poster(movie_list)
    second.movie_details(movie_list)


elif output == "Rate the Movie":

    data = pd.read_csv("users_movie_rating.csv")
    movie_name = second.title('Rate the Movie')
    st.subheader("Rating of the movie: " + movie_name)

    second.movie_current_rating(movie_name, data)

    # slider to get the rating of the movie
    rating = st.slider("Rate the movie", 1, 10)

    # date of last rating
    date = datetime.datetime.now().strftime("%d-%m-%Y")

    # time of last rating
    time = datetime.datetime.now().strftime("%H:%M:%S")

    # name of last user who rated the movie
    user = st.text_input("Enter your name:")

    if st.button("Rate"):

        # add the data to particular row and particular column of csv file
        for i in range(len(data)):

            # check movie_title matches with movie name
            if data["movie_title"].values[i] == movie_name:

                # check if value is nan
                if np.isnan(data["rating"].values[i]):
                    data["rating"].values[i] = 0.0

                if np.isnan(data['vote_count'].values[i]):
                    data['vote_count'].values[i] = 0.0

                data["rating"].values[i] = second.avg_rating(data, rating, i)
                data["date"].values[i] = date
                data["time"].values[i] = time
                data["user"].values[i] = user
                data['vote_count'].values[i] += 1

                # write the data to csv file
                data.to_csv("users_movie_rating.csv", index=False)
                break

        second.success_message(data, movie_name)




# I want to display the top rated movies from the my database csv files but now 
# sufficient votes has been not given to the movies.
# Once each movie get enough votes then I will displayed the "top rated movies section" from app database.
# till now the movies are displayed in the "top rated movies section" from the databse of tmdb .


# tp rated movies from users_movie_rating.csv
# def top_rated_movies():
#     data = pd.read_csv("users_movie_rating.csv")
#     movie_list = {}
#     for i in range(len(data)):
#         # append movies title with movie rating
#         if np.isnan(data["rating"].values[i]):
#             continue
#         movie_list[data["movie_title"].values[i]] = data["rating"].values[i]
#         if len(movie_list) == 10:
#             break

#     # sort the movies based on rating in ascending order
#     sorted_movie_list = sorted(movie_list.items(), key=operator.itemgetter(1), reverse=True)
#     return sorted_movie_list


# # to print the top rated movies in table form
# if st.button("Top Rated Movies"):
#     st.subheader("According to app users Top Rated Movies")
#     sorted_movie_list = top_rated_movies()
#     st.table(pd.DataFrame(sorted_movie_list, columns=["Movie", "Rating"]).style.set_caption("Top Rated Movies"))