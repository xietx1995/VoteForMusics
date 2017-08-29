# coding=utf-8
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from music_clustering import mc
from app import app
from databaseTransaction import dt
import matplotlib.pyplot as plt
import numpy as np


def decomp(data_mat, n=3):
    """
    对数据data_mat进行降维，默认降到3维
    :param data_mat: 数据集
    :param n: 目标维度
    :return: None
    """
    pca = PCA(n_components=3)
    pca.fit(data_mat)
    data_new = pca.transform(data_mat)

    fig = plt.figure()
    ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=30, azim=20)
    plt.scatter(data_new[:, 0], data_new[:, 1], data_new[:, 2], marker='o')


def test():
    # 构造查询语句
    query_statement = 'SELECT * FROM ' + app.config['TABLE_NAME']
    # 连接数据库
    db = dt.connect_to_database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                                app.config['MYSQL_PASSWD'], app.config['DB_MUSICS'])
    # 查询音乐信息
    musics = dt.query(db, query_statement)
    db.close()

    # 获取音乐情感矩阵
    sent_mat = np.mat(mc.get_sentiments(musics))

    # 降维
    decomp(sent_mat)
