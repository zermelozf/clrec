""" Simple command line movie recommender.
"""

import random
import os

from recsys.datamodel.user import User
from recsys.datamodel.data import Data

from utils import load_movies, load_ratings, load_tags
from utils import create_svd_model, filter_by_genre, filter_by_tag


GENRE = {0: 'Unknow',
    1: 'Action',
    2: 'Adventure',
    3: 'Animation',
    4: 'Children\'s',
    5: 'Comedy',
    6: 'Crime',
    7: 'Documentary',
    8: 'Drama',
    9: 'Fantasy',
    10: 'Film-Noir',
    11: 'Horror',
    12: 'Musical',
    13: 'Mystery',
    14: 'Romance',
    15: 'Sci-Fi',
    16: 'Thriller',
    17: 'War',
    18: 'Western'}


def see_ratings(user_id, movies, ratings):
    
    os.system('clear')
    print """MY RATINGS
----------

movie                                              rating
"""
    for rating, iid, uid in ratings:
        if user_id == uid:
            print '{:<50}'.format(movies[iid]._data['name'][:50]),
            print rating
    
    print ""
    try:
        input("[Enter] to got back to menu.")
    except:
        pass

def random_rating(user_id, movies, ratings):
    
    os.system('clear') 
    print ("RATING\n"
           "------\n"
           "\n"
           "Ratings should be between 1 and 5.\n"
           "\n"
           "Enter `-1` if to stop rating.")

    rating = 0
    while rating != -1:
        print ""
        item_id = movies.keys()[random.randint(0, len(movies))]
        movie_name = movies[item_id]._data['name']
        print "Please rate \"%s\"" % movie_name
        try:
            rating = input("Your rating ([Enter] to skip): ")
            if rating != -1:
                ratings.add_tuple((rating, item_id, user_id))
        except SyntaxError:
            continue
    
    return ratings


def select_genre(results, movies):
    
    os.system('clear')
    
    print """GENRE
-----

What genre would you like to select?"
"""
    print 
    
    for k, v in GENRE.iteritems():
        print "%s: %s" % (k, v)
    
    try:
        desired_genres = [GENRE[input("Your choice (Enter to skip): ")]]
    except SyntaxError:
        desired_genres = None
        
    filtered_results = filter_by_genre(results, movies, desired_genres)
    
    return filtered_results

def select_keyword(results, tags):
    
    os.system('clear')  
    print """KEYWORD
-------

Would you like to filter by keyword (ex. Christian Bale)?
"""
    
    try:
        desired_tags = [str(raw_input("Your choice (Enter to skip): "))]
    except SyntaxError:
        desired_tags = None
    
    filtered_results = filter_by_tag(results, tags, desired_tags)
    
    return filtered_results


def menu(user_id, results, movies):
    
    os.system('clear')
    
    print """MENU
----
"""
    
    if results != []:
        print "Here are some recommendations for you, % s:\n" % user_id
        for movie_id, rating in results[:10]:
            print '   {:<50}'.format(movies[movie_id]._data['name'][:50]), 
            print "%.1f stars" % rating
    else:
        print "No match for now."

    print """
1. Rate movies
2. Filter movies by genre
3. Filter movies by keyword
4. See my ratings
5. Save & quit
    """
    
    choice = input("Enter your choice: ")
    
    return choice


if __name__ == "__main__":
    
    #Load data
    try:
        ratings = Data()
        ratings.load('../data/myratings.data')
    except:
        ratings = load_ratings('../data/ml-latest-small/ratings.csv')
    movies = load_movies('../data/ml-latest-small/movies.csv')
    tags = load_tags('../data/ml-latest-small/tags.csv')
    
    os.system('clear')
    print """
#####################################################
####           COMMAND LINE RECOMMENDER          ####
#####################################################

A minimalistic command line recommender system using
SVD decomposistion.
"""
    
    # Create a user
    user_id = str(raw_input("Please enter your username: "))
    user = User(user_id)
    
    #Create and train model
    svd = create_svd_model(ratings)
    
    N = 10000
    choice = -1
    while True:
        
        #recommend
        try:
            results = svd.recommend(user_id, is_row=False, n=N)
        except KeyError:
            results = []
        if choice == 4:  # See ratings
            see_ratings(user_id, movies, ratings)
        if choice == 1:  # Rate movies
            ratings = random_rating(user_id, movies, ratings)
            svd = create_svd_model(ratings)  # Update model
            try:
                results = svd.recommend(user_id, is_row=False, n=N)
            except KeyError:
                results = []
        if choice == 2:  # Filter by genre
            results = select_genre(results, movies)
        if choice == 3:  # Filter by tag
            results = select_keyword(results, tags)
        if choice == 5:  # Save & Quit
            ratings.save('../data/myratings.data')
            print "\nThank you!\n"
            break
        
        choice = menu(user_id, results, movies)
            