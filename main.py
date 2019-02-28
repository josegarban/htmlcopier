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
    output_dict ["sourcetype"]        = ""
    output_dict ["tag"]               = ""
    output_dict ["tag_searchtype"]    = ""
    output_dict ["class_"]            = ""
    output_dict ["class__searchtype"] = ""
    
    sourcetype        = None
    tag               = None
    class_            = None
    tag_searchtype    = ""
    class__searchtype = ""

    # Select how search text will be sourced
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

    # Select how tags will be searched
    while tag_searchtype not in ("1", "2", "3", "4"):
        print("\nHow will tags be searched?")
        print("1. Single tag search.")
        print("2. Approximate tag search.")
        print("3. Search across all tags.")
        print("4. Load search terms from a list.")        
        tag_searchtype = input("Type your choice. ")
    output_dict["tag_searchtype"] = tag_searchtype

    while tag is None and tag_searchtype in ("1", "2", "3", "4"):
        if tag_searchtype == "1": tag = input("\nWhat tag will be searched?\n")
        if tag_searchtype == "2": tag = input("\nWhat string should appear in the tag name(s)?\n")
        if tag_searchtype == "3": tag = ""
        if tag_searchtype == "4":
            print("Loading files is not yet available...")
            tag = ""
    output_dict["tag"] = tag

    # Select how classes will be searched
    while class__searchtype not in ("1", "2", "3", "4"):
        print("\nHow will classes be searched?")
        print("1. Single class search.")
        print("2. Approximate class search.")
        print("3. Search across all classes.")
        print("4. Load search terms from a list.")        
        class__searchtype = input("Type your choice. ")
    output_dict["class__searchtype"] = class__searchtype

    while class_ is None and class__searchtype in ("1", "2", "3", "4"):
        if class__searchtype == "1": class_ = input("\nWhat class will be searched?\n")
        if class__searchtype == "2": class_ = input("\nWhat string should appear in the class name(s)?\n")
        if class__searchtype == "3": class_ = ""
        if class__searchtype == "4":
            print("Loading files is not yet available...")
            class_ = ""
    output_dict["class_"] = class_
        
    return output_dict

####################################################################################################

def process_files_in_folder (mode):
    """
    Input: dictionary with parameters
    Objective: read the html files
    Output: 
    """
        
    # Find file(s)
    files = os.listdir()

    # Get a list with just html file names
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
    
    