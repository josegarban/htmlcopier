"""
This script is meant to take several sources,
be it saved files or records from a database
"""

import htmlparser
import filegenerator
import userinput
import pprint


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
    
    print("Total files processed:", len(results), "Type:", type(results))
    for file in results:
        print("  {0} results in file {1}.".format(len(results[file]), file, ))  

    # Prepare the output file
    timestamp = filegenerator.generate_longtimestamp()

    if  mode["outputtype"][0] == "html":
        filename = mode["outputtype"][1] +"_" + timestamp + ".html"
        filegenerator.dict_to_simplehtml (results, filename)
    
    """
        Next steps:
        for the sql version probably a dictionary with "a/link-to" attributes is needed
    """

    return results

####################################################################################################

## Uncomment to run
run = main("")
pprint.pprint(run)
    