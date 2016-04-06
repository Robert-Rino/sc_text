#-*- coding=utf-8 -*-
import csv
import sys
import os
import datetime
import requests
import json
import operator

subtitle_dir = '../it_done'
timeLine_dir = '../to_weeks_preprocessed'
result_dir = '../hot_word'

# 輸入countList
# 會回傳依照關鍵次出現次數降冪排列的對應(index,count)的list


def return_big_index_list(timelineCount):
    tmp = []
    for index, count in enumerate(timelineCount):
        tmp.append((index, int(count)))
    # print tmp
    sorted_index_list = sorted(tmp, key=lambda x: x[1], reverse=True)
    # print(sorted_index_list)
    return sorted_index_list


def get_key_word(scale_start, scale_end, video_start, video_end):
    if video_end >= scale_start:
        if scale_end >= video_start:
            return video_start, video_end

# def create_dir_ifNotExist(dir_path):
#     if not os.path.exists(dir_path):
#         os.makedirs(dir_path)


def makeElementUnique(keyWordList):
    tmeSet = set(keyWordList)
    uniqueList = list(tmeSet)
    return uniqueList

# 得到依點擊高低排序的 time-keyword pair


def getTime_KeyWord(biggestCountIndex, lecture_data):
    # 一個sequence是幾秒
    timeSegment = 40
    # 最後的關鍵字列表
    time_keyword = {}
    for rank in range(5):  # 取前5高的點擊，可設定抓更多的數量
        index_count = biggestCountIndex[rank]
        startTime = index_count[0]*timeSegment
        endTime = (index_count[0]+1)*timeSegment
        timePair = (startTime, endTime)  # make it tuple
        keyWordTmp = []
        for timeTuple in time_keyList:
            keyWordTimeTmp = get_key_word(startTime,
                                          endTime,
                                          timeTuple[0],
                                          timeTuple[1])
            if keyWordTimeTmp ! = None:
                keyWordTmp.extend(time_keyList[keyWordTimeTmp])
        time_keyword[index_count[1]] = makeElementUnique(keyWordTmp)
        detail_data.append([lecture_data['vname'],
                            lecture_data['vhash'],
                            startTime,
                            index_count[1],
                            time_keyword[index_count[1]]])
    return time_keyword


def output_fill(time_keyword):
    tmp_list = []
    for counts in time_keyword.keys():
        for words in time_keyword[counts]:
            tmp_list.append([counts, words])
    return tmp_list


def output_json_file():
    word_list = {}
    for data in detail_data:
        for each_word in data[4]:
            #data[0] : video name ; data[1] : video url ; data[2] : start time;
            #data[3] : count ; data[4] : key word
            count_group = {}
            if each_word in word_list:
                word_list[each_word]["vid_list"].append([data[0],
                                                         data[1],
                                                         data[2],
                                                         data[3]])
                word_list[each_word]["total_count"] += data[3]
                  # count_group["vid_list"].append([data[0],data[1]])
            else:
                time_group = []
                time_group.append([data[0], data[1], data[2], data[3]])
                count_group["vid_list"] = time_group
                count_group["total_count"] = data[3]
                word_list[each_word] = count_group

    word_list_order = {}
    for k_w in word_list.keys():
        word_list_order[k_w] = word_list[k_w]["total_count"]

    sorted_count = sorted(word_list_order.items(), key=operator.itemgetter(1))

    num = 1
    for i in sorted_count:
        word_list[i[0]]["order"] = num/len(sorted_count)
        num += 1
    return word_list

# create weekdir in resultdir if not exists
# week_dirs = os.listdir(keyword_dir)
# for dirName in week_dirs:LAN 1000 eng

#get sharecourse video name and url
sc_course = requests.get('http://104.155.227.109:8080/api/v1/getVideoHash')
course_json = sc_course.json()

weekList = os.listdir(subtitle_dir)
weekly = {}
for week in weekList:
    weekDir = subtitle_dir+'/'+week
    # create_dir_ifNotExist(result_dir+'/'+week)
    # create week dir in ../hot_word/
    lectureVideoList = os.listdir(weekDir)
    result_file = result_dir+'/'+week+'.csv'
    detail_data = []  # detail data every week
    week_data = course_json[int(week)]  # the video name and url every week
    # print(week_data)
    # out = []
    # out.append(['size','text'])
    for lectureVideo in lectureVideoList:
        keyword_file = subtitle_dir+'/'+week+'/'+lectureVideo
        fileName = lectureVideo.split('.')[0]
        timeline_file = timeLine_dir+'/'+week+'/'+fileName+'.csv'
        # the lecture video name and url
        lecture_data = week_data[int(fileName)]
        # print(lecture_data)
        # store keyword list to time_keyword = {}
        with open(keyword_file, 'r') as f:
            time_keyList = {}
            lines = f.readlines()
            for line in lines:
                timeInTuple = eval(line.split(':')[0])  # make time to tuple
                keyList = eval(line.split(':')[1])  # make keyword to list
                time_keyList[timeInTuple] = keyList
        try:
            # store timeline to %timeList %countList 2 list separately
            with open(timeline_file, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # skip title
                timeList = []
                countList = []
                for line in reader:
                    timeList.append(line[0])
                    countList.append(line[1])

            # get biggest count index
            topRankedCount = return_big_index_list(countList)
            # 取前5高的點擊，可設定抓更多的數量
            time_keyword = getTime_KeyWord(topRankedCount, lecture_data)

        except IOError:
            print('no such file')
            pass

    word_list = output_json_file()

    week_name = int(week)
    with open('../hot_word/' + str(week_name) + '.txt', 'w') as outfile:
        json.dump(word_list, outfile, ensure_ascii=False)

    weekly[int(week)] = word_list

with open('../hot_word/tagcloud.txt', 'w') as outfile:
    json.dump(weekly, outfile, ensure_ascii=False)
