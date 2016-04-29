import unittest

from recsys.datamodel.user import User

from utils import load_movies, load_ratings
from utils import create_svd_model, filter_by_genre, eval_reco

class Test(unittest.TestCase):
    
    def setUp(self):
        #Load data
        ratings = load_ratings('../data/ml-latest-small/ratings.csv')
        self.movies = load_movies('../data/ml-latest-small/movies.csv')
        
        #Train & Test data
        train, test = ratings.split_train_test(percent=80)
        self.train = train
        self.test = test
        
        self.svd = create_svd_model(self.train)

     
    def testEval(self):
        
        #Eval model
        rmse, mae = eval_reco(self.svd, self.test)
        self.assertLess(rmse.compute(), 1.)
    
    def testFiltering(self):
    
        #Recommend
        USERID = 1
        N = 10000
        results = self.svd.recommend(USERID, is_row=False, n=N)
        
        desired_genres = [1]  # Action movies
        filtered_results = filter_by_genre(results, self.movies, desired_genres)
        
        # TODO: Write proper test


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()