#-*- coding=utf-8 -*-
import csv,sys,os
import jieba
import datetime

jieba.set_dictionary('../dict/extra_dict/dict.txt.big')
jieba.set_dictionary('../dict/keyword.txt')
keywords_dir = '../dict/userdict.txt'

def return_big_index_list(timelineCount):
    tmp = []
    for index,count in enumerate(timelineCount):
        tmp.append((index,int(count)))
    # print tmp
    sorted_index_list = sorted(tmp , key = lambda x :x[1],reverse=True)
    # print sorted_index_list
    return sorted_index_list

def get_key_word(scale_start,scale_end,video_start,video_end):
    if video_end > scale_start:
        if scale_end > video_start:
            return video_start,video_end

# preprocess 原始字幕黨成 ((startTime,endTime):[wordList])
# original_file : 原始字幕黨
# it_done : 處理好的字幕黨
def preprocessSubtitle():
    with open(keywords_dir) as f:
        key_list = f.read().splitlines()
    for folder in os.listdir('../original_file'):
        print(folder + '============================')
        for filename in os.listdir('../original_file/'+ folder):
            print(filename + '============================')
            fr = open('../original_file/' + folder + '/' + filename)
            fw = open('../it_done/' + folder + '/' + filename,'w')
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
                    words = jieba.cut(content_list[index +1], cut_all=False)
                    tmp_word = []
                    for word in words:
                        if word != ' ':
                            tmp_word.append(word)
                    key = set(tmp_word).intersection(set(key_list))
                    fw.write('(' + str(video_start) + ',' + str(video_end) + ')' + ' : ' + str(key) + '\n' )
            fr.close()

# preprocess 原始字幕黨
preprocessSubtitle()
