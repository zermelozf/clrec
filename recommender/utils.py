""" Simple recommender system using collaborative filtering.
"""

from collections import defaultdict
import re

from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data
from recsys.datamodel.item import Item
from recsys.evaluation.prediction import RMSE, MAE


def load_ratings(filename):
    """ Load ratings
    """
    
    data = Data()
    format = {'col':0, 'row':1, 'value':2, 'ids': 'int'}
    data.load(filename, sep=',', format=format)
    
    return data


def load_movies(filename):
    """ Load movies.
    """
    pattern = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
    items = dict()
    for line in open(filename):
        try:
            data =  pattern.split(line)[1::2]
            item_id = int(data[0])
            item_name = data[1]
            genres = data[2].split('|')
            item = Item(item_id)
            item.add_data({'name': item_name,
                           'genres': genres})
            items[item_id] = item
        except ValueError:
            continue
    
    return items


def load_tags(filename):
    """ Load tags
    """
    items = defaultdict(set)
    for line in open(filename):
        try:
            data =  line.strip('\r\n').split(',')
            item_id = int(data[1])
            tag = data[2]
            items[item_id].add(tag.lower())
        except ValueError:
            continue
    
    return items


def create_svd_model(train):
    """ Build SVD model
    """
    
    svd = SVD()
    svd.set_data(train)
    svd.compute(k=100,
                min_values=0,
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
    desired_genres : list(str)
        list of genres
    
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
                if desired_genre in movie_genres:
                    filtered_results.append(result)
                    break
        except KeyError:
            continue
    
    return filtered_results


def filter_by_tag(results, tag_index, desired_tags):
    """ Filter by genre
    
    Arguments
    ---------
    results : list of tuples
        (movi_id, expected_rating) list
    tag_index : dict(set)
        dictionary of (movie_id, tags)
    desired_tags : list(str)
        list of tags
    
    Returns
    -------
    filtered_results : list of tuples
        Sorted results that have desired tags
    """
    
    if desired_tags is None:
        return results
    
    filtered_results = []
    for result in results:
        try:
            movie_id, _ = result
            movie_tags = tag_index[movie_id]
            for desired_tag in desired_tags:
                if desired_tag.lower() in movie_tags:
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
