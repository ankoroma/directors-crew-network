import analysis
import analysis_utils as util
from metric import Apply_Metric
from pprint import pprint

# Run this file to display analysis

if __name__ == '__main__':
    run = input("""
    What analysis would you like to run?

    Options:
    - "all"
    - "summary"
    - "homog"
    """)
    network_file = "data/compressed_credits.jsonl.gz"
    raw_file = 'data/100_film_directors.csv'
    graph_file = 'data/final_dcnet.graphml'
    raw_data, directors = util.ProcessData(raw_file)
    graph = util.GetGraph(graph_file)

    if run == 'summary' or run == 'all':
        raw, net, hub = analysis.Get_All_Stats(raw_data, network_file, graph, directors)
        analysis.Print_Summary(raw, net, hub)
    if run == 'homog' or run == 'all':
        role_hom, director_hom, attributes, weights = Apply_Metric(network_file)
        util.Print_Ranking(director_hom, role_hom)
        util.Plot_Histogram(director_hom.values(), 'Directors Homogeneity', 'Homogeneity Score')
        grouped_by_attr = analysis.Group_By_Attribute(director_hom, attributes)
        mean_by_attr = util.Group_Means(grouped_by_attr)
        grouped_by_role = analysis.Group_By_Role(role_hom)
        print('Mean Homogeneity By Attribute:')
        mean_by_attr = util.Group_Means(mean_by_attr)
        attr_ranking = sorted(mean_by_attr.items(), key=lambda x:x[1], reverse=True)
        pprint(attr_ranking)
        util.Plot_Subplots(grouped_by_attr)
        print('\nMean Homogeneity By Role:')
        mean_by_role = util.Group_Means(grouped_by_role)
        role_ranking = sorted(mean_by_role.items(), key=lambda x:x[1], reverse=True)
        pprint(role_ranking)
        util.Plot_Subplots(grouped_by_role, name='ByRole')
    if run != 'all' and run != 'summary' and run != 'homog':
        print('Not an option!')
