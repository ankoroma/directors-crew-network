# Analysis Script (Run_Analysis.py)

When run, the analysis script outputs statistics and visualizations that describe the data and network. 

The user is given three options for the type of analysis they would like to run:

- all
- summary
- homog

The "all" option will run both the "summary" analysis and the "homog" analysis

### summary:

The "summary" option will run the following analyses:
- **Data composition analysis**
  - Counts of gender, ethnicity, renowned, queer
- **Small Worlds Analysis**
  - Connectivity
  - Triangles/clustering coefficient statistics and histogram
  - density/sparcity
  - assortativity coefficient
- **Hubs Analysis**
  - Director and crew degree rankings (unweighted and weighted)
  - Average degree for directors and crew members
  - Director betweenness centrality: ranking, histogram, and mean score

### homog:

The "homog" option will run an analysis based on the role homogeneity metric.

The output for the homog option includes the following:
- Director homogeneity ranking with top 3 roles for each director
  - Histogram of all director homogeneity scores
- Homogeneity by attribute
  - Mean values by attribute
  - Histograms of each attributes distribution of scores
- Homogeneity by role
  - Mean values by role
  - Histograms of each roles distribution of scores


