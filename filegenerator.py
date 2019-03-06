import pprint
import os

import time
import datetime

"""
Objective: create or read files
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

def html_files_in_folder (folder):
    """
    Input: folder path
    Objective: find html files in the same folder
    Output: list with filenames
    """
    
    if folder == "":
        # Find file(s) in same folder
        files = os.listdir()
    else:
        # Find file(s) in other folder
        files = os.listdir(folder)

    # Get a list with just html file names
    htmlfiles  = []
    for file in files: 
        if ".html" in file: htmlfiles.append(file)
    if len (htmlfiles) == 0:
        print("No html files found.")
        print("")
    else:
        print("The following files were found:")
        pprint.pprint(htmlfiles)
        print("")
        
    return htmlfiles

####################################################################################################
# READ FILES
####################################################################################################

def txt_to_list(filename):
    """
    Input: txt filename
    Output: list
    """
    output_list = []
    print("  Reading file {0}...".format(filename))
    
    with open(filename, "r") as my_file:
        for line in my_file:
            line = line.rstrip()
            output_list.append(line)
            print("    Line {0}: {1}".format(output_list.index(line), line), "")
    
    return output_list

####################################################################################################

def file_to_string (filename):
    """
        Input: filename
        Objective: open a file and return a string, to be handled in-memory
        Output: string 
    """
    output_string = ""
    
    try:
        with open(filename, "r", errors="replace") as myfile:
            print("    Successfully opened {0}.".format(filename))
            for line in myfile:
                try:
                    line = line.rstrip()
                    line = line.encode('latin-1').decode('unicode-escape').encode('latin-1').decode('utf-8')
                    output_string = output_string + line
                except:
                    #print("Failed line", line)
                    pass

    except:
        print("\n    Failed to open {0}.\n".format(filename))
        
    return output_string  

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
            myfile.write((str(input_dict[key])[1:-1]))
            myfile.write("<p></p>")
            myfile.write("\n")

        myfile.close()    
    return None
