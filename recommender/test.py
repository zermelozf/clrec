import unittest

from recsys.datamodel.data import Data
from recsys.datamodel.item import Item

from utils import create_svd_model, filter_by_genre, eval_reco


ratings = [(5, 0, 0), (4, 1, 0), (1, 2, 0), (3, 3, 0), (3, 4, 0), (4, 4, 0),
           (1, 0, 1), (1, 1, 1), (4, 2, 1), (3, 3, 0), (2, 4, 1), (5, 4, 1),
           (2, 0, 2), (5, 1, 2), (5, 2, 2), (1, 3, 2), (1, 4, 2), (2, 4, 2),
           (5, 0, 3), (4, 1, 3), (1, 2, 3), (3, 3, 1), (3, 4, 2), (4, 4, 1),]

movie_genres = [
        (0, 'movie1', set(['Action', 'Drama'])), 
        (1, 'movie2', set(['Adventure', 'Action'])),
        (2, 'movie3', set(['Thriller'])),
        (3, 'movie4', set(['Musical']))]


class Test(unittest.TestCase):
    
    def setUp(self):
        
        data = Data()
        for stars, item_id, user_id in ratings:
            data.add_tuple((stars, item_id, user_id))
        
        movies = dict()
        for mid, name, genres in movie_genres:
            movie = Item(mid)
            movie.add_data({'name': name, 'genres': genres})
            movies[mid] = movie
        
        self.ratings = data
        self.movies = movies


    def testEval(self):
        
        ratings = self.ratings
        svd = create_svd_model(ratings)
        rmse, _ = eval_reco(svd, ratings)


    def testFiltering(self):
        
        movies = self.movies
        results = [(0, 5), (1, 3), (2, 3), (3, 3)]
        
        desired_genres = ['Action']  # Action movies
        filtered_results = filter_by_genre(results, movies, desired_genres)
        
        self.assertEqual(filtered_results, [(0, 5), (1, 3)])
        
        # TODO: Write proper test


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()