# Subtask 2: Network Generation
This folder contains all python scripts for network generation.

**netgen_utils.py**
- This is a collection of utility functions that perform different tasks related to generating a network graph modeling the director-crew relationship.

**netgen.py**
- The module uses the NetworkX library and the other modules in this folder to create a graphical representation of the various director-crew network models as described above, which can be used for analyses and visualization.

**metric.py**
- This is the collection of functions that compute the average director homogeneity, role homogeneity, and our custom crew weight

**run.py**
- This script is made for the sole purpose of running functions to process, generate, and write the network graphs for further use in Gephi.
- `python3 -m run`
