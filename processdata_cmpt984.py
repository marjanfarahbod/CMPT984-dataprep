import sys
import pandas as pd
import numpy as np
from statistics import mean

def read_include(file): 
    '''to parse the pilotregion file '''
    with open(file, 'r') as inc_file:
        lines = inc_file.readlines()
        
    include = []
    for l in lines:
        splitted = l.split('\t')[:-1]
        # splitted[-1] = splitted[-1].replace('\n', '')
        include.append(splitted)
    
    return pd.DataFrame(include, columns=['chr', 'start', 'end'])

def read_bedgraph(bg_file): 
    '''to read the raw data'''

    df = []
    with open(bg_file, 'r') as bgf:
        lines = bgf.readlines()
    for i in range(len(lines)): 
        tl = lines[i].split('\t')
        tl[-1] = float(tl[-1].replace('\n', ''))
        df.append(tl)
    return pd.DataFrame(df, columns=['chr', 'start', 'end', 'signal'])

def initialize_bins(coords, res): 
    '''initializes empty bins according to the genome positions specified in the pilotregions file'''

    supercontig_in_progress = []
    for i in range(len(coords)):
        region_in_progress = list(coords.iloc[i,:])
        for j in range(int(region_in_progress[1]), int(region_in_progress[2]), res):

            if int(j + res) > int(region_in_progress[2]):
                supercontig_in_progress.append([region_in_progress[0], int(j), int(region_in_progress[2]) + int(res - (int(region_in_progress[2]) % res))])

            else: 
                supercontig_in_progress.append([region_in_progress[0], int(j), int(j + res)])

    return pd.DataFrame(supercontig_in_progress, columns=['chr', 'start', 'end'])

def save_empty_bg(df, newfile_name):
    with open(newfile_name, 'w') as wfile:
        for i in range(len(df)):
            wfile.write('{}\t{}\t{}\n'.format(
                df['chr'][i], df['start'][i], df['end'][i]))

def fill_bins(empty_bins, raw_data, M): 

    """This function assigns the signal value to each bin based on the corresponding 
    value in the raw data file. I used a "search margin" to prevent the function from 
    performing in O(n^2). M denotes search margin and limits the inner loop to M indices 
    only, starting from where the last bin was aligned with the raw data. The final signal 
    value of each bin is weighted by the length of alignment """

    empty_bins.insert(3, "signal", np.zeros(len(empty_bins)))#  [[]for x in range(len(empty_bins))])
    notfilled = 0
    c = 0 # denotes the center of search space
    for i in range(len(empty_bins)): # i denotes index of empty bin
        filledbool = False
        # define search space
        if i%100 == 0:
            print("filled {} bins. could not fill {} bins".format(i-notfilled, notfilled))
        
        if c < M:
            search_start_loc = 0
        else:
            search_start_loc = c - int(M/10)
    
        if c + M > len(raw_data):
            search_end_loc = len(raw_data)
        else:
            search_end_loc = c + M

        for j in range(search_start_loc, search_end_loc): # j denotes index of raw data

            if empty_bins.iloc[i, 0] == raw_data.iloc[j, 0]: # check chr match

                statement1 = bool(int(empty_bins.iloc[i,1]) <= int(raw_data.iloc[j, 1]) <= int(empty_bins.iloc[i,2]) )
                statement2 = bool(int(raw_data.iloc[j, 1]) <= int(empty_bins.iloc[i,1]) <= int(raw_data.iloc[j, 2]) )

                statement3 = bool(int(empty_bins.iloc[i,2]) < int(raw_data.iloc[j, 1])) # passed statement

                if statement1 or statement2:
                    bin_range = range(int(empty_bins.iloc[i,1]), int(empty_bins.iloc[i,2]))
                    signal_range = range(int(raw_data.iloc[j, 1]), int(raw_data.iloc[j, 2]))
                    
                    set_r1 = set(bin_range)
                    overlap = set_r1.intersection(signal_range)

                    if len(overlap) > 0:
                        filledbool = True
                        c = j # the center of search space changes to latest match index
                        bin_len = int(empty_bins.iloc[i, 2]) - int(empty_bins.iloc[i, 1])
                        empty_bins.iloc[i, 3] += float(raw_data.iloc[j, 3] * (len(overlap) / bin_len))
                
                elif statement3:
                    break

        if filledbool == False:
            notfilled +=1

    return empty_bins #filled now :))


def save_csv(binned_df, csv_name):
    binned_df.to_csv(csv_name)

if __name__== "__main__":

    """hint :
    sys.argv[1] = raw data file -> bedGraph/bed
    sys.argv[2] = M (seaching margin) -> int
    sys.argv[3] = output filename -> csv""" 

    df = initialize_bins(read_include('encodePilotRegions.hg19.bed'),100)
    # df = df.iloc[:1000, :]
    # save_empty_bg(df, 'binned_100bp_PilotRegions.bedGraph')
    raw_data = read_bedgraph(sys.argv[1]) 
    filled_df = fill_bins(df, raw_data, int(sys.argv[2]))

    save_csv(filled_df, sys.argv[3])

