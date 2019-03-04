"""
This script is meant to take several sources,
be it saved files or records from a database
"""

import htmlparser
import filegenerator
import os
import pprint

def choose_mode ():
    """
    Input: User input.
    Objective: Let the user choose which mode is to be used.
    Output: Dictionary containing the search parameters.
    """

    output_dict = {}    
    answer     = None
    sourcetype = None
    tag        = None
    class_     = None
    searchtype = None
    outputtype = None

    print("""
This script will analyze one or more .html files and extract the text
and attibutes within a particular tag and class (optional).
    """)
    
    # Select how search text will be sourced
    while answer not in ("y", "Y", "n", "N"):
        answer = input("Will files be read from a folder? Y/N\n")
        
        if answer in ("y", "Y"):
            answer = input("Will a single file be read? Y/N\n")
            if answer in ("y", "Y"):
                sourcetype = "file"
            elif answer in ("n", "N"):
                sourcetype = "folder"
            continue
        
        elif answer in ("n", "N"):
            answer = input("Will files be read from a website? Y/N\n")
            if answer in ("y", "Y"):
                sourcetype = "website"
        
            elif answer in ("n", "N"):
                answer = input("Will fields be read from a database? Y/N\n")                
                if answer in ("y", "Y"):
                    sourcetype = "database"

                else:
                    print ("Incorrect input. Please start over...")
                    return output_dict

    # Get file name if it is a single file
    if sourcetype == "file":
        file = ""
        while file == "":
            file = input('Insert the file name, with ".html" at the end.\n')
            output_dict ["sourcetype"] = (sourcetype, file)

    # Get file name if it is a single folder
    if sourcetype == "folder":        
        folder = ""
        print("Insert the folder absolute path. If it's the same folder as this script, hit ""Enter"".")
        folder = input("")
        output_dict ["sourcetype"] = (sourcetype, folder)

    # Select how tags will be searched
    while searchtype not in ("1", "2", "3", "4"):
        print("\nHow will tags and/or classes be searched?")
        print("1. Single tag/class search.")
        print("2. Approximate tag/class search.")
        print("3. Search across all tags and classes.")
        print("4. Load search terms from a list.")        
        searchtype = input("Type your choice. ")
    if   searchtype == "1": output_dict["searchtype"] = "Exact"
    elif searchtype == "2": output_dict["searchtype"] = "Approximate"
    elif searchtype == "3": output_dict["searchtype"] = "All"
    elif searchtype == "4": output_dict["searchtype"] = "List"

    # Tag search
    while tag is None and searchtype in ("1", "2", "3", "4"):
        if searchtype == "1": tag = input("\nWhat tag will be searched?\nLeave it blank to search all tags\n")
        if searchtype == "2": tag = input("\nWhat string should appear in the tag name(s)?\n")
        if searchtype == "3": tag = ""
        if searchtype == "4":
            print("Loading files is not yet available!")
            tag = ""
    output_dict["tag"] = tag
    
    # Class search
    while class_ is None and searchtype in ("1", "2", "3", "4"):
        if searchtype == "1": class_ = input("\nWhat class will be searched?\nLeave it blank to search all classes\n")
        if searchtype == "2": class_ = input("\nWhat string should appear in the class name(s)?\n")
        if searchtype == "3": class_ = ""
        if searchtype == "4":
            print("Loading files is not yet available!")
            class_ = ""
    output_dict["class_"] = class_
    
    # Output generation
    while outputtype not in ("1", "2", "3", "4"):
        print("\nHow should the output be produced?")
        print("1. .html file.")
        print("2. .pdf file.")
        print("3. Current .sqlite database.")
        print("4. Fresh .sqlite database.")
        outputtype = input("Type your choice. ")
        
    if  outputtype == "1":
        outputfile = "html"
        outputname = "output"
         
    elif outputtype == "2":
        outputfile  = "pdf"
        print(".pdf output not available yet!")
        outputname = "output"

    elif outputtype == "3":
        outputfile = "current.sqlite"
        print(".sqlite output not available yet!")
        #outputname = input("Insert filename or path without the .sqlite extension")

    elif outputtype == "4":
        outputfile = "fresh.sqlite"
        print(".sqlite output not available yet!")
        outputname = "output"
    
    output_dict["outputtype"] = (outputfile, outputname)
    
    return output_dict

####################################################################################################

def process_files_in_folder (folder):
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
    else:
        print("The following files were found:")
        pprint.pprint(htmlfiles)

    return htmlfiles

####################################################################################################

def main (mode):
    """
    Input: blank, if set by user. For testing, a dictionary may be used to simulate user input.
    Objective: retrieve tags of a certain class (optional) in one or more html files
                in a local folder or in a remote location.                
    Output:
        Current: a dictionary with attributes to be converted to an html file
        Goal: an html file consisting of just those tags. No styles will be copied.
    """
    results = {}
    if mode == "": mode = choose_mode() # Usual state of affairs
    
    # Generate a file list
    if mode["sourcetype"][0] == "file":
        folder    = ""
        file      = mode["sourcetype"][1]
        htmlfiles = [file]
    
    elif mode["sourcetype"][0] == "folder":
        folder = mode["sourcetype"][1]
        htmlfiles = process_files_in_folder(mode["sourcetype"][1])
    
    else:
        print("Websites or databases can't be processed yet")
        return results 
    
    # Process our file list
    for file in htmlfiles:
        if "\\" not in file:
            absolute_file_location = os.path.join(folder,file)
            # Join path and filename if a path is involved
        else:
            absolute_file_location = file
            
        if   mode ["searchtype"] == "Exact":
            results[file] = htmlparser.extract_tags_classes_exact(
                absolute_file_location, mode["tag"], mode["class_"])
    
        elif mode ["searchtype"] == "Approximate":
            results[file] = htmlparser.extract_tags_classes_approximate(
                absolute_file_location, mode["tag"], mode["class_"])
    
        elif mode ["searchtype"] == "All":
            results[file] = htmlparser.extract_all_tags_classes(
                absolute_file_location)
    
    print("Total files processed:", len(results), "Type:", type(results))
    for file in results:
        print("  {0} results in file {1}.".format(len(results[file]), file, ))  

    # Prepare the output file
    timestamp = filegenerator.generate_longtimestamp()

    if  mode["outputtype"][0] == ".html":
        filename = mode["outputtype"][1] +"_" + timestamp + ".html"
        filegenerator.dict_to_simplehtml (results, filename)
    
    """
        Next steps:
        for the sql version probably a dictionary with "a/link-to" attributes is needed
    """

    return results

####################################################################################################

## Uncomment to run
#run = main("")
#pprint.pprint(run)
    