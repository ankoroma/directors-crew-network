import json
import gzip
import numpy as np
from pprint import pprint
from analysis_utils import load_director, Normalize_Roles

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
    "Visual Effects by"
]
    
def Get_Department_Counts(movies):
    """Returns dictionary showing the amount of times a director employed a specific role/department"""
    dept_counts = {}
    for movie in range(len(movies)):
        crew = movies[movie]['crew']
        roles = set([role[0] for role in crew ])
        for role in roles:
            if role in dept_counts:
                dept_counts[role] += 1
            else:
                dept_counts[role] = 1
    return dept_counts

def Homog_By_Dept(crew_list, homog_dict, exclude=True):
    """Returns a dictionary of usage counts for each crew member in each role"""
    for role in crew_list:
        if role[0] in exc_roles and exclude:
            continue
        if role[0] in homog_dict.keys():
            if role[1] in homog_dict[role[0]].keys():
                homog_dict[role[0]][role[1]] += 1
            else:
                homog_dict[role[0]][role[1]] = 1
        else:
            homog_dict[role[0]] = {role[1]:1}
    return homog_dict

def Get_Weights(crew_list, weight_dict, dept_counts, exclude=True):
    """Returns a dictionary of weights between the director and each crew member, organized by role"""
    for role in crew_list:
        if role[0] in exc_roles and exclude:
            continue
        if role[0] in weight_dict.keys():
            if role[1] in weight_dict[role[0]].keys(): # If we have seen the crew member before, that means they have been re-used
                try:
                    weight_dict[role[0]][role[1]] += 1/(dept_counts[role[0]]-1) # Add 1/number of possible re-uses to their weight
                except: 
                    weight_dict[role[0]][role[1]] += 0 # If the department was only used in one movie, the weight remains at zero
            else: # Add new crew member to existing role
                weight_dict[role[0]][role[1]] = 0 # Weight is initialized to zero since this is the first time we have seen them
        else: # Initialize the role in the weight dictionary
            weight_dict[role[0]] = {role[1]:0} # The weight is set to zero for a new crew member since this is the first time we have seen them
    return weight_dict

def Homog_By_Dir(homog_dict):
    """
    Returns the overall homogeneity score for a given director. 
    This is the average homogeneity across roles.
    """
    homogeneity = {}
    for key in homog_dict.keys(): # For each department...
        unique = len(homog_dict[key].keys()) # Number of unique crew members
        total = sum(list(homog_dict[key].values())) # Total number of crew members
        if unique == 1:
            homogeneity[key] = 1
        else:
            homogeneity[key] = 1 - (unique/total)
    total_homogeneity = np.mean(list(homogeneity.values()))
    return homogeneity, total_homogeneity

def Apply_Metric(file, exclude=True):
    """
    Returns three dictionaries: crew_homogeneity, role_homogeneity, and dir_homogeneity

    role_homogeneity: Homogeneity scores for each role/department under each director
       
    dir_homogeneity: Total homogeneity score for each director (average homogeneity across roles/departments)

    dir_attributes: Additional information about each director e.g. sex, ethnicity, renowned

    all_weights: Relationship Strength score for each individual crew member within each department for each director.
    """
    dir_homogeneity = {}
    role_homogeneity = {}
    all_weights = {}
    dir_attributes = {}
    for director in load_director(file):
        director = json.loads(director)
        name = director['name']
        gender = director['gender']
        ethn = director['ethnicity']
        other = director['otherlabel']
        num_movies = len(director['movies'])
        dir_attributes[name] = {'gender':gender, 'ethnicity':ethn, 'other':other, 
                                'num_movies':num_movies, 'role_counts':{}}
        homog_dict = {}
        weights = {}
        movies = Normalize_Roles(director['movies'])
        dept_counts = Get_Department_Counts(movies)
        m = 0
        while m < len(movies):
            crew_list = movies[m]['crew']
            homog_dict = Homog_By_Dept(crew_list, homog_dict, exclude)
            weights = Get_Weights(crew_list, weights, dept_counts)
            m += 1
        for role in homog_dict.keys():
            dir_attributes[name]['role_counts'][role] = len(homog_dict[role])
        role_homog, dir_homog = Homog_By_Dir(homog_dict)
        role_homogeneity[name] = role_homog
        dir_homogeneity[name] = dir_homog
        all_weights[name] = weights
    return  role_homogeneity, dir_homogeneity, dir_attributes, all_weights
