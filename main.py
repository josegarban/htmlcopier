"""
This script is meant to take several sources,
be it saved files or records from a database
"""

import htmlparser
import os
import pprint

def choose_mode ():
    """
    Input: User input.
    Objective: Let the user choose which mode is to be used.
    Output: Dictionary containing the search parameters.
    """

    output_dict = {}    
    sourcetype = None
    tag        = None
    class_     = None
    searchtype = None

    # Select how search text will be sourced
    while sourcetype not in ("y", "Y", "n", "N"):
        sourcetype = input("Will files be read from a folder? Y/N\n")

        if sourcetype in ("y", "Y"):
            sourcetype = input("Will a single file be read? Y/N\n")
            if sourcetype in ("y", "Y"):
                print("You will be asked for the file name later.")
                output_dict["sourcetype"] = "file"
            else:
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
    while searchtype not in ("1", "2", "3", "4"):
        print("\nHow will tags and/or classes be searched?")
        print("1. Single tag/class search.")
        print("2. Approximate tag/class search.")
        print("3. Search across all tags and classes.")
        print("4. Load search terms from a list.")        
        searchtype = input("Type your choice. ")
    if   searchtype == "1": output_dict["searchtype"] = "Single"
    elif searchtype == "2": output_dict["searchtype"] = "Approximate"
    elif searchtype == "3": output_dict["searchtype"] = "All"
    elif searchtype == "4": output_dict["searchtype"] = "List"

    while tag is None and searchtype in ("1", "2", "3", "4"):
        if searchtype == "1": tag = input("\nWhat tag will be searched?\nLeave it blank to search all tags\n")
        if searchtype == "2": tag = input("\nWhat string should appear in the tag name(s)?\n")
        if searchtype == "3": tag = ""
        if searchtype == "4":
            print("Loading files is not yet available!")
            tag = ""
    output_dict["tag"] = tag
    
    while class_ is None and searchtype in ("1", "2", "3", "4"):
        if searchtype == "1": class_ = input("\nWhat class will be searched?\Leave it blank to search all classes\n")
        if searchtype == "2": class_ = input("\nWhat string should appear in the class name(s)?\n")
        if searchtype == "3": class_ = ""
        if searchtype == "4":
            print("Loading files is not yet available!")
            class_ = ""
    output_dict["class_"] = class_
        
    return output_dict

####################################################################################################

def process_files_in_folder ():
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
    print("""
This script will analyze one or more .html files and extract the text
and attibutes within a particular tag and class (optional).\n
    """)
    results = ""
    mode = choose_mode()
    
    file = ""
    if mode ["sourcetype"] == "file"   :
        while file = "":
            file = input('Insert the file name, with ".html" at the end.\n')
        htmlfiles = [file]

    if mode ["sourcetype"] == "folder" :
        htmlfiles = process_files_in_folder()
        
    for file in htmlfiles:
        if   mode ["searchtype"] == "Single":
            results = htmlparser.extract_tags_classes_exact(file, mode["tag"], mode["class_"])
    
        elif mode ["searchtype"] == "Approximate":
            results = htmlparser.extract_tags_classes_approximate(file, mode["tag"], mode["class_"])
    
        elif mode ["searchtype"] == "All":
            results = htmlparser.extract_tags_classes_exact(file, "", "")
    
#    print(type(results))
#    print(len(results))
#    print(results)
    
#    if mode ["sourcetype"] == "website":
    
#    if mode ["sourcetype"] == "database":

    return results

####################################################################################################
    
main()
    
    