import networkx as nx
import netgen_utils as nu
import metric


def create_graph(file, exclude_roles=None, remove_dir_targets=False):
    """Generate a networkx graph from the full director credits: user can decide which roles to exclude"""
    directors = nu.get_directors(file)
    scores = metric.Apply_Metric(file)

    def add_dir_nodes(G):
        """Add director nodes to the graph"""
        dir_homogeneity = scores[1]
        for data in nu.load_data(file):
            data = nu.json_loader(data)
            dir_name = nu.remove_extra_whitespaces(data["name"])
            renowned_status = nu.renowned(data["otherlabel"])
            combined_label = nu.combine_labels(
                data["gender"], data["ethnicity"], data["otherlabel"]
            )
            G.add_node(
                dir_name,
                dir_names=dir_name,
                dir_ids=data["dir_id"],
                gender=data["gender"],
                ethnicity=data["ethnicity"],
                renowned=renowned_status,
                grouped_labels=combined_label,
                type="director",
                avg_dir_homog=float(dir_homogeneity[data["name"]]),
            )
        print("Added director nodes to the graph...")
        return None

    def add_crew_nodes(G):
        """Add crew nodes to the graph"""
        for data in nu.load_data(file):
            data = nu.json_loader(data)
            for movie in data["movies"]:
                for crew in movie["crew"]:
                    crew_name = nu.remove_extra_whitespaces(crew[1])
                    norm_role = nu.normalize_role(crew[0])
                    if (exclude_roles is not None) and (norm_role in exclude_roles):
                        continue
                    node_type = nu.get_node_type(crew[1], directors)  # type: ignore
                    if (not G.has_node(crew_name)) and node_type == "crew":
                        G.add_node(
                            crew_name,
                            crew_names=crew_name,
                            gender="nan",
                            ethnicity="nan",
                            avg_dir_homog=0.0,
                            grouped_labels=node_type,
                            type=node_type,
                        )
        print("Added crew nodes to the graph...")
        return None

    def add_edges(G):
        crew_homogeneity = scores[3]
        for data in nu.load_data(file):
            data = nu.json_loader(data)
            dir_name = nu.remove_extra_whitespaces(
                data["name"]
            )  # remove extra whitespaces
            for movie in data["movies"]:
                for crew in movie["crew"]:
                    crew_name = nu.remove_extra_whitespaces(
                        crew[1]
                    )  # remove extra whitespaces
                    norm_role = nu.normalize_role(crew[0])
                    if (exclude_roles is not None) and (norm_role in exclude_roles):
                        continue
                    node_type = nu.get_node_type(crew[1], directors)  # type: ignore
                    if remove_dir_targets and (node_type == "director"):
                        continue
                    if G.has_edge(dir_name, crew_name):
                        G.edges[dir_name, crew_name]["weight"] += 1
                    else:
                        crew_homg = float(
                            crew_homogeneity[data["name"]][norm_role][crew[1]]
                        )
                        G.add_edge(
                            dir_name,
                            crew_name,
                            weight=1,
                            departments=norm_role,
                            crew_homog=crew_homg,
                        )
        print("Added edges to the graph...")
        return None

    try:
        G = nx.Graph()
        add_dir_nodes(G)
        add_crew_nodes(G)
        add_edges(G)
        nu.remove_self_loops(G)
        print("Graph generated...")
        return G
    except Exception as e:
        nu.ErrorHandler(e, input=file)
        print("Could not generate graph!")
        return None


def write_graph(G, fname="sample", ext=".graphml"):
    """Write the graph to a graphml file for later use in Gephi"""
    try:
        nx.write_graphml(G, fname + ext)  # type: ignore
        if nu.get_file_size(fname + ext) < 275:
            nu.delete_file(fname + ext)
        else:
            print(f"Graph written to {fname + ext}")
    except Exception as e:
        nu.ErrorHandler(e, input=G)
        print("Could not write graph!")
        # delete the empty file
        if nu.path_exists(fname + ext) and nu.get_file_size(fname + ext) == 0:
            nu.delete_file(fname + ext)
    return None
