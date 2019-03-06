import pprint
import filegenerator
from bs4 import BeautifulSoup
    
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

def extract_tags_classes_exact(html_filename, wanted_tags, wanted_classes):
    """
    Inputs: filename of an html file,
            tuple with tag(s) we want to retrieve,
            tuple with class(es) we want to retrieve.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = filegenerator.file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")
    output_snippets = []
    
    if wanted_classes != ("",) and wanted_tags != ("",):
        for wanted_tag in wanted_tags:
            for wanted_class_ in wanted_classes:
                for item in soup.find_all(wanted_tag, wanted_class_):
                    output_snippets.append(item)        
                print('    {0} <{1}> tags with the class "{2}" were retrieved in the file {3}.\n'.format(
                    len(output_snippets), wanted_tag, wanted_class_, html_filename))

    elif wanted_classes == ("",) and wanted_tags != ("",):
        for wanted_tag in wanted_tags:
            for item in soup.find_all(wanted_tag):
                output_snippets.append(item)
            print('    {0} <{1}> tags were retrieved in the file {2}.\n'.format(
                len(output_snippets), wanted_tag, html_filename))

    elif wanted_classes != ("",) and wanted_tags == ("",):
        output_snippets = []
        for wanted_class_ in wanted_classes:
            for tag in soup.find_all():
                if tag.get("class") is not None:
                    if wanted_class_ in tag.get("class"):
                        output_snippets.append(tag)   
            print('    {0} tags with the class "{1}" were retrieved in the file {2}.\n'.format(
                len(output_snippets), wanted_class_, html_filename)) #### Show this only once

    return output_snippets


####################################################################################################

def extract_tags_classes_approximate(html_filename, wanted_tags, wanted_classes):
    """
    Inputs: filename of an html file,
            tuple with tag(s) we want to retrieve,
            tuple with class(es) we want to retrieve.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = filegenerator.file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")
    output_snippets = []
    
    # Get all tags similar to tag
    if wanted_tags != ("",):
        similar_tags = set()
        for tag in soup.find_all():
            for wanted_tag in wanted_tags:
                if wanted_tag in tag.name: similar_tags.add(tag.name)
        print("      Similar tags:", similar_tags)

    # Get all classes similar to class_
    if wanted_classes != ("",):
        classes = get_class_names(html_string)
        similar_classes = set()
        for class_ in classes:
            for wanted_class_ in wanted_classes:
                if wanted_class_ in class_: similar_classes.add(class_)
        print("      Similar classes:", similar_classes)

        print("")
    # Different cases (whether we search classes, tags, both or all)
    
    if wanted_classes != ("",) and wanted_tags != ("",):
        output_snippets = []
        for tag in similar_tags:
            for class_ in similar_classes:
                snippets = soup.find_all(tag, class_)
                print('      {0} <{1}> tags with the class "{2}" were retrieved in the file {3}.\n'.format(
                    len(snippets), tag, class_, html_filename))
                if len(snippets) > 0: # Don't add empty search results
                    for snippet in snippets:
                        output_snippets.append(snippet)

    elif wanted_classes == ("",) and wanted_tags != ("",):
        output_snippets = []
        for tag in similar_tags:
            snippets = soup.find_all(tag)
            print('      {0} <{1}> tags were retrieved in the file {2}.\n'.format(
                len(snippets), tag, html_filename))
            if len(snippets) > 0: # Don't add empty search results
                for snippet in snippets:
                    output_snippets.append(snippet)
            
    elif wanted_classes != ("",) and wanted_tags == ("",):
        output_snippets = []
        for similar_class in similar_classes:
            snippets = soup.find_all(class_=similar_class)
            for snippet in snippets:
                output_snippets.append(snippet)
            
            print('      {0} tags with class "{1}" were retrieved in the file {2}.\n'.format(
                len(output_snippets), similar_class, html_filename))
    
    return output_snippets

####################################################################################################

def extract_all_tags_classes(html_filename):
    """
    Inputs: filename of an html file, tag we want to retrieve, class we want to retrieve.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = filegenerator.file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")

    all_tags = soup.find_all()
    
    output_snippets = []
    
    print('      {0} tags of all types and classes were retrieved in the file {1}.'.format(
        len(all_tags), html_filename))

    for tag in all_tags:
        output_snippets.append(tag)

    return output_snippets
