# encoding=utf-8
"""
dt.py

处理数据库的连接与查询
"""
import pymysql


sentiments = {0: 's_happy',      1: 's_miss',         2: 's_terrified',
              3: 's_troubled',   4: 's_disappointed', 5: 's_guilty',
              6: 's_jealous',    7: 's_shy',          8: 's_wish',
              9: 's_praise',     10: 's_angry',       11: 's_sacred',
              12: 's_aroused',   13: 's_grand',       14: 's_solemn',
              15: 's_peaceful',  16: 's_panic',       17: 's_hate',
              18: 's_criticise', 19: 's_surprise',    20: 's_doubt',
              21: 's_sad',       22: 's_warm',        23: 's_friendship',
              24: 's_in_love',   25: 's_motivate',    26: 's_blue'}


def connect_to_database(host, user, password, db, charset='utf8'):
    """
    连接mysql数据，并返回游标
    :param host: 主机地址
    :param user: 数据库用户名
    :param password: 密码
    :param db: 数据库名
    :param charset: 数据库要使用的字符集
    :return: 数据库实例
    """
    db = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)

    return db  # 返回数据库实例


def query(db, query_statement):
    """
    执行查询语句，并返回结果
    :param db: 数据库实例
    :param query_statement: 查询语句
    :return: 查询结果
    """
    cursor = db.cursor()  # 获得游标
    cursor.execute(query_statement)
    result = cursor.fetchall()

    return result  # 返回值为一个元组，每个元素也为一个元组，包含了一条数据库记录


def write(db, tb_name, entry_id, judge):
    """
    将用户评价写入数据库
    :param db: 数据库实例
    :param tb_name: 表名
    :param entry_id: 记录的id
    :param judge: 用户的评价
    :return: None
    """
    # 从表单获得的是字符串值，需转换为整型
    list_indices = []
    for item in judge:
        list_indices.append(int(item))

    # 根据用户选择获得字段名
    choices = []
    for i in list_indices:
        choices.append(sentiments[i])

    # 构造sql语句
    sql_statement = "UPDATE " + tb_name + " SET "
    for s in choices:
        sql_statement = sql_statement + s + "=" + s + "+1,"  # 例如：update tb_name set s1=s1+1,s2=s2+1...
    sql_statement = sql_statement.rstrip(",")
    sql_statement = sql_statement + " WHERE m_id=" + str(entry_id)
    #print(sql_statement)

    cursor = db.cursor()  # 获得游标
    cursor.execute(sql_statement)  # 执行sql语句
    db.commit()  # 提交到数据库执行
