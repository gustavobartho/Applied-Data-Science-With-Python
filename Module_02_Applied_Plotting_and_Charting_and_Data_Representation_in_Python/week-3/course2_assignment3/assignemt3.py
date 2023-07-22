# Use the following data for this assignment:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(12345)

df = pd.DataFrame([
    np.random.normal(32000,200000,3650), 
    np.random.normal(43000,100000,3650), 
    np.random.normal(43500,140000,3650), 
    np.random.normal(48000,70000,3650),
], index=[1992,1993,1994,1995])


#Your Code Here

def get_bar_color(floor, ceil, y_value):
    if floor <= y_value <= ceil: return "white"
    if ceil < y_value: return "red"
    return "blue"

def plot_easiest_option(df, y_value):

    # gets the data -------------------------------

    # get right mean and std
    df['mean'] = df.mean(axis=1)
    df['std'] = df.std(axis=1)

    # unbiased standard error of the mean over requested axis
    df['sem'] = df.sem(axis=1)
    # gets the confidence interval floor
    df['conf floor'] = df['mean'] - df['sem'] * 4
    # gets the confidence interval ceil
    df['conf ceil'] = df['mean'] + df['sem'] * 4

    # gets the error 
    df['yerr'] = df['sem'] * 4 

    # creates the plot -----------------------------

    # get the Axis object
    ax = plt.gca()

    # iterate through each 
    for index in df.index:
        row = df.loc[index]
        plt.bar(str(index), row['mean'], color=get_bar_color(row['conf floor'], row['conf ceil'], y_value), align='center', edgecolor="black", yerr=row['yerr'], capsize=10,  alpha=0.4)

    plt.xlabel('Year', fontsize=13, labelpad=10)
    ax.spines[['top', 'right']].set_visible(False)
    plt.axhline(y=y_value, color='gray', linestyle='-')

    plt.savefig('assignment3.png', bbox_inches = 'tight')


plot_easiest_option(df, 35000)