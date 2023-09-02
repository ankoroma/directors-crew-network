from analysis_utils import PrintTopN, Plot_Histogram
import networkx as nx
import numpy as np
from metric import Apply_Metric
from operator import itemgetter

# Raw data / summary statistics
def Describe_Raw(data, graph, network_file):
    """ Returns a dictionary of descriptive statistics"""
    dir_attributes = Apply_Metric(network_file)[2]
    total_movies = 0
    for attribute_dict in dir_attributes.values():
        total_movies += attribute_dict['num_movies']
    num_directors = len(data)
    avg_movies = total_movies/num_directors
    num_nodes = graph.number_of_nodes()
    num_crew = num_nodes - num_directors
    sex_counts = data['Sex'].value_counts()
    ethnicity_counts = data['Ethnicity_Race'].value_counts()
    num_renowned = sum(data['Labels'] == 'H')
    num_queer = sum(data['Labels'] == 'Q')
    renowned = data[data['Labels']=='H']
    renowned_eth_counts = renowned['Ethnicity_Race'].value_counts()
    stats = {'num_directors':num_directors, 'avg_movies':avg_movies, 'num_nodes':num_nodes, 
             'total_movies':total_movies, 'sex_counts':sex_counts.to_string(), 
             'ethnicity_counts':ethnicity_counts.to_string(), 'renowned_eth_counts':renowned_eth_counts.to_string(),
             'num_crew':num_crew, 'num_renowned':num_renowned, 'num_queer':num_queer}
    return stats

# Network characteristics
def Analyze_Network(graph, directors):
    """Returns a dictionary of network characteristic statistics"""
    num_edges = graph.number_of_edges()
    connected = nx.is_connected(graph)
    dir_triangles = nx.triangles(graph)
    num_triangles = int(sum(dir_triangles.values())/3)
    cluster_coeffs = nx.clustering(graph,nodes=directors)
    avg_clustering = np.mean(list(cluster_coeffs.values()))
    max_clustering_idx = np.argmax(list(cluster_coeffs.values()))
    max_clustering_key = list(cluster_coeffs.keys())[max_clustering_idx]
    max_clustering = {max_clustering_key:cluster_coeffs[max_clustering_key]}
    density = nx.density(graph)
    assortativity = nx.degree_assortativity_coefficient(graph, weight='avg_dir_homog', nodes=directors)
    stats = {'connected':connected, 'num_edges':num_edges, 'num_triangles':num_triangles, 
             'avg_clustering':avg_clustering, 'density':density, 'assortativity':assortativity,
             'max_clustering':max_clustering, 'cluster_coeffs':cluster_coeffs}
    return stats

# Important nodes
def Analyze_Hubs(graph, directors):
    """Returns a dictionary of various node statistics"""
    crew = [name for name in graph.nodes() if name not in directors]
    dir_degree_rankings1 = sorted(graph.degree(nbunch= directors, weight ='crew_homog'), key=itemgetter(1), reverse=True)
    dir_degree_rankings2 = sorted(graph.degree(nbunch= directors), key=itemgetter(1), reverse=True)
    crew_degree_rankings1 = sorted(graph.degree(nbunch=crew,weight='crew_homog'), key=itemgetter(1), reverse=True)
    crew_degree_rankings2 = sorted(graph.degree(nbunch=crew), key=itemgetter(1), reverse=True)
    avg_dir_degree1 = np.mean([ranking[1] for ranking in dir_degree_rankings1])
    avg_dir_degree2 = np.mean([ranking[1] for ranking in dir_degree_rankings2])
    all_betweenness = nx.betweenness_centrality_subset(graph, directors, graph.nodes()) 
    dir_betweenness = {}
    for name, val in all_betweenness.items():
        if name in directors:
            dir_betweenness[name] = val
    betw_ranking = sorted(dir_betweenness.items(), key=lambda x:x[1], reverse=True) 
    avg_betweenness = np.mean([ranking[1] for ranking in betw_ranking])
    stats = {'dir_degree_rankings1': dir_degree_rankings1, 'dir_degree_rankings2': dir_degree_rankings2,
             'crew_degree_rankings1':crew_degree_rankings1, 'crew_degree_rankings2': crew_degree_rankings2,
             'avg_dir_degree1':avg_dir_degree1, 'avg_dir_degree2':avg_dir_degree2, 'all_betweenness':all_betweenness, 
             'dir_betweenness':dir_betweenness, 'ranking':betw_ranking, 'avg_betweenness':avg_betweenness}
    return stats

