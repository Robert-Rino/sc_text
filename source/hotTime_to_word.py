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

# <<<<<<< HEAD
#deal processed video data===================================
# path = '../hot_scale/' #current dir
# dirs = os.listdir(path)
# inPath = path+dirs[0]
# # sorted(dirs)
# for key,name in enumerate(dirs):
#     if name == 'key_timeline.py':
#         del(dirs[key])
#
# week_order_timeList={}
# #future work all week data currently only week3
# week_order_timeList[3] = {}
# # 將key_timeline存入week_order_timeList
# for order,file_name in enumerate(dirs):
#     tmp_path = path+file_name
#     week_order_timeList[3][order] = {}
#     with open(tmp_path,'r') as f:
#         reader = csv.reader(f)
#         next(reader)#skip title
#         timeList = []
#         countList = []
#         for rows in reader:
#             timeList.append(int(rows[0]))
#             countList.append(int(rows[1]))
#         indexList = return_big_index_list(countList)
#         returnTimeList = []
#         returnCountList = []
#         for index_count in indexList[:5]:
#             returnTimeList.append(timeList[index_count[0]])
#             returnCountList.append(countList[index_count[0]])
#         week_order_timeList[3][order]['time'] = returnTimeList
#         week_order_timeList[3][order]['count'] = returnCountList
# 分割字幕成關鍵字存入檔案
# for folder in os.listdir('../original_file'):
#     # print(folder + '============================')
#     week_dir = '../original_file/'+ folder
#     for filename in os.listdir(week_dir):
#         # print(filename + '============================')
#         fr = open('../original_file/' + folder + '/' + filename)
#         fw = open('../it_done/' + folder + '/' + filename,'w')
#         # subtitle = {}
#         content_list = fr.read().splitlines()
#
#         file = filename.split(".txt")
#
#         for point in range(0,5):
#             scale_start = week_order_timeList[int(folder)][int(file[0])]['time'][point]
#             scale_end = scale_start + 5
# =======
#deal processed timeline data===================================

path = '../hot_scale/' #current dir
dirs = os.listdir(path)
inPath = path+dirs[0]
# sorted(dirs)
for key,name in enumerate(dirs):
    if name == 'key_timeline.py':
        del(dirs[key])

week_order_timeList={}
#future work all week data currently only week3
week_order_timeList[3] = {}
# 將key_timeline存入week_order_timeList
for order,file_name in enumerate(dirs):
    tmp_path = path+file_name
    week_order_timeList[3][order] = {}
    with open(tmp_path,'r') as f:
        reader = csv.reader(f)
        next(reader)#skip title
        timeList = []
        countList = []
        for rows in reader:
            timeList.append(int(rows[0]))
            countList.append(int(rows[1]))
        indexList = return_big_index_list(countList)
        returnTimeList = []
        returnCountList = []
        for index_count in indexList[:5]:
            returnTimeList.append(timeList[index_count[0]])
            returnCountList.append(countList[index_count[0]])
        week_order_timeList[3][order]['time'] = returnTimeList
        week_order_timeList[3][order]['count'] = returnCountList

store_it_done()

folder = input("Which folder? ")
filename = input("Which file?(ex : 0.txt) ")

# 分割字幕成關鍵字存入檔案
subtitle = {}
keyword = []

fr = open('../original_file/' + folder + '/' + filename)
content_list = fr.read().splitlines()
file = filename.split(".txt")
for point in range(0,5):
    scale_start = week_order_timeList[3][int(file[0])]['time'][point]
    scale_end = scale_start + 5
    for index, content in enumerate(content_list):
        if index % 4 == 1:
            # time
            time = content.split()
            time.pop(1)
            start = datetime.datetime.strptime(time[0], "%H:%M:%S,%f")
            end = datetime.datetime.strptime(time[1], "%H:%M:%S,%f")
            video_start = start.minute*60 + start.second
            video_end = end.minute*60 + end.second
            tmp_time = [video_start,video_end]
            words = jieba.analyse.extract_tags(content_list[index +1])
            tmp_word = []
            for word in words:
                if word != ' ':
                    tmp_word.append(word)
            subtitle[video_start,video_end] = tmp_word
            keyword_time = get_key_word(scale_start,scale_end,tmp_time[0],tmp_time[1])
            if keyword_time != None:
                keyword.append(subtitle[keyword_time[0],keyword_time[1]])
print(keyword)
fr.close()
