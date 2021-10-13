import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt


def read_csv(filename): # input: binned track csv file
    return pd.read_csv(filename, index_col=False)

def asinh_transform(raw_signals): # input: an array of the signal values
    return(pd.DataFrame(np.arcsinh(np.array(raw_signals))))

def concat_tracks(coords_chr, coords_start, coords_end, dic_of_signal_arrays): # input: start_column, end_column, dic of signal_tracks
    columns = ['chr', 'start', 'end']
    list_of_signal_arrays= [coords_chr, coords_start, coords_end]
    for k, v in dic_of_signal_arrays.items():
        columns.append(k)
        list_of_signal_arrays.append(v)

    gathered = pd.concat(list_of_signal_arrays, axis=1)
    gathered.columns = columns
    return gathered


def multipanel_plot(filename):
    df = pd.read_csv(filename)
    do_not_include = ['Unnamed: 0', 'chr', 'start', 'end']
    df = df.drop(do_not_include, axis=1)

    fig, axs = plt.subplots(df.shape[1], sharex=True)

    for i in range(df.shape[1]):
        axs[i].plot(range(df.shape[0]), df[df.columns[i]])
        axs[i].set_title(df.columns[i])

    plt.show()

if __name__== "__main__":
    dic_of_signal_arrays = {}
    for i in range(2, len(sys.argv)-1):
        df = read_csv(sys.argv[i])

        if sys.argv[1] == "asinh":
            dic_of_signal_arrays[sys.argv[i].replace(".csv", "")] = asinh_transform(df['signal'])
        else:
            dic_of_signal_arrays[sys.argv[i].replace(".csv", "")] = df['signal']

    coords_chr = df['chr']
    coords_start = df['start']
    coords_end = df['end']

    gathered_df = concat_tracks(coords_chr, coords_start, coords_end, dic_of_signal_arrays)
    gathered_df.to_csv(sys.argv[-1])