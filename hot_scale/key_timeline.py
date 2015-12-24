# -*- coding:utf-8 -*-
# {'week':
#   {
#    order1:
#        {
#       times : [time1,time2,time3...]
#       count : [count1,count2,count3...]
#        }
#   }
#
# }
import csv,os,sys
import numpy as np
def return_big_index_list(timelineCount):
    tmp = []
    for index,count in enumerate(timelineCount):
        tmp.append((index,int(count)))
    # print tmp
    sorted_index_list = sorted(tmp , key = lambda x :x[1],reverse=True)
    # print sorted_index_list
    return sorted_index_list

path = './' #current dir
dirs = os.listdir(path)
inPath = path+dirs[0]
# sorted(dirs)
for key,name in enumerate(dirs):
    if name == 'key_timeline.py':
        del(dirs[key])

# with open(inPath,'r') as f:
#     reader = csv.reader(f)
#     next(reader)#skip title
#     timeList = []
#     countList = []
#     for line in reader:
#         timeList.append(line[0])
#         countList.append(line[1])
#     indexList = return_big_index_list(countList)
#     returnTimeList = []
#     returnCountList = []
#     for index_count in indexList[:5]:
#         returnTimeList.append(timeList[index_count[0]])
#         returnCountList.append(countList[index_count[0]])


week_order_timeList={}
week_order_timeList[3] = {}#future work all week data currently only week3
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

# print(week_order_timeList[3][2]['time'])
# print week_order_timeList[3][2]['count']
