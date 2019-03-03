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
                print("\n    {0} was successfully opened.\n".format(filename))
        return output_string  
    
    except:
        print("\n    Failed to open {0}.\n".format(filename))
        return ""
    
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
            print("\n    Successfully opened {0}.".format(filename))
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
        
    finally:
        return output_string  

####################################################################################################

def get_class_names (html_string):
    """
    Inputs: string representing an html file.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of class names is returned
    Output: list with extracted class names.
    """
    output_set = set()

    soup = BeautifulSoup(html_string, "html.parser")

    for tag in soup.find_all():
        if tag.get("class") is None: pass
        else: output_set.update(tag.get("class")) # It has to be update because multiple classes are possible
    
    return output_set

####################################################################################################

def get_tag_names (html_string):
    """
    Inputs: string representing an html file.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tag names is returned
    Output: list with extracted tag names.
    """
    output_set = set()

    soup = BeautifulSoup(html_string, "html.parser")

    for tag in soup.find_all():
        output_set.add(tag.name) 
    
    return output_set

####################################################################################################

def extract_tags_classes_exact(html_filename, wanted_tag, wanted_class_):
    """
    Inputs: filename of an html file, tag we want to retrieve, class we want to retrieve.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")
    
    if wanted_class_ != "" and wanted_tag != "":
        output_snippets = soup.find_all(wanted_tag, wanted_class_)
        print('    {0} <{1}> tags with the class "{2}" were retrieved in the file {3}.\n'.format(
            len(output_snippets), wanted_tag, wanted_class_, html_filename))

    elif wanted_class_ == "" and wanted_tag != "":
        output_snippets = soup.find_all(wanted_tag)   
        print('    {0} <{1}> tags were retrieved in the file {2}.\n'.format(
            len(output_snippets), wanted_tag, html_filename))

    elif wanted_class_ != "" and wanted_tag == "":
        output_snippets = []
        for tag in soup.find_all():
            if tag.get("class") is not None:
                if wanted_class_ in tag.get("class"):
                    output_snippets.append(tag)   
        print('    {0} tags with the class "{1}" were retrieved in the file {2}.\n'.format(
            len(output_snippets), wanted_class_, html_filename))

    return output_snippets


####################################################################################################

def extract_tags_classes_approximate(html_filename, wanted_tag, wanted_class_):
    """
    Inputs: filename of an html file, tag we want to retrieve, class we want to retrieve.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")
    
    # Get all tags similar to tag
    if wanted_tag != "":
        similar_tags = set()
        for tag in soup.find_all():
            if wanted_tag in tag.name: similar_tags.add(tag.name)
        print("      Similar tags:", similar_tags)

    # Get all classes similar to class_
    if wanted_class_ != "":
        classes = get_class_names(html_string)
        similar_classes = set()
        for class_ in classes:
            if wanted_class_ in class_: similar_classes.add(class_)
        print("      Similar classes:", similar_classes)

    print("")
    # Different cases (whether we search classes, tags, both or all)
    
    if wanted_class_ != "" and wanted_tag != "":
        output_snippets = []
        for tag in similar_tags:
            for class_ in similar_classes:
                snippets = soup.find_all(tag, class_)
                print('      {0} <{1}> tags with the class "{2}" were retrieved in the file {3}.\n'.format(
                    len(snippets), tag, class_, html_filename))
                output_snippets.append(tag)
        #print (output_snippets)

    elif wanted_class_ == "" and wanted_tag != "":
        output_snippets = []
        for tag in similar_tags:
            snippets = soup.find_all(tag)
            print('      {0} <{1}> tags were retrieved in the file {2}.\n'.format(
                len(snippets), tag, html_filename))
            output_snippets.append(tag)
        #print (output_snippets)
        
    elif wanted_class_ != "" and wanted_tag == "":
        output_snippets = []
        for tag in soup.find_all():
            if tag.get("class") is not None:
                classes_in_tag = tag.get("class")
                for class_in_tag in classes_in_tag:
                
                    if class_in_tag in list(similar_classes):
                        output_snippets.append(tag)   
        
        print('      {0} tags with classes similar to "{1}" were retrieved in the file {2}.\n'.format(
            len(output_snippets), wanted_class_, html_filename))
        #print (output_snippets)
    
    return output_snippets

####################################################################################################

def extract_all_tags_classes(html_filename):
    """
    Inputs: filename of an html file, tag we want to retrieve, class we want to retrieve.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")
    
    output_snippets = []
    
    print('      {0} tags of all types and classes were retrieved in the file {1}.\n'.format(
        len(soup.find_all()), html_filename))
    # print (output_snippets)
        
    return output_snippets


