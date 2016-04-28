""" Simple recommender system using collaborative filtering.
"""

from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data
from recsys.datamodel.item import Item
from recsys.evaluation.prediction import RMSE, MAE


def load_ratings(filename):
    """ Load ratings
    """
    
    data = Data()
    format = {'col':0, 'row':1, 'value':2, 'ids': 'int'}
    data.load(filename, sep='\t', format=format)
    
    return data


def load_movies(filename):
    """ Load movies.
    """
    
    items = dict()
    for line in open(filename):
        try:
            data =  line.strip('\r\n').split('||')
            item_id, item_name, release_date = data[0].split('|')
            att = data[1].split('|')
            url = att[0]
            genres = att[1:]
            item = Item(int(item_id))
            item.add_data({'name': item_name,
                           'url': url,
                           'release_date': release_date,
                           'genres': genres})
            items[int(item_id)] = item
        except ValueError:
            continue
    
    return items

def create_svd_model(train):
    """ Build SVD model
    """
    
    svd = SVD()
    svd.set_data(train)
    svd.compute(k=100,
                min_values=5,
                pre_normalize=None,
                mean_center=True,
                post_normalize=True)
    
    return svd


def filter_by_genre(results, movies, desired_genres=None):
    """ Filter by genre
    
    Arguments
    ---------
    results : list of tuples
        (movi_id, expected_rating) list
    movies : dict
        dictionary of movie items
    desired_genres : list(int)
        list of genre IDs
    
    Returns
    -------
    filtered_results : list of tuples
        Sorted results that belong to the desired genre
    """
    
    if desired_genres is None:
        return results
    
    filtered_results = []
    for result in results:
        try:
            movie_id, _ = result
            movie_genres = movies[movie_id]._data['genres']
            for desired_genre in desired_genres:
                if movie_genres[desired_genre] == '1':
                    filtered_results.append(result)
                    break
        except KeyError:
            continue
    
    return filtered_results


def eval_reco(model, test):
    """ Compute RMSE and MAE on test set
    """

    #Evaluation using prediction-based metrics
    rmse = RMSE()
    mae = MAE()
    for rating, item_id, user_id in test.get():
        try:
            pred_rating = model.predict(item_id, user_id)
            rmse.add(rating, pred_rating)
            mae.add(rating, pred_rating)
        except KeyError:
            continue

    return rmse, mae
    

if __name__ == "__main__":
    
    #Load data
    ratings = load_ratings('../data/ml-100k/u.data')
    movies = load_movies('../data/ml-100k/u.item')
     
    #Train & Test data
    train, test = ratings.split_train_test(percent=80)
     
    #Create model
    svd = create_svd_model(train)
 
    #Eval model
    rmse, mae = eval_reco(svd, test)
     
    print 'RMSE=%s' % rmse.compute()
    print 'MAE=%s' % mae.compute()
    
    #Recommend
    USERID = 1
    N = 10000
    results = svd.recommend(USERID, is_row=False, n=N)

    print results
    
    desired_genres = [1]  # Action movies
    filtered_results = filter_by_genre(results, movies, desired_genres)
    
    for movie_id, rating in filtered_results:
        print movie_id, movies[movie_id]._data['name'], rating