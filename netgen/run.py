import netgen
import netgen_utils

exc_roles = [
    "Additional Crew",
    "Animation Department",
    "Art Department",
    "Art Direction by",
    "Camera and Electrical Department",
    "Cast",
    "Casting By",
    "Casting Department",
    "Costume and Wardrobe Department",
    "Editorial Department",
    "Location Management",
    "Music Department",
    "Produced by",
    "Production Department",
    "Production Management",
    "Script and Continuity Department",
    "Second Unit Director or Assistant Director",
    "Set Decoration by",
    "Stunts",
    "Thanks",
    "Transportation Department",
    "Visual Effects by",
]

file = "fullest_credits.jsonl"

# without role exclusion
netgen.write_graph(netgen.create_graph(file), fname="full_dcnet")

# # with role exclusion
netgen.write_graph(
    netgen.create_graph(file, exclude_roles=exc_roles),
    fname="final_dcnet",
)

# for bipartite subnetwork: remove links between directors that are also crew members
netgen.write_graph(
    netgen.create_graph(file, exclude_roles=exc_roles, remove_dir_targets=True),
    fname="for_bipartite_dcnet",
)
