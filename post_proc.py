#!/usr/bin/env python3


import datetime as dt
import random

def post_processing(results_file_name):  # ratios
    
    with open(results_file_name, 'r') as outfile:
        results = [line.strip().split('\t') for line in outfile]
    
    results = results[1:] # stripping header
    results = [ [int(line[0]), dt.strptime(line[1]), dt.strptime(line[2]), float(line[3]), float(line[4]),
                 bool(line[5]),line[6] ] for line in results]
    print(results)

post_processing('res_8207385cffc393d.txt')
