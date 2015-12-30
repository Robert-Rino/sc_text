# -*- coding: utf-8 -*-
# this is a script to filter pass-liked seek action
# if a person trigger seek 'action' in less than 2 second 
# then i treat that data a pass-data ,which is not the essential
# point of the video
import csv
import dateutil.parser
import datetime
def iso_to_dateobject(iso_string):#input string will return datetime.datetime-object
    t = dateutil.parser.parse(iso_string).replace(tzinfo=None)
    # 年：t.year
    # 月：t.month
    # 日：t.day
    # 時：t.hour
    # 分：t.minute
    # 秒：t.second
    # 毫秒：t.microsecond
    return t

def is_just_pass(early,late):#pass two datetime object return if duration is smaller than 2 sec
    duration = late-early
    d_day = duration.days
    d_sec = duration.seconds
    d_microsec = duration.microseconds
    if d_sec < 2:
        return True
    else:
        return False
out = []
uid_record = {}
raw_file = './video_record_12_7.csv'
out_dir = './video_record_12_7_filtered.csv'
with open(raw_file,'r') as f:
    reader = csv.reader(f)
    title_line = next(reader)
    out.append(title_line)
with open(raw_file,'r') as f:
    reader = csv.reader(f)
    next(reader)
    next(reader)
    for line in reader:
        uid = line[0]
        start_time = line[1]
        endTime = line[2]
        vid = line[4]
        time_stamp = line[5]
        if uid_record.get(uid) == None:
            uid_record[uid] = []
            uid_record[uid].append(line)
        else:
            uid_record[uid].append(line)

for uid in uid_record:
    record_list = uid_record[uid]
    for i in range(len(record_list)):
        next_index = i+1
        if next_index >= len(record_list):#if is the end of list , then break .
            break
        this_time_obj = iso_to_dateobject(record_list[i][5])
        next_time_obj = iso_to_dateobject(record_list[next_index][5])
        if is_just_pass(this_time_obj,next_time_obj) == False:
            out.append(record_list[i])
with open(out_dir,'w') as f:
    w = csv.writer(f)
    w.writerows(out)
# print out
