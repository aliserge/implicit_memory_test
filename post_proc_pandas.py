import sys
import datetime as dt
import pandas as pd
import statistics

def post_processing(results_file_name):  
    # Loading CSV form a file
    df = pd.read_csv(results_file_name, delimiter='\t', skiprows=2)
    
    # Converting time values to datetime (Just in case)
    df["Start_time"]=pd.to_datetime(df["Start_time"])
    df["Stop_time"]=pd.to_datetime(df["Stop_time"])
    
    # Throwing away all incorrect elements
    df = df[df['Correctness'] == True]
    
    # Collecting Delta values by buttons
    rt_by_buttons = [ df.loc[df["Right_answer"]==i , "RT"] for i in range(1,5) ]
    # Calculating meen value buttons
    means_by_buttons = [statistics.mean(rt) for rt in rt_by_buttons]
    
    # Creating new columnd with normalized RT
    # The RT of chhosing correct answer (1,2,3,4) is normalizes to mean RT of choosing the same answer for whole experiment (bot A and B sequence)
    # Trying to get rid of user pressing biases (for example, user is right-handed and pressing right buttons faster than left ones
    df["Normalized_RT"] = 0
    for i in range(1,5): # i is a number of square 
        df.loc[df["Right_answer"]==i, "Normalized_RT"] = df["RT"] / means_by_buttons[i-1]
    
    df["ReactionRatio_to_latest_control"] = -1
    
    for i in range(len(df)):
        if df.iloc[i]["Sequence"] == "A":
            j = find_prev_B(df,i)
            if j>=0:
                ratio = df.iloc[i]["Normalized_RT"] / df.iloc[j]["Normalized_RT"]
                print(f"UpdatingRTRatio {ratio} for {i}")
                
                df.iat[i, df.columns.get_loc("ReactionRatio_to_latest_control")] = ratio
                #df.iloc[i][] = ratio
    
    print(df)
    
    df.to_csv(results_file_name+'.proc.tsv', sep='\t')

def find_prev_B(df,i):
    '''
    Finds in dataframe control button from B sequence with the same button
    Returns -1 is not found
    '''
    key = df.iloc[i]["Right_answer"]
    j=i
    while j>=0:
        j_key = df.iloc[j]["Right_answer"]
        if df.iloc[j]["Sequence"] == "B" and df.iloc[j]["Right_answer"] == key:
            break
        j -= 1
    return j
    
if __name__ == "__main__":
    post_processing(sys.argv[1])

