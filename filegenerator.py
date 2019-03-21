import pprint
import os

import time
import datetime
import structures

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
            output_list.append(str(line))
            print("    Line {0}: {1}".format(output_list.index(line), line), "")

    if len(output_list) == 0: output_list = [""] # In case the file is empty we want a list, not a set
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

def dict_to_simplehtmlreport (input_dict, filename):
    """
    Objective: open a dictionary and write it to a .html file
    Inputs:
        (1) list 
        (2) output filename
    """
    print("Creating file {0}...".format(filename))
    # Open (or create) file
    with open (filename, "w") as myfile:                
        myfile.write("<body>")
        
        for level1 in input_dict: # Dictionary with a list as entry
            myfile.write("<p>--------------------------------------------------</p>")
            myfile.write("<p>File: <strong>" + str(level1) + "</strong> contains " +
                         str(len(input_dict[level1])) + " tags</p>")

            for level2 in input_dict[level1]: # Dictionary within list
                myfile.write("<p>----------</p>")
                myfile.write("<p>Tag {0}</p>".format(
                                str( 1 + input_dict[level1].index(level2) )))
                myfile.write("<ul><li>Tag : <strong>{0}</strong> with class(es) : <strong>{1}</strong></li>".format(
                             str(level2["tag"]), str(level2["class"]) )) 
                myfile.write("<li>Absolute position : {0} in file {1}.</li></ul>".
                                format(str( 1 + level2["pos_index"]), str( 1 + level2["file_index"]) ))
                myfile.write("<p></p>")
                myfile.write(str(level2["contents"]))        
            myfile.write("<p></p>")
        
        myfile.write("</body>")
        myfile.close()    
    return None

####################################################################################################

def dict_to_simplehtmlabridged (input_dict, filename):
    """
    Objective: open a dictionary and write it to a .html file that will keep the original tag order
    Inputs:
        (1) list 
        (2) output filename
    """
    print("Creating file {0}...".format(filename))
    # Open (or create) file
    tr_dict = structures.dictlist_to_dictdict(input_dict, "pos_index")
    
    with open (filename, "w") as myfile:                
        myfile.write("<body>")
        
        for level1 in tr_dict: # Dictionary with a list as entry
            myfile.write("<p>--------------------------------------------------</p>")
            myfile.write("<p>File: <strong>" + str(level1) + "</strong> contains " +
                         str(len(tr_dict[level1])) + " tags</p>")
            
            sortedkeys = sorted(list(tr_dict[level1].keys()))
            
            for sortedkey in sortedkeys: # Dictionary within list
                level2 = tr_dict[level1][sortedkey]

                myfile.write("<p>----------</p>")
                myfile.write("<p>Tag {0} <strong>{1}</strong> with class(es) : <strong>{2}</strong> in file {3}.</p>".format(
                                str( 1 + sortedkey ),
                                str( level2["tag"] ),
                                str( level2["class"] ),
                                str( 1 + level2["file_index"] ) ))
                myfile.write(str(level2["contents"]))        
            myfile.write("<p></p>")
        
        myfile.write("</body>")
        myfile.close()    
    return None

####################################################################################################
# OTHER FILETYPES MANIPULATION
####################################################################################################

def string_to_txt(filename, string):
    """
    Inputs: output filename, string.
    Objective: converts a string to a text file.
    Outputs: none.
    """
    
    text_file = open(filename, "a")
    text_file.write(string)
    text_file.write("\n"*2)
    text_file.close()
    
    return None