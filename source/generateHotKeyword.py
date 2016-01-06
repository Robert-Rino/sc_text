#-*- coding=utf-8 -*-
import csv,sys,os
import datetime

hotTime_dir = '../to_weeks_preprocessed'
keyword_dir = '../it_done'
result_dir  = '../hot_word'

# 輸入countList
# 會回傳依照關鍵次出現次數降冪排列的對應(index,count)的list
def return_big_index_list(timelineCount):
    tmp = []
    for index,count in enumerate(timelineCount):
        tmp.append((index,int(count)))
    # print tmp
    sorted_index_list = sorted(tmp , key = lambda x :x[1],reverse=True)
    # print sorted_index_list
    return sorted_index_list

def get_key_word(scale_start,scale_end,video_start,video_end):
    if video_end >= scale_start:
        if scale_end >= video_start:
            return video_start,video_end

def create_dir_ifNotExist(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def makeElementUnique(keyWordList):
    tmeSet = set(keyWordList)
    uniqueList = list(tmeSet)
    return uniqueList
# create weekdir in resultdir if not exists
# week_dirs = os.listdir(keyword_dir)
# for dirName in week_dirs:
#     create_dir_ifNotExist(result_dir+'/'+dirName)
#     keyword_files = keyword_dir+'/'+dirName
#     for fileName in os.listdir(keyword_files):
#         print dirName+'/'+fileName

keyword_file = '../it_done/3/0.txt'
timeline_file = '../to_weeks_preprocessed/3/0-13680.csv'

# store keyword list to %time_keyList
with open(keyword_file,'r') as f :
    time_keyList = {}
    lines = f.readlines()
    for line in lines:
        timeInTuple = eval(line.split(':')[0]) # make time to tuple
        keyList = eval(line.split(':')[1])  # make keyword to list
        time_keyList[timeInTuple] = keyList
    # print time_keyList

# store timeline to %timeList %countList 2 list separately
with open(timeline_file,'r') as f:
    reader = csv.reader(f)
    next(reader) # skip title
    timeList = []
    countList = []
    for line in reader:
        timeList.append(line[0])
        countList.append(line[1])

# get biggest count index
topRankedCount = return_big_index_list(countList)
# 一個sequence是幾秒
timeSegment = 5
# 最後的關鍵字列表
time_keyword = {}

# 取前5高的點擊，可設定抓更多的數量
for rank in range(5):
    index_count = topRankedCount[rank]
    startTime = index_count[0]*timeSegment
    endTime = (index_count[0]+1)*timeSegment
    timePair = (startTime,endTime) #make it tuple
    keyWordTmp = []
    for timeTuple in time_keyList:
        # print 'start is :%s , end is %s' %(timeTuple[0],timeTuple[1])
        keyWordTimeTmp = get_key_word(startTime,endTime,timeTuple[0],timeTuple[1])
        if keyWordTimeTmp != None:
            keyWordTmp.extend(time_keyList[keyWordTimeTmp])
    time_keyword[timePair] = makeElementUnique(keyWordTmp)
print(time_keyword)
