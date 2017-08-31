# encoding=utf-8
"""
sa.py

对文章进行分词，词频统计，查询数据库，根据词频加权法计算情感分类结果
"""
import jieba
from databaseTransaction import dt  # 导入数据库事务处理模块


# 下面是哈工大21类情感与4类音乐的映射关系
str_sad = '悲伤的'
str_hap = '欢快的'
str_lyc = '抒情的'
str_amz = '震撼的'
sentiment_map = {'NB': str_sad, 'NJ': str_sad, 'NH': str_sad, 'NI': str_sad,
                 'NC': str_sad, 'NG': str_sad, 'ND': str_sad, 'NN': str_sad,
                 'PA': str_hap, 'PE': str_hap, 'PD': str_hap, 'PH': str_hap,
                 'PG': str_hap,
                 'PF': str_lyc, 'NE': str_lyc, 'NK': str_lyc, 'NL': str_lyc,
                 'PK': str_lyc, 'PB': str_lyc,
                 'NA': str_amz, 'PC': str_amz}

# 下面是聚类和情感的映射
cluster_sent_map = {str_sad: 2, str_hap: 0, str_lyc: 1, str_amz: 3}


def word_segmentation(essay):
    """
    对输入的文章essay进行分词
    :param essay: 输入的文章
    :return: 分词结果，为一个列表
    """
    seg_list = jieba.cut(essay, cut_all=False)  # 全分模式
    result_list = []
    
    for item in seg_list:
        result_list.append(item)

    return result_list  # 返回值为一个列表


def frequency_count(seg_list):
    """
    统计词频
    :param seg_list: 分词列表
    :return: 返回值为一个字典，记录每个词出现的次数
    """
    frequency = {}

    for item in seg_list:
        if item not in frequency:
            frequency[item] = 1
        else:
            frequency[item] += 1

    return frequency


def make_query(word_frequency):
    """
    构造一个查询语句
    :param word_frequency: 词频字典
    :return: 查询结果
    """
    words = "("
    for item in word_frequency:  # 构建词表
        words = words + '\'' + item + '\','
    words = words.rstrip(',')
    words += ')'

    host = '127.0.0.1'
    user = 'root'
    password = 'daimao,./'
    database = 'sent_words'
    query_string = "SELECT * FROM sentiment_dict WHERE word_entity in " + words  # 构造查询语句
    cursor = dt.connect_to_database(host, user, password, database)  # 连接数据库
    word_info = dt.query(cursor, query_string)  # 查询词语信息

    return word_info


def make_word_class_dict(word_info):
    """
    根据数据库查询结果，构造词-类字典
    :param word_info: 数据库中记录
    :return: 根据查询结果建立的词-类字典
    """
    word_class_dict = {}
    for entry in word_info:
        word = entry[1]
        word_class = entry[5]  # 第五列为词语的类别字段
        word_class_dict[word] = word_class

    return word_class_dict


def method_word_freq(word_info, word_freq):
    """
    词频法
    :param word_info: 词语信息
    :param word_freq: 词频信息
    :return: 返回分类结果
    """
    # 四大类词计数器
    counters = {str_sad: 0, str_hap: 0, str_lyc: 0, str_amz: 0}

    # 获得词语-类别字典
    word_class_dict = make_word_class_dict(word_info)

    # 统计四大类词的分别出现的次数
    for word in word_freq:
        word_class = word_class_dict.get(word)  # 得到词类
        if word_class:  # 如果该词语存在
            if sentiment_map[word_class] == str_sad:
                counters[str_sad] += word_freq[word]
            elif sentiment_map[word_class] == str_hap:
                counters[str_hap] += word_freq[word]
            elif sentiment_map[word_class] == str_lyc:
                counters[str_lyc] += word_freq[word]
            else:
                counters[str_amz] += word_freq[word]

    # 找出出现次数最多的大类
    max_ct = 0
    music_class = ''
    for item in counters:
        if counters[item] > max_ct:
            max_ct = counters[item]
            music_class = item

    return music_class  # 返回音乐类别


