# -*- coding: utf-8 -*-
# run this program -----
# > python precessing.py <vid>
import csv
import sys
import dateutil.parser
import datetime
import os,sys
def iso_to_hash(iso_string):
    date_hash={}
    t = dateutil.parser.parse(iso_string)
    # date_hash['year'] = date.split('-')[0]
    # date_hash['month'] = date.split('-')[1]
    # date_hash['day'] = date.split('-')[2]
    # date_hash['hour'] = time.split(':')[0]
    # date_hash['min'] = time.split(':')[1]
    # date_hash['second'] = time.split(':')[2]
    print iso_string
    print t.year
    print t.month
    print t.day
    print t.hour
    print t.minute
    print t.second
    print t.microsecond
    # return date_hash

# print sys.argv[1]
# fileType = '.csv'
# inFileName = sys.argv[1]
# infile_dir=inFileName+fileType

#input file directory path
weeks_dir_path_in = '../to_weeks/'
#output file directory path
weeks_dir_path_out = '../to_weeks/filtered/'

infile_dir = '../to_weeks/4/1-13695.csv'
# outfile_dir =inFileName+'precessed.csv'
outfile_dir = '../1-13695prepcessed.csv'
timeSequence = 5#every 5 second is a sequence
totalTime = 0
outHash = {}

dir_list = os.listdir(weeks_dir_path_in)
dirList_weeks = []
for dir_name in dir_list:
    name_tmp = weeks_dir_path_in+dir_name
    dirList_weeks.append(name_tmp)
# print dirList_weeks
for dir in dirList_weeks:
    # to_weeks/xxx
    current_dir = dir
    print current_dir
    video_data_file_list = os.listdir(current_dir)
    video_data_file_path_list = []
    for file in video_data_file_list:
        #to_weeks/week-xxx/number-ooo
        video_data_file_path_list.append(current_dir+'/'+file)
    # print video_data_file_path_list
        # for file in video_data_file_path_list:
        #     print file









with open(infile_dir,'r') as f_in:
    lines = csv.reader(f_in)
    #skip title
    lines.next()
    secondLine = lines.next()
    totalTime = secondLine[3]
#count sequence num
totalSeq = int(round(float(totalTime)/float(timeSequence)))
#create another reader object
f_in = open(infile_dir,'r')
out = []
# read start from 2nd line
f_in.next()
#iterate over all line of original file
for line in csv.reader(f_in):
    #seek action video_end_time
    endTime = line[2]
    ratio = round(float(endTime))/timeSequence
    remain = round(float(endTime))%timeSequence
    # print 'ratio is %s remain is %s '%(remain,ratio)
    # print 'endTime is %s , ratio is %s , remain is %s' %(endTime,ratio,remain)
    if remain > 0:
        ratio = round(ratio)
    if outHash.get(ratio) == None:
        outHash[ratio] = 1
    else:
        outHash[ratio] += 1
    # print 'endTime is %s , ratio is %s , remain is %s' %(endTime,ratio,remain)
out.append(['time','count'])
for i in range(totalSeq+2):
    if outHash.get(i) == None:
        out.append([timeSequence*i,0])
    else:
        out.append([timeSequence*i,outHash[i]])
    # print outHash[index]
    # print out
#create a file object for write
# f_out = open(outfile_dir,'w')
# w = csv.writer(f_out)
# w.writerows(out)
f_in.close()
# f_out.close()
