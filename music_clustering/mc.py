# coding=utf-8
"""
This module is used to load music data
"""
from itertools import islice
from databaseTransaction import dt
from app import app
import numpy as np
from sklearn.cluster import KMeans


def load_data(filename):
    """
    Load data from csv file "filename"
    :param filename: a csv file
    :return: list of lists containing records
    """
    musics = []
    input_file = open(filename)

    for line in islice(input_file, 1, None):
        cur_line = line.strip().split('\t')
        musics.append(cur_line)

    input_file.close()

    return musics


def get_sentiments(musics):
    """
    Get sentiments from musics list
    :param musics: list of lists containing records
    :return: list of lists containing sentiments
    """
    ms = np.array(musics)
    sentiments = ms[:, 2:29]
    flt_sentiments = []

    # convert strings to floats
    for st in sentiments:
        flt_sentiments.append(map(float, st))

    return flt_sentiments


def load_data_from_db():
    """
    Load music data from database
    :return: sentiments of music(matrix)
    """
    # 构造查询语句
    query_statement = 'SELECT * FROM ' + app.config['TABLE_NAME']
    # 连接数据库
    db = dt.connect_to_database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                                app.config['MYSQL_PASSWD'], app.config['DB_MUSICS'])
    # 查询音乐信息，并保存在session中
    musics = dt.query(db, query_statement)
    db.close()

    return np.mat(get_sentiments(musics))


def cluster_musics(data_set, k):
    """
    Cluster musics by using k-means algorithm
    :param data_set: data set
    :param k: number of clusters
    :return: A KMeans object
    """
    kmeans = KMeans(n_clusters=k, random_state=0).fit(data_set)

    return kmeans