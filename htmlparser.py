import pprint
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
    
    try:
        with open(filename, "r", errors="replace") as myfile:
            print("Successfully opened {0}.\n".format(filename))
            for line in myfile:
                try:
                    line = line.rstrip()
                    line = line.encode('latin-1').decode('unicode-escape').encode('latin-1').decode('utf-8')
                    output_string = output_string + line
                except:
                    #print("Failed line", line)
                    pass

        return output_string  

    except:
        print("\nFailed to open {0}.\n".format(filename))

####################################################################################################

def get_class_names (html_filename):
    """
    Inputs: filename of an html file.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of class names is returned
    Output: list with extracted class names.
    """
    output_set = set()

    html_string = file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")

    for tag in soup.find_all():
        if tag.get("class") is None: pass
        else: output_set.update(tag.get("class")) # It has to be update because multiple classes are possible
    
    return output_set

####################################################################################################

def get_tag_names (html_filename):
    """
    Inputs: filename of an html file.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tag names is returned
    Output: list with extracted tag names.
    """
    output_set = set()

    html_string = file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")

    for tag in soup.find_all():
        output_set.add(tag.name) 
    
    return output_set

####################################################################################################

def extract_tags_classes(html_filename, tag, class_):
    """
    Inputs: filename of an html file, tag we want to retrieve, class we want to retrieve.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")
    
    if class_ != "" and tag != "":
        output_snippets = soup.find_all(tag, class_)
        print('{0} <{1}> tags with the class "{2}" were retrieved in the file {3}.\n'.format(
            len(output_snippets), tag, class_, html_filename))

    elif class_ == "" and tag != "":
        output_snippets = soup.find_all(tag)   
        print('{0} <{1}> tags were retrieved in the file {2}.\n'.format(
            len(output_snippets), tag, html_filename))

    elif class_ != "" and tag == "":
        output_snippets = []
        for tag in soup.find_all():
            if tag.get("class") is not None:
                if class_ in tag.get("class"):
                    output_snippets.append(tag)   
        print('{0} tags with the class "{1}" were retrieved in the file {2}.\n'.format(
            len(output_snippets), class_, html_filename))

    elif class_ == "" and tag == "":
        output_snippets = soup.find_all()   
        print('{0} tags of all types and classes were retrieved in the file {1}.\n'.format(
            len(output_snippets), html_filename))

    return output_snippets