def Get_All_Stats(raw_data, network_file, graph, directors):
    """Run all analysis functions and retrieve the respective stats"""
    raw = Describe_Raw(raw_data, graph, network_file)
    net = Analyze_Network(graph,directors)
    hubs = Analyze_Hubs(graph, directors)
    return raw, net, hubs


def Print_Summary(raw_stats=False, net_stats=False, hub_stats=False):
    """Prints a summary of the input"""
    if raw_stats:
        print('\nData Composition Analysis:\n')
        print(f'The data is composed of {raw_stats["num_directors"]} directors and {raw_stats["num_crew"]} crew members for a total of {raw_stats["num_nodes"]} nodes\n')
        print(f'The average number of movies for a director is {round(raw_stats["avg_movies"],2)} for a total of {raw_stats["total_movies"]}')
        print(f'Gender Distribution:\n{raw_stats["sex_counts"]}\n')
        print(f'Ethnicity Distribution:\n{raw_stats["ethnicity_counts"]}\n')
        print(f'There are {raw_stats["num_renowned"]} directors designated as "renowned"')
        print(f'Renowned Ethnicity Distribution:\n{raw_stats["renowned_eth_counts"]}')
        print(f'There are {raw_stats["num_queer"]} LGBTQ+ directors\n')
    if net_stats:
        print('\nSmall Worlds Analysis:')
        print(f'Connected? {"Yes" if net_stats["connected"] else "No"}')
        print(f'Number of edges: {net_stats["num_edges"]}')
        print("\n Clustering:")
        root_coeffs = np.sqrt(list(net_stats["cluster_coeffs"].values()))
        Plot_Histogram(root_coeffs, 'Directors Clustering Coefficient', 'Root Clustering Coefficient')
        print(f'Number of triangles: {net_stats["num_triangles"]}')
        print(f'Mean Clustering Coefficient: {net_stats["avg_clustering"]}')
        print(f'Max Clustering Coefficient: {net_stats["max_clustering"]}')
        print(f'Density/Sparcity: {net_stats["density"]}')
        print(f'Assortativity Coefficient: {net_stats["assortativity"]}\n')
    if hub_stats:
        print('\nHubs Analysis:\n')
        print('Top 5 Directors- Raw Degree:')
        PrintTopN(hub_stats['dir_degree_rankings2'], 5)
        print(f'\nAverage Director Raw Degree: {hub_stats["avg_dir_degree2"]}')
        print('\nTop 5 Directors- Weighted Degree:')
        PrintTopN(hub_stats['dir_degree_rankings1'], 5)
        print(f'\nAverage Director Weighted Degree: {hub_stats["avg_dir_degree1"]}')
        print('\nTop 5 Crew Members- Raw Degree:')
        PrintTopN(hub_stats['crew_degree_rankings2'], 5)
        print('\nTop 5 Crew Members- Weighted Degree:')
        PrintTopN(hub_stats['dir_degree_rankings1'], 5)
        print('\n Betweenness:')
        Plot_Histogram(hub_stats["dir_betweenness"].values(), 'Directors Betweenness', 'Betweenness Score')
        print(f'\nTop 10 Directors- Betweenness Centrality:')
        PrintTopN(hub_stats["ranking"],101)
        print(f'\nAverage Betweenness Centrality: {hub_stats["avg_betweenness"]}')
    return


# Homogeneity Statistics
def Group_By_Role(role_homogeneity):
    """Returns a dictionary of average homogeneity score for each role across directors"""
    homog_by_role = {}
    for director in role_homogeneity.keys():
        for role in role_homogeneity[director].keys():
            score = role_homogeneity[director][role]
            if role not in homog_by_role.keys():
                homog_by_role[role] = [score]
            else:
                homog_by_role[role].append(score)
    return homog_by_role

def Group_By_Attribute(dir_homogeneity, dir_attributes):
    """Returns a dictionary of average homogeneity score for each role across attributes"""
    groups = {'renowned':[], 'minority':[], 'other':[]}
    for director, homog in dir_homogeneity.items():
        other = dir_attributes[director]['other']
        gender = dir_attributes[director]['gender']
        ethn = dir_attributes[director]['ethnicity']
        renowned = other == 'H'
        minority = gender == 'F' or ethn != 'W' or other == 'Q'
        if renowned:
            groups['renowned'].append(homog)
        elif minority:
            groups['minority'].append(homog)
        else:
            groups['other'].append(homog)
    return groups