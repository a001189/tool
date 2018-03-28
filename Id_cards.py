#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2018/3/26 15:05
# @Author  : ysj


def get_IDs(prefix='411327', birth='19930101', sex=0):
    """create all IDs， sex: 1 is male ,0 is female"""
    str_14 = prefix + birth
    return (str_14 + code + suffix(str_14 + code) for code in three(sex))


def suffix(number):
    """Enter the first 17 IDs and return to the last"""
    numbers = str(number)
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    final = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    score = sum((int(x) * y for x, y in zip(numbers, weight)))
    _, index = divmod(score, 11)
    return final[index]


def three(sex=False):
    """
    According to men and women, false is female
    :return: all sequence codes of this type (the 15~17 of IDs)
    """
    start = 11 if sex else 10
    return ('{:03}'.format(x) for x in range(start, 1000, 2))


if __name__ == '__main__':
    s = list(get_IDs())
    print(s)
    print(len(s))
