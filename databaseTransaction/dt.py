# encoding=utf-8
"""
dt.py

处理数据库的连接与查询
"""
import pymysql


def connect_to_database(host, user, password, db, charset='utf8'):
    """
    连接mysql数据，并返回游标
    :param host: 主机地址
    :param user: 数据库用户名
    :param password: 密码
    :param db: 数据库名
    :param charset: 数据库要使用的字符集
    :return: 游标
    """
    db = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)
    cursor = db.cursor()

    return cursor  # 返回游标


def query(cursor, query_statement):
    """
    执行查询语句，并返回结果
    :param cursor: 游标
    :param query_statement: 查询语句
    :return: 查询结果
    """
    cursor.execute(query_statement)
    result = cursor.fetchall()

    return result  # 返回值为一个元组，每个元素也为一个元组，包含了一条数据库记录
