"""
This script is meant to take several sources,
be it saved files or records from a database
"""

import htmlparser
import filegenerator
import userinput
import dbhandler
import structures
import os
import pprint

####################################################################################################

def main (mode):
    """
    Input: blank, if set by user. For testing, a dictionary may be used to simulate user input.
    Objective: retrieve tags of a certain class (optional) in one or more html files
                in a local folder or in a remote location.
                Creates a html file consisting of just those tags. No css styles will be copied.
    Output:
        Current: a dictionary with attributes to be converted to an html file.
    """
    results = {}
    if mode == "": mode = userinput.choose_primary_mode() # Usual state of affairs
    
    # Generate a file list
    if mode["sourcetype"][0] == "file":
        folder    = ""
        file      = mode["sourcetype"][1]
        htmlfiles = [file]
    
    elif mode["sourcetype"][0] == "folder":
        folder = mode["sourcetype"][1]
        htmlfiles = filegenerator.html_files_in_folder(mode["sourcetype"][1])
    
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
    
    print("\nTotal files processed:", len(results), "Type:", type(results))
    for file in results:
        print("  {0} results in file {1}.".format(len(results[file]), file, ))  

    # Prepare the output file
    timestamp = filegenerator.generate_longtimestamp()

    if  mode["outputtype"][0] == "html":
        filename = mode["outputtype"][1] + "_" + timestamp + ".html"
        filegenerator.dict_to_simplehtml(results, filename)
    
    if  mode["outputtype"][0] == "current.sqlite":
        filename = mode["outputtype"][1]
        results_mod = dbhandler.flatten_dictdictdict(dictlist_to_dictdict(results))
        dbhandler.update_dict_to_db(results_mod, filename, "Processed_html_files", "id", True)

    if  mode["outputtype"][0] == "fresh.sqlite":
        filename = mode["outputtype"][1] + "_" + filegenerator.generate_timestamp() + ".sqlite" 
        results_mod = structures.flatten_dictdictdict(structures.dictlist_to_dictdict(results))
        print("#"*100)
        pprint.pprint(results_mod)
        print("#"*100)
        dbhandler.create_table(results_mod, filename, "Processed_html_files", True)        
        dbhandler.add_dbrows(results_mod, filename, "Processed_html_files", "id", True)

    return results

####################################################################################################


    