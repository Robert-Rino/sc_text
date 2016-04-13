#-*- coding=utf-8 -*-
import csv
import sys
import os
import re
import jieba
import datetime

jieba.set_dictionary('../dict/extra_dict/dict.txt.big')
jieba.set_dictionary('../dict/keyword.txt')
keywords_dir = '../dict/userdict.txt'
phrase_dir = '../dict/phrase.txt'

# preprocess 原始字幕黨成 ((startTime,endTime):[wordList])
# original_file : 原始字幕黨
# it_done : 處理好的字幕黨


def preprocessSubtitle():
    with open(keywords_dir) as f:
        key_list = f.read().splitlines()

    with open(phrase_dir) as f:
        phrase_list = f.read()
    cut_phrase = phrase_list.split('\n')

    for folder in os.listdir('../original_file'):
        print(folder + '============================')
        for filename in os.listdir('../original_file/' + folder):
            print(filename + '============================')
            fr = open('../original_file/' + folder + '/' + filename)
            fw = open('../it_done/' + folder + '/' + filename, 'w')
            content_list = fr.read().splitlines()
            for index, content in enumerate(content_list):
                if index % 4 == 1:
                    # time
                    time = content.split()
                    time.pop(1)
                    start = datetime.datetime.strptime(time[0], "%H:%M:%S,%f")
                    end = datetime.datetime.strptime(time[1], "%H:%M:%S,%f")
                    video_start = start.minute*60 + start.second
                    video_end = end.minute*60 + end.second
                    #keywords
                    words = jieba.cut(content_list[index + 1], cut_all=False)
                    tmp_word = []
                    for word in words:
                        if word != ' ' and word != '-' and word != '.' and word != '/' and word != '^':
                            if re.search(word, phrase_list):
                                new_word = filter(lambda x: word in x,
                                                  cut_phrase)
                                tmp_word.extend(new_word)
                            else:
                                tmp_word.append(word)
                    key = set(tmp_word).intersection(set(key_list))
                    fw.write('(' + str(video_start) + ',' + str(video_end)
                                 + ')' + ' : ' + str(key) + '\n')
            fr.close()

# preprocess 原始字幕黨
preprocessSubtitle()
