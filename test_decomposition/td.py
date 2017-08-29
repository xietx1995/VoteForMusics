# coding=utf-8
from sklearn.decomposition import PCA
from music_clustering import mc
from app import app
from databaseTransaction import dt
import matplotlib.pyplot as plt
import numpy as np


def decomp(data_mat, labels=None, n=3):
    """
    对数据data_mat进行降维，默认降到3维
    :param data_mat: 数据集
    :param labels: 标签
    :param n: 目标维度
    :return: None
    """
    pca = PCA(n_components=3)
    pca.fit(data_mat)
    data_new = pca.transform(data_mat)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=30, azim=20)
    size = labels + 20
    ax.scatter(data_new[:, 0], data_new[:, 1], data_new[:, 2], marker='o', s=np.array(size), c=labels)
    plt.show()


def test(target_n=5):
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
    kmeans = mc.cluster_musics(sent_mat, target_n)

    # 降维
    decomp(sent_mat, kmeans.labels_)
