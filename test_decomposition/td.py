# coding=utf-8
from sklearn.decomposition import PCA
from music_clustering import mc
from databaseTransaction import dt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def decomp(data_mat, filename=None, labels=None, n=3, save=True):
    """
    对数据data_mat进行降维，默认降到3维
    :param data_mat: 数据集
    :param filename: 文件名
    :param labels: 标签
    :param n: 目标维度
    :param save: 是否保存
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

    if save and filename:
        plt.savefig('static/imgs/%s' % filename)
    else:
        plt.show()


def test(target_n=5):
    from app import app
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
    print kmeans.labels_
    # 降维
    decomp(sent_mat, labels=kmeans.labels_, save=False)
