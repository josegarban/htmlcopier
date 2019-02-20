import pprint
import os
from bs4 import BeautifulSoup

####################################################################################################

def txt_to_string (filename):
    """
        Input: filename
        Objective: open a file and return a string, to be handled in-memory
        Output: string 
    """
    output_string = ""
    
    try:        
        with open(filename, "r") as myfile:
            for line in myfile:
               output_string = output_string + line    
    #pprint.pprint(output_string)
            print("\n{0} was successfully opened.\n".format(filename))
        return output_string
      
    except:
        print("\nFailed to open {0}.\n".format(filename))

####################################################################################################

def file_to_string (filename):
    """
        Input: filename
        Objective: open a file and return a string, to be handled in-memory
        Output: string 
    """
    output_string = ""
    
#    try:
    print("\n{0} was successfully opened.\n".format(filename))
        
    with open(filename, "r") as myfile:
        for line in myfile:
            line = line.rstrip()
#            line = line.encode("unicode-escape").decode("latin-1")
            print(line)
            output_string = output_string + line    
    #pprint.pprint(output_string)
    
    return output_string
      
#    except:
#        print("\nFailed to open {0}.\n".format(filename))

####################################################################################################

def extract_tags_classes(html_filename, tag, class_ = ""):
    """
    Inputs: filename of an html file, tag we want to retrieve, class (optional) we want to retrieve.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")
    
    if class_ != "":
        wanted_tags = soup.find_all(tag, class_)   
        print('{1} <{2}> tags with the class "{3}" were retrieved in the file {0}.'.format(
            html_filename, len(wanted_tags), tag, class_))

    elif class_ == "":
        wanted_tags = soup.find_all(tag)   
        print('{1} <{2}> tags were retrieved in the file {0}.'.format(
            html_filename, len(wanted_tags), tag))

    return wanted_tags

## Test with class
#file = "alice.html"
#test = extract_tags_classes(file,"p","story")
#pprint.pprint(test)
## Test without class
#file = "alice.html"
#test = extract_tags_classes(file,"p")
#pprint.pprint(test)

## Test with actual file
file = "file1.html"

#test = extract_tags_classes("file1.html", "a")
pprint.pprint(file_to_string("file1.html"))

