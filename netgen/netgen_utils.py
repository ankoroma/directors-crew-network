import os
import json
import networkx as nx


def get_file_size(path):
    """Get the size of a file"""
    return os.path.getsize(path)


def path_exists(path):
    """Check if a path exists"""
    return os.path.exists(path)


def delete_file(path):
    """Delete a file"""
    try:
        os.remove(path)
        print(f"Deleted {path}")
    except Exception as e:
        ErrorHandler(e, input=path)
        print(f"Could not delete {path}")


def ErrorHandler(err, **details):
    """Handle errors gracefully"""
    err_type = type(err).__name__
    print(f"An error occurred: {err_type}")
    print(err)
    for k, v in details.items():
        print(f"{k}: {v}")
    return None


def load_data(file):
    """Load data iteratively"""
    with open(file) as infile:
        for line in infile:
            yield line


def json_loader(data):
    """Load JSON data"""
    return json.loads(data)


def get_directors(file):
    """Get the directors"""
    try:
        directors = []
        for data in load_data(file):
            data = json_loader(data)
            directors.append(data["name"])
        print("Returned directors...")
        return directors
    except Exception as e:
        ErrorHandler(e, input=file)
        print("Could not return directors!")


def get_movies(file):
    """Get the movies"""
    movies = []
    try:
        for data in load_data(file):
            data = json_loader(data)
            for movie in data["movies"]:
                movies.append(movie["title"])
        print("Returned movies...")
        return movies
    except Exception as e:
        ErrorHandler(e, input=file)
        print("Could not return movies!")


def get_roles(file, exclude_roles=None):
    """Get the distinct crew roles"""
    roles = []
    try:
        for data in load_data(file):
            data = json_loader(data)
            for movie in data["movies"]:
                for crew in movie["crew"]:
                    norm_role = normalize_role(crew[0])
                    if (exclude_roles is not None) and (norm_role in exclude_roles):
                        continue
                    roles.append(norm_role)
        print("Returned roles...")
        return set(roles)
    except Exception as e:
        ErrorHandler(e, input=file)
        print("Could not return roles!")


def get_node_type(crew_name, directors):
    """Get the node type: crew or director"""
    return "crew" if crew_name not in directors else "director"


def remove_extra_whitespaces(string):
    """Remove extra whitespaces from a string"""
    return " ".join(string.split())


def combine_labels(gender, ethnicity, label):
    """Group director labels into a single label"""
    return (
        gender + ethnicity if isinstance(label, float) else gender + ethnicity + label
    )


def renowned(label):
    """return the renowned label of a director: handles NaNs"""
    return "nan" if isinstance(label, float) else label


def normalize_role(role):
    """Normalize the crew roles"""
    return "Writing Credits" if role.startswith("Writing") else role


def show_self_loops(G):
    """Show the self-loops in the graph"""
    print(f"Self-loops:\n\n {list(nx.nodes_with_selfloops(G))}")  # type: ignore
    return None


def remove_self_loops(G):
    """Remove the self-loops in the graph"""
    selfloops = list(nx.selfloop_edges(G))  # type: ignore
    G.remove_edges_from(selfloops)
    return None
