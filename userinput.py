import filegenerator

"""
Functions to obtain user input
"""

def choose_primary_mode ():
    """
    Input: User input.
    Objective: Let the user choose which mode is to be used.
    Output: Dictionary containing the search parameters.
    """

    output_dict  = {}    
    answer       = None
    sourcetype   = None
    tag_tuple    = None
    class__tuple = None
    searchtype   = None
    outputtype   = None
    tagfile      = ""
    classfile    = ""

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
    while tag_tuple is None and searchtype in ("1", "2", "3", "4"):
        if searchtype == "1":
            tag_tuple = (input("\nWhat tag will be searched?\nLeave it blank to search all tags\n"),)
        if searchtype == "2":
            tag_tuple = (input("\nWhat string should appear in the tag name(s)?\n"),)
        if searchtype == "3":
            tag_tuple = ("",)
        if searchtype == "4":
            while ".txt" not in tagfile:
                print("\nWhat is the name of the .txt file where the tags are?")
                tagfile = input('Your input must end in .txt. A full path is also valid.\n')
            tag_tuple   = tuple(filegenerator.txt_to_list(tagfile))
    output_dict["tag"]  = tag_tuple

    # Class search
    while class__tuple is None and searchtype in ("1", "2", "3", "4"):
        if searchtype == "1":
            print("\nWhat class will be searched?")
            class__tuple = (input("Leave it blank to search all classes unless you chose to search all tags\n"),)
        if searchtype == "2":
            class__tuple = (input("\nWhat string should appear in the class name(s)?\n"),)
        if searchtype == "3":
            class__tuple = ("",)
        if searchtype == "4":
            while ".txt" not in classfile:
                print("\nWhat is the name of the .txt file where the classes are?")
                classfile = input('Your input must end in .txt. A full path is also valid.\n')
            class__tuple   = tuple(filegenerator.txt_to_list(classfile))
    output_dict["class_"] = class__tuple
    
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
    
    print("")
    
    return output_dict

####################################################################################################

def input_filename():
    """
    Input: typed by user.
    Objective: get a filename for other functions to use.
    Output: string.
    """
    output_string = ""
    
    while output_string == "":
        print("Please type the filename or path. Don't forget to add the extension at the end.")
        output_string = input("")
        
    return output_string