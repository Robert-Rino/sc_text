# -*- coding: utf-8 -*-
# run this program -----
# > python precessing.py <vid>
import csv
import sys
import dateutil.parser
import datetime
import os,sys

def create_dir_ifNotExist(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

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
# ============================================================
# preprocessing_file(): input file path this function will return a list
# for output processed chapter viewing file in csv format
def preprocessing_file(file_path):
    # print file_path
    outHash = {}
    with open(file_path,'r') as f_in:
        lines = csv.reader(f_in)
        next(lines)
        secondLine = lines.next()
        totalTime = secondLine[3]
    totalSeq = int(round(float(totalTime)/float(timeSequence)))#count sequence num
    with open(file_path,'r') as f_in:
        out = []
        f_in.next()# reaterminald start from 2nd line
        for line in csv.reader(f_in):#iterate over all line of original file
            endTime = line[2]
            ratio = round(float(endTime))/timeSequence
            remain = round(float(endTime))%timeSequence
            if remain > 0:
                ratio = round(ratio+1)
            if outHash.get(ratio) == None:
                outHash[ratio] = 1
            else:
                outHash[ratio] += 1
        out.append(['time','count'])
        for i in range(totalSeq+2):
            if outHash.get(i) == None:
                out.append([timeSequence*i,0])
            else:
                out.append([timeSequence*i,outHash[i]])
        return out

#=========================
#==function define above==
#=========================

#input file directory path
weeks_dir_path_in = '../to_weeks/'
#output file directory path
weeks_dir_path_out = '../to_weeks_preprocessed/'

# outfile_dir =inFileName+'precessed.csv'
timeSequence = 40#every 5 second is a sequence
totalTime = 0
outHash = {}

dir_list = os.listdir(weeks_dir_path_in)
dirList_weeks = []
for dir_name in dir_list:
    current_dir = weeks_dir_path_in+dir_name # current_dir = to_weeks/1
    output_dir = weeks_dir_path_out+dir_name
    create_dir_ifNotExist(output_dir)
    video_data_file_list = os.listdir(current_dir)
    for file in video_data_file_list:
        #to_weeks/1/1-1234.csv
        complete_input_file_path = current_dir+'/'+file
        complete_output_file_path = weeks_dir_path_out+dir_name+'/'+file
        # print complete_input_file_path
        # print complete_output_file_path
        try:
            out = preprocessing_file(complete_input_file_path)
            # print 'hello'
            with open(complete_output_file_path,'w') as f:
                w = csv.writer(f)
                w.writerows(out)
        except StopIteration:
            print '=====%s/%s no content=====' %(dir_name,file)
            pass
