import pprint
import os

import time
import datetime

"""
Objective: create csv files
"""
####################################################################################################
# FILESYSTEM
####################################################################################################

def generate_timestamp ():
    """
    Inputs: None
    Returns: String with a timestamp to be appended to a file name
    """
    now = datetime.datetime.now()
    timestamp = now.fromtimestamp(time.time()).strftime("%Y%m%d_%H%M%S")

    return timestamp

def generate_longtimestamp ():
    """
    Inputs: None
    Returns: String with a fully precise timestamp to be appended to a file name
    """
    now = datetime.datetime.now()
    timestamp = str(now.fromtimestamp(time.time())).replace(":", "").replace("-", "").replace(".", ",")

    return timestamp

####################################################################################################
# HTML FILE MANIPULATION
####################################################################################################

def dict_to_simplehtml (input_dict, filename):
    """
    Objective: open a dictionary and write it to a .html file
    Inputs:
        (1) list 
        (2) output filename
    """
    print("Creating file {0}...".format(filename))
    # Open (or create) file
    with open (filename, "w") as myfile:                
        
        for key in input_dict:
            myfile.write(r"<strong>File: " + str(key) + "</strong> \n")
            myfile.write(str(input_dict[key])[1:-1])
            myfile.write("\n")

        myfile.close()    
    return None

