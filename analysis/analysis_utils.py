import pandas as pd
import numpy as np
import gzip
import matplotlib.pyplot as plt
import networkx as nx
from math import ceil


def ProcessData(file):
    """Cleans the data frame and adds a full name column"""
    data = pd.read_csv(file)
    data["name"] = data['FirstName'].str.rstrip().str.lstrip() +" "+ data["LastName"].str.rstrip().str.lstrip()
    data["name"] = data['FirstName'].str.rstrip().str.lstrip() +" "+ data["LastName"].str.rstrip().str.lstrip()
    directors = data["name"].to_list()
    return data, directors

def GetGraph(graph_file):
    """Returns networkx graph"""
    graph = nx.read_graphml(graph_file)
    return graph

def Normalize_Roles(movies):
    """Groups similar roles into departments"""
    for movie in range(len(movies)):
        crew = movies[movie]['crew']
        for role in crew:
            if 'Writing' in role[0]:
                role[0] = 'Writing Credits'
    return movies

def Print_Ranking(dir_homogeneity, role_homogeneity):
    """Prints a formatted ranking of directors with their most homogeneous departments"""
    role_copy = role_homogeneity.copy()
    ranking = sorted(dir_homogeneity.items(), key=lambda x:x[1], reverse=True)
    for director, roles in role_copy.items():
        sorted_roles = sorted(roles.items(), key=lambda x:x[1], reverse=True)
        role_copy[director] = sorted_roles
    print(f'\n***Ranking of Directors by Homogeneity Score***\n.\n.\n.\n')
    print(f"Rank \t Name \t\t    AHS \t\t\t Top 3 Roles")
    for i, director in enumerate(ranking):
        role_names = ' - '.join([i[0] for i in role_copy[director[0]]])
        top3_roles = ' - '.join(role_names.split(' - ')[:3])
        print(f'{i+1}.   {director[0]}   {director[1]}    {top3_roles}\n')
    return

def load_director(file):
    """Load data iteratively
       Must be a .jsonl.gz file""" 
    with gzip.open(file) as movie_creds:
        for director in movie_creds:
            yield director
    
def Group_Means(grouped_directors):
    """Returns the mean value for each group in the input dictionary"""
    copy = grouped_directors.copy()
    for key in copy.keys():
        copy[key] = np.mean(copy[key])
    return copy

def Plot_Histograms(grouped_directors):
    """Plots seperate histograms for each group in the input dictionary"""
    lengths = [len(value) for value in grouped_directors.values()]
    if np.sqrt(max(lengths)) > min(lengths):
        bins = int(min(lengths))
    else:
        bins = ceil(np.sqrt(max(lengths)))
    for key in grouped_directors.keys():
        plt.plot(figsize=(4,4))
        plt.hist(grouped_directors[key], rwidth=0.98, bins=bins)
        ax = plt.gca()
        plt.tick_params(labelsize = 14)
        plt.grid(axis='y', color='white', alpha = 0.5)
        plt.xlabel('Homogeneity Score', fontsize=14, labelpad=10)
        plt.ylabel('Count', fontsize=14, labelpad=10)
        [ax.spines[i].set_visible(False) for i in ax.spines]
        plt.title(key.title(), fontsize=16)
        plt.savefig(f'plots/{"".join(key.title().split())}.png', bbox_inches='tight')
        plt.show()
    return

def Plot_Subplots(grouped_directors, name=''):
    """Returns a figure with subplots for each group"""
    if len(grouped_directors.keys()) <= 4:
        rows, cols = 1, len(grouped_directors.keys())
    else:
        cols = 4
        rows = ceil(len(grouped_directors.keys())/4)
    lengths = [len(value) for value in grouped_directors.values()]
    if np.sqrt(max(lengths)) > min(lengths):
        bins = int(min(lengths))
    else:
        bins = ceil(np.sqrt(max(lengths)))
    row = 0
    if rows > 1:
        fig, axes = plt.subplots(rows, cols, figsize=(25,25))
        for col, key in enumerate(grouped_directors.keys()):
            if col > 0 and col%4 == 0:
                row += 1
            column = col%4
            axes[row,column].hist(grouped_directors[key], rwidth=0.96, bins=bins)
            axes[row, column].set_title(key.title(), fontsize=25)
            [axes[row,column].spines[j].set_visible(False) for j in axes[row,column].spines]
            axes[row,column].grid(axis='y', color='white', alpha = 0.5)
        column+=1
        while column < cols:
            fig.delaxes(axes[row][column])
            column += 1

    else:
        fig, axes = plt.subplots(rows, cols, figsize=(14,6))
        fig.supxlabel('Homogeneity Score', fontsize=14)
        fig.supylabel('Count', fontsize=14)
        for col, key in enumerate(grouped_directors.keys()):
            axes[col].hist(grouped_directors[key], rwidth=0.96, bins=bins)
            axes[col].set_title(key.title(), fontsize=15)
            [axes[col].spines[j].set_visible(False) for j in axes[col].spines]
            axes[col].grid(axis='y', color='white', alpha = 0.5)
    plt.savefig(f'plots/subplots{name}.png', bbox_inches='tight')
    plt.show()
    return

def Plot_Histogram(value_list, title, xlabel):
    """Plots a histogram of the input list"""
    length = len(value_list)
    bins = ceil(np.sqrt(length))
    plt.plot(figsize=(4,4))
    plt.hist(value_list, rwidth=0.98, bins=bins)
    ax = plt.gca()
    plt.tick_params(labelsize = 14)
    plt.grid(axis='y', color='white', alpha = 0.5)
    plt.xlabel(xlabel, fontsize=14, labelpad=10)
    plt.ylabel('Count', fontsize=14, labelpad=10)
    [ax.spines[i].set_visible(False) for i in ax.spines]
    plt.title(title, fontsize=16)
    plt.savefig(f'plots/{"".join(title.split())}.png', bbox_inches='tight')
    plt.show()
    return

def PrintTopN(rankings, n):
    """Prints a formatted top n ranking of the "rankings" input list"""
    for i, pair in enumerate(rankings[:n]):
        print(i+1, pair[0]+':', pair[1])
    return