# coding=utf-8
"""
This module is used to load music data
"""
from itertools import islice
import numpy as np


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
