# Command line recommender system

A minimalistic recommender system based on python-recsys.

Use SVD decomposition to perform collaborative filtering. Also allows to filter results by genre.

## Dependency

This program depends on [python-recsys](http://ocelma.net/software/python-recsys/build/html/installation.html)

## Run program

```shell
cd recommender
python recommender.py
```

## Docker run

This script has been packaged with [docker](https://www.docker.com) to ease
installation and running.

To use it please install the [docker toolbox](https://www.docker.com/products/overview#/docker_toolbox)
and run the following command from a docker terminal:

```
docker run -v /my/data/folder:/data -it zermelozf/clrec
```

where `/my/data/folder` is the location of your dataset. Datasets are available 
on the [Movielens site](http://grouplens.org/datasets/movielens/latest/).
