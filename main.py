"""
This script is meant to take several sources,
be it saved files or records from a database
"""

import htmlparser
import os
import pprint

def choose_mode ():
    """
    Input: None.
    Objective: Let the user choose which mode is to be used.
    Output:
    """
    print("""
This script will analyze one or more .html files and extract the text
and attibutes within a particular tag and class (optional).\n
    """)
    output_dict = {}
    output_dict ["sourcetype"] = ""
    output_dict ["tag"]        = ""
    output_dict ["class_"]     = ""
    
    sourcetype = None
    tag        = ""
    class_     = None
        
    while sourcetype not in ("y", "Y", "n", "N"):
        sourcetype = input("Will files be read from a folder? Y/N\n")

        if sourcetype in ("y", "Y") :
            output_dict["sourcetype"] = "folder"
            continue
        
        elif sourcetype in ("n", "N"):
            sourcetype = input("Will files be read from a website? Y/N\n")
            if sourcetype in ("y", "Y"): output_dict["sourcetype"] = "website"
        
            elif sourcetype in ("n", "N"):
                sourcetype = input("Will fields be read from a database? Y/N\n")
                
                if sourcetype in ("y", "Y"):
                    output_dict["sourcetype"] = "database"
                else:
                    print ("Incorrect input. Please start over...")
                    return output_dict
                
    while tag == "":
        tag = input("What tag will be searched?\n")
        output_dict["tag"] = tag

    while class_ is None:
        class_ = input("What class will be searched? Leave this blank if classes don't matter.\n")
        output_dict["class_"] = class_
        
    return output_dict

####################################################################################################

def process_files_in_folder (mode):
    """
    Input: dictionary with parameters
    Objective: read the html files
    Output: 
    """
        
    
    files = os.listdir()
    htmlfiles  = []
    
    for file in files: 
        if ".html" in file: htmlfiles.append(file)
    
    if len (htmlfiles) == 0:
        print("No html files found.")
    else:
        print("The following files were found:")
        pprint.pprint(htmlfiles)
        print("")

    return htmlfiles

####################################################################################################

def main ():
    """
    Input: set by user.
    Objective: retrieve tags of a certain class (optional) in one or more html files
                in a local folder or in a remote location.                
    Output: an html file consisting of just those tags. No styles will be copied.
    """
    
    mode = choose_mode()
    
    if mode ["sourcetype"] == "folder" :
        htmlfiles = process_files_in_folder (mode)
        for file in htmlfiles:
            htmlparser.extract_tags_classes(file, mode["tag"], mode["class_"])
    
    if mode ["sourcetype"] == "website":
        return None
    
main()
    
    