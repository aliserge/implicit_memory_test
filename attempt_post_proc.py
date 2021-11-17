#!/usr/bin/env python3

import statistics as stats

def post_processing(results_file_name):  # ratios
    
    btn_one_ratio = []
    btn_two_ratio = []
    btn_three_ratio = []
    btn_four_ratio = []
    
    with open(results_file_name, 'r') as outfile:
        results = [line.strip().split('\t') for line in outfile]
    
    outfile = open(results_file_name+'.proc.tsv', 'w')
    outfile.write('Btn\tStart\tStop\tNormDelta\tRatio\tCorrectness\tSequence\tRatioToPrevControl\n')
    
    results = results[3:] # stripping header
    
    
    results = [ [int(line[0]), # Key - results[0]
                 line[1].split(' ')[1].split(':'), # Start time - results[1] 
                 line[2].split(' ')[1].split(':'), # Stop time - results[2]
                 float(line[3]), # Delta - results[3]
                 float(line[4]), # Ratio - results[4]
                 line[5]=="True", #Correctness - results[5] 
                 line[6], #Sequence - results[6] 
                 ] for line in results if not line[0].startswith('Err')]
    # TODO: Thing, how to deal with error keys. For now, just filreting it out
    
    # Transforming to absolute time
    for line in results:
        line[1][-1] = line[1][-1].split('.')
        line[2][-1] = line[2][-1].split('.')
        
        while True:
            if line[1][0] == line[2][0]:
                del line[1][0]
                del line[2][0]
            else:
                break
        line[1] = flat_list(line[1])
        line[2] = flat_list(line[2])

        if len(line[1]) == 3:
            line[1] = [int(line[1][-3]) * 60 * 1000 + int(line[1][-2]) * 1000 + int(line[1][-1])]
            line[2] = [int(line[2][-3]) * 60 * 1000 + int(line[2][-2]) * 1000 + int(line[2][-1])]
        else:
            line[1] = [int(line[1][-2]) * 1000 + int(line[1][-1])]
            line[2] = [int(line[2][-2]) * 1000 + int(line[2][-1])]
        results[results.index(line)] = flat_list(line)


    # Calculating means for all buttons
    btn_1_norm = []
    btn_2_norm = []
    btn_3_norm = []
    btn_4_norm = []
    
    for lst in results:
        if lst[0] == 1:
            btn_1_norm.append(lst[3])
        elif lst[0] == 2:
            btn_2_norm.append(lst[3])
        elif lst[0] == 3:
            btn_3_norm.append(lst[3])
        else:
            btn_4_norm.append(lst[3])
    
    btn_1_mean = mean_std(btn_1_norm)
    btn_2_mean = mean_std(btn_2_norm)
    btn_3_mean = mean_std(btn_3_norm)
    btn_4_mean = mean_std(btn_4_norm)
    
    # Normalizing delta values on mean
    for lst in results:
        if lst[0] == 1:
            lst[3] = lst[3] / btn_1_mean
        elif lst[0] == 2:
            lst[3] = lst[3] / btn_2_mean
        elif lst[0] == 3:
            lst[3] = lst[3] / btn_3_mean
        else:
            lst[3] = lst[3] / btn_4_mean
            
    for i,lst in enumerate(results):
        if lst[6] == "A":
            #print("finding prev_b")
            i_B = find_prev_B(results, i)
            if i_B == None:
                lst.append("None")
                continue
            else:
                lst.append(lst[3] / results[i_B][3])
            
    for lst in results:
        outfile.write('\t'.join((str(el) for el in lst)) + '\n')
    
            
    outfile.close()

def find_prev_B(results, i):
    while i >= 0:
        if results[i][6] == "B":
            return i
        else:
            i -= 1
    return None
    
def mean_std(array):
    return stats.mean(array)
    
def flat_list(array):
    new_array = []
    for element in array:
        if isinstance(element, list):
            new_array += flat_list(element)
        else:
            new_array.append(element)
    return new_array
    
if __name__ == "__main__":
    import sys
    post_processing(sys.argv[1])
    
