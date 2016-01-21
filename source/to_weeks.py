# -*- coding: utf-8 -*-
import csv,os
#chapter_video_dir is dump from mysql v_chapter_video table
#format is
#cid,chid,chapter_order,content-order,vid,v_name
chapter_video_dir = '../video_file/v_chapter_video.csv'
#in_file_path is dumpform mongodb format is
#userId,videoStartTime,videoEndTime,videoTotalTime,videoId,time
in_file_path = '../video_file/video_record_12_7_filtered.csv'
# out_dir = './weeks_filtered/week3/'
out_path = '../to_weeks'

if not os.path.exists(out_path):
    os.makedirs(out_path)
title = []
weeks_vid={}
with open(chapter_video_dir,'r') as f:
    reader = csv.reader(f)
    next(reader)#skip title
    for line in reader:
        week = int(line[2])-1
        content_order = int(line[3])
        vid = int(line[4])
        order_vid = (content_order,vid)
        if weeks_vid.get(week) == None:
            weeks_vid[week] = [order_vid]
        else:
            weeks_vid[week].append(order_vid)

#sort vid by content_order every week
for week in weeks_vid:
    sorted(weeks_vid[week], key = lambda x : x[0])
#write week video to file
for week in weeks_vid:
    print week
    dir_path = out_path+'/'+str(week)
    #create week folder if not exists
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    vid_list = []
    for video in weeks_vid[week]:
        vid = video[1]
        vid_list.append(vid)
        for index,vid in enumerate(vid_list):
            # out_file_name = '/'+str(index)+'-'+str(vid)+'.csv'
            out_file_name = '/'+str(index)+'.csv'
            out_file_path = dir_path+out_file_name
            out = []
            # out.append(title)
            with open(in_file_path,'r') as f :
                reader = csv.reader(f)
                next(reader)#skip the first line
                for line in reader:
                    if int(line[4]) == vid:
                        out.append(line)
            with open(out_file_path,'w') as f:
                w = csv.writer(f)
                w.writerows(out)


# with open(in_file_path,'r') as f:#get title
#     reader = csv.reader(f)
#     row = next(reader)
#     title.append(row)
# print title
# for vid in week3:
#     out_file_path = out_dir+str(vid)+'.csv'
#     out = []
#     out.append(title)
#     with open(in_file_path,'r') as f :
#         reader = csv.reader(f)
#         next(reader)#skip the first line
#         for line in reader:
#             if int(line[4]) == vid:
#                 out.append(line)
#     with open(out_file_path,'w') as f:
#         w = csv.writer(f)
#         w.writerows(out)
