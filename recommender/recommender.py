""" Simple command line movie recommender.
"""

import random

from recsys.datamodel.user import User

from utils import load_movies, load_ratings
from utils import create_svd_model, filter_by_genre


#Load data
ratings = load_ratings('../data/ml-100k/u.data')
movies = load_movies('../data/ml-100k/u.item')

#Create a user
user_id = 1234567890
user = User(user_id)

print """
##################################
#### COMMAND LINE RECOMMENDER ####
##################################

Please rate a few movies. 

Ratings should be between 1 and 5. 
Enter `-1` if you if you would like
to stop rating.

The more movies you rate the better
the recommendation will be.

----------------------------------"""

rated = 0
while rated != -1:
    print ""
    item_id = random.randint(0, len(movies))
    movie_name = movies[item_id]._data['name']
    print "Please rate \"%s\"" % movie_name
    try:
        rating = input("Your rating (Enter to skip): ")
    except SyntaxError:
        continue
    if rating == -1:
        break
    ratings.add_tuple((rating, item_id, user_id))
    rated += 1
    

#Create and train model
svd = create_svd_model(ratings)

#recommend
N = 10000
results = svd.recommend(user_id, is_row=False, n=N)

print """
Please select a genre:

0: Unknow
1: Action
2: Adventure
3: Animation
4: Children's
5: Comedy
6: Crime
7: Documentary
8: Drama
9: Fantasy
10: Film-Noir
11: Horror
12: Musical
13: Mystery
14: Romance
15: Sci-Fi
16: Thriller
17: War
18: Western
"""
try:
    desired_genres = [input("Your choice (Enter to skip): ")]
except SyntaxError:
    desired_genres = None
    
filtered_results = filter_by_genre(results, movies, desired_genres)

print "\nHere are some recommendations for you:\n"

for movie_id, rating in filtered_results[:10]:
    print movie_id, movies[movie_id]._data['name'], rating