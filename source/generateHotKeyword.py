#-*- coding=utf-8 -*-
import csv,sys,os
import jieba
import jieba.analyse
import jieba.posseg as pseg
import datetime

jieba.set_dictionary('../dict/extra_dict/dict.txt.big')
jieba.analyse.set_stop_words("../dict/pleonasm.txt")
jieba.analyse.set_stop_words("../dict/extra_dict/stop_words.txt")
jieba.analyse.set_idf_path("../dict/extra_dict/idf.txt.big");
jieba.load_userdict('../dict/userdict.txt')

hotTime_dir = '../to_weeks_preprocessed/'
keyword_dir = '../it_done/'

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

def store_it_done():
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
                    words = jieba.analyse.extract_tags(content_list[index +1])
                    tmp_word = []
                    for word in words:
                        if word != ' ':
                            tmp_word.append(word)
                    fw.write('(' + str(video_start) + ',' + str(video_end) + ')' + ' : ' + str(tmp_word) + '\n' )
            fr.close()
