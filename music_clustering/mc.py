# coding=utf-8
"""
This module is used to load music data
"""
from itertools import islice
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


def cluster_musics(data_set, k):
    """
    Cluster musics by using k-means algorithm
    :param data_set: data set is a list
    :param k: number of clusters
    :return: A KMeans object
    """
    data_mat = np.mat(data_set)  # convert list to matrix
    kmeans = KMeans(n_clusters=k, random_state=0).fit(data_mat)

    return kmeans


def write_cluster_to_database(labels, db, tb_name):
    """
    将聚类标签写入数据库
    :param labels: 聚类标签列表
    :param db: 数据库实例
    :param tb_name: 表名字
    :return: None
    """
    # print labels
    cursor = db.cursor()  # 获得游标
    m_id = 1
    for lb in labels:
        # print lb
        sql_statement = 'UPDATE ' + tb_name + ' SET m_cluster=' + str(lb) + ' WHERE m_id=' + str(m_id)
        cursor.execute(sql_statement)
        db.commit()  # 提交更改
        m_id += 1