def make_word_intensity_dict(word_info):
    """
    根据数据库返回的词语信息构造词语-强度字典
    :param word_info: 词语信息
    :return: 词语-强度字典
    """
    intensity_dict = {}
    for entry in word_info:
        word = entry[1]
        word_intensity = entry[6]  # 第6列为情感强度
        intensity_dict[word] = word_intensity

    return intensity_dict


def method_weighted_word_freq(word_info, word_freq):
    """
    加权词频法
    :param word_info: 词语信息
    :param word_freq: 词频信息
    :return:
    """
    word_class_dict = make_word_class_dict(word_info)  # 根据数据库返回的记录构造词语的类别字典
    intensity_dict = make_word_intensity_dict(word_info)  # 根据数据库返回的记录构造词语的强度字典
    word_lists = {str_sad: [], str_hap: [], str_lyc: [], str_amz: []}  # 保存四类词语的列表
    weighted_scores = {str_sad: 0, str_hap: 0, str_lyc: 0, str_amz: 0}  # 四大类情感的加权得分

    # 构建四类词语的列表
    for word in word_freq:
        word_class = word_class_dict.get(word)  # 得到词类
        if word_class:
            if sentiment_map[word_class] == str_sad:
                word_lists[str_sad].append(word)
            elif sentiment_map[word_class] == str_hap:
                word_lists[str_hap].append(word)
            elif sentiment_map[word_class] == str_lyc:
                word_lists[str_lyc].append(word)
            else:
                word_lists[str_amz].append(word)

    # 计算四大类情感的加权得分
    for wl in word_lists:  # wl为key
        score = 0
        for word in word_lists[wl]:  # word_lists[wl]为值，即一个词语列表
            score += intensity_dict[word] * word_freq[word]  # 强度乘以该词语出现的次数为该词语的得分
        weighted_scores[wl] = score  # 情感大类的总得分

    # 计算得分最高的情感类别
    max_score = 0
    music_class = ''
    for item in weighted_scores:
        if weighted_scores[item] > max_score:
            max_score = weighted_scores[item]
            music_class = item

    return music_class  # 返回音乐类别


def method_max_weighted(word_info, word_freq):
    """
    最大加权法
    :param word_info: 词语信息
    :param word_freq: 词频信息
    :return:
    """
    word_class_dict = make_word_class_dict(word_info)  # 根据数据库返回的记录构造词语的类别字典
    intensity_dict = make_word_intensity_dict(word_info)  # 根据数据库返回的记录构造词语的强度字典

    # 测试代码块
    # print(word_info)
    # print(word_class_dict)
    # print(intensity_dict)

    # 寻找强度最大的词
    max_intensity = 0
    res_word = ''
    for word in intensity_dict:
        intensity = intensity_dict[word] * word_freq[word]  # 一个词的总强度为词频乘以该词语的强度
        if intensity > max_intensity:
            max_intensity = intensity
            res_word = word

    word_class = word_class_dict[res_word]  # 获得情感强度最大的词语所属的类别
    music_class = sentiment_map[word_class]  # 获得音乐类别

    return music_class  # 返回音乐类别


def sentiment_classify(essay):
    """
    利用词频法，对输入的文本进行情感分析
    :param essay: 输入的文章
    :return: 情感类别
    """
    word_list = word_segmentation(essay)  # 分词
    word_frequency = frequency_count(word_list)  # 统计词频
    word_info = make_query(word_frequency)  # 获得每个词的信息

    if not word_info:  # 如果词典中不存在任何词语
        return -1

    # 测试代码块
    # print('分词：', word_list)
    # print('词频：', word_frequency)
    # print('查询结果：', word_info)

    # 利用三种方法，计算情感分类结果
    m_word_freq = method_word_freq(word_info, word_frequency)
    m_weighted = method_weighted_word_freq(word_info, word_frequency)
    m_max = method_max_weighted(word_info, word_frequency)

    return m_word_freq, m_weighted, m_max  # 返回情感结果
