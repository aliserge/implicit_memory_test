import sys
from collections import namedtuple
import datetime as dt
#from functools import map
import statistics

User_Record = namedtuple('User_record',
                             'Sequence Position Right_answer User_answer Correctness Start_time Stop_time RT')

def print_list(l):
    for i in l:
        print(i)

def post_processing(results_file_name, skip=3):
    # Loading CSV form a file
    df = []
    with open(results_file_name) as results_file:
        for i in range(skip):
            results_file.readline()

        for t in results_file.readlines():
            (seq, pos, right_answer, user_answer, correctness, start_time, stop_time, RT) = t.strip().split('\t')
            pos = int(pos)
            right_answer = int(right_answer)
            user_answer = int (user_answer)
            correctness = correctness == "True"
            #start_time = dt.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            #stop_time = dt.datetime.strptime(stop_time, '%Y-%m-%d %H:%M:%S.%f')
            RT = float(RT)
            df.append({'Sequence':seq, 'Position':pos, 'Right_answer':right_answer,
                    'User_answer':user_answer, 'Correctness':correctness, 'Start_time':start_time,
                    'Stop_time':stop_time, 'RT':RT})

    # Filtering only test sequence
    df = list(filter(lambda x: x['Sequence'] in ["A","B"], df))

    # Throwing away all incorrect elements
    df = list(filter(lambda x: x['Correctness'] == True, df ))

    # Collecting Delta values by buttons
    answers = [list(filter(lambda x: x['Right_answer'] == i, df)) for i in range(1, 5)]
    rt_by_buttons = [list(map(lambda x: x['RT'], button)) for button in answers]

    # Calculating meen value buttons
    means_by_buttons = [statistics.mean(rt) for rt in rt_by_buttons]
    print(means_by_buttons)

    for i in range(len(df)):
        # Creating new column with normalized RT
        # The RT of correct answer (1,2,3,4) is normalizes to mean RT of choosing the same answer for whole experiment (both A and B sequence)
        # Trying to get rid of user pressing biases (for example, user is right-handed and pressing right buttons faster than left ones
        corresponding_mean = means_by_buttons[ df[i]['Right_answer'] - 1 ]
        df[i]["Normalized_RT"] = df[i]["RT"] / corresponding_mean
        df[i]["ReactionRatio_to_latest_control"] = -1

        if df[i]["Sequence"] == "A":
            j = find_prev_B(df, i)
            if j >= 0:
                ratio = df[i]["Normalized_RT"] / df[j]["Normalized_RT"]
                print(f"UpdatingRTRatio {ratio} for {i}")

                df[i]["ReactionRatio_to_latest_control"] = ratio

    with open(results_file_name+'.proc.tsv','w') as processed_file:
        processed_file.write('\t'.join(df[0].keys())+'\n')
        for measure in df:
            processed_file.write('\t'.join([str(s) for s in  measure.values()]) + '\n')



def find_prev_B(df, i):

    # Finds in dataframe control button from B sequence with the same button
    # Returns -1 is not found

    key = df[i]["Right_answer"]
    j = i
    while j >= 0:
        if df[j]["Sequence"] == "B" and df[j]["Right_answer"] == key:
            break
        j -= 1
    return j

    '''
    df.to_csv(, sep='\t')

'''
if __name__ == "__main__":
    post_processing(sys.argv[1])

