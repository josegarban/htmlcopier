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

def extract_tags_classes_exact(html_filename, wanted_tags, wanted_classes, file_index = 0):
    """
    Inputs: filename of an html file,
            tuple with tag(s) we want to retrieve,
            tuple with class(es) we want to retrieve,
            file index of the file within a file list, if applicable.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = filegenerator.file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")
    output_snippets = []
    all_tags_list = list(soup.find_all())
    
    if wanted_classes != ("",) and wanted_tags != ("",):
        for wanted_tag in wanted_tags:
            for wanted_class_ in wanted_classes:
                applicable_tags = soup.find_all(wanted_tag, wanted_class_)                        
                for item in applicable_tags:
                    snippet = {}
                    snippet["given_path"] = html_filename
                    snippet["tag"] = item.name
                    if item.get("class") is not None: snippet["class"] = str(item.get("class"))
                    else: snippet["class"] = None
                    snippet["contents"] = str(item)
                    if item.get("href") is not None: snippet["href"] = str(item.get("href"))
                    else: snippet["href"] = None
                    snippet["file_index"] = file_index
                    snippet["pos_index"]  = all_tags_list.index(item)
                    
                    # No plans to fully use RMDB yet, various data types will be converted to text

                    if snippet not in output_snippets: output_snippets.append(snippet)

                print('    {0} <{1}> tags with the class "{2}" were retrieved in the file {3}.\n'.format(
                    len(output_snippets), wanted_tag, wanted_class_, html_filename))

    elif wanted_classes == ("",) and wanted_tags != ("",):
        for wanted_tag in wanted_tags:
            applicable_tags = soup.find_all(wanted_tag)                        
            for item in applicable_tags:
                snippet = {}
                snippet["given_path"] = html_filename
                snippet["tag"] = item.name
                if item.get("class") is not None: snippet["class"] = str(item.get("class"))
                else: snippet["class"] = None
                snippet["contents"] = str(item)
                if item.get("href") is not None: snippet["href"] = str(item.get("href"))
                else: snippet["href"] = None
                snippet["file_index"] = file_index
                snippet["pos_index"]  = all_tags_list.index(item)
                    
                # No plans to fully use RMDB yet, various data types will be converted to text
                   
                if snippet not in output_snippets: output_snippets.append(snippet)

            print('    {0} <{1}> tags were retrieved in the file {2}.\n'.format(
                len(output_snippets), wanted_tag, html_filename))

    elif wanted_classes != ("",) and wanted_tags == ("",):
        all_tags = soup.find_all()
        for wanted_class_ in wanted_classes:
            for item in all_tags:
                if item.get("class") is not None and wanted_class_ in item.get("class"):
                    snippet = {}
                    snippet["given_path"] = html_filename
                    snippet["tag"] = item.name
                    if item.get("class") is not None: snippet["class"] = str(item.get("class"))
                    else: snippet["class"] = None
                    snippet["contents"] = str(item)
                    if item.get("href") is not None: snippet["href"] = str(item.get("href"))
                    else: snippet["href"] = None
                    snippet["file_index"] = file_index
                    snippet["pos_index"]  = all_tags_list.index(item)
                    
                    # No plans to fully use RMDB yet, various data types will be converted to text

                    if snippet not in output_snippets: output_snippets.append(snippet)

            print('    {0} tags with the class "{1}" were retrieved in the file {2}.\n'.format(
                len(output_snippets), wanted_class_, html_filename)) #### Show this only once

    return output_snippets


####################################################################################################

def extract_tags_classes_approximate(html_filename, wanted_tags, wanted_classes, file_index = 0):
    """
    Inputs: filename of an html file,
            tuple with tag(s) we want to retrieve,
            tuple with class(es) we want to retrieve,
            file index of the file within a file list, if applicable.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = filegenerator.file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")
    output_snippets = []
    all_tags_list = list(soup.find_all())

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
        for similar_tag in similar_tags:
            for similar_class_ in similar_classes:
                applicable_tags = soup.find_all(similar_tag, similar_class_)
                
                if len(similar_classes) > 0 and len(similar_tags) > 0: # Don't add empty search results
                    if len(similar_classes) > 0:
                        for item in applicable_tags:
                            snippet = {}
                            snippet["given_path"] = html_filename
                            snippet["tag"] = item.name
                            if item.get("class") is not None: snippet["class"] = str(item.get("class"))
                            else: snippet["class"] = None
                            snippet["contents"] = str(item)
                            if item.get("href") is not None: snippet["href"] = str(item.get("href"))
                            else: snippet["href"] = None
                            snippet["file_index"] = file_index
                            snippet["pos_index"]  = all_tags_list.index(item)
                            
                            # No plans to fully use RMDB yet, various data types will be converted to text
                    
                            if snippet not in output_snippets: output_snippets.append(snippet)
                print('      {0} <{1}> tags with the class "{2}" were retrieved in the file {3}.\n'.format(
                    len(output_snippets), similar_tag, similar_class_, html_filename))
                
    elif wanted_classes == ("",) and wanted_tags != ("",):
        for tag in similar_tags:
            applicable_tags = soup.find_all(tag)
            if len(similar_tags) > 0: # Don't add empty search results
                for item in applicable_tags:
                    snippet = {}
                    snippet["given_path"] = html_filename
                    snippet["tag"] = item.name
                    if item.get("class") is not None: snippet["class"] = str(item.get("class"))
                    else: snippet["class"] = None
                    snippet["contents"] = str(item)
                    if item.get("href") is not None: snippet["href"] = str(item.get("href"))
                    else: snippet["href"] = None
                    snippet["file_index"] = file_index
                    snippet["pos_index"]  = all_tags_list.index(item)
                    # No plans to fully use RMDB yet, various data types will be converted to text
                    
                    if snippet not in output_snippets: output_snippets.append(snippet)
            print('      {0} <{1}> tags were retrieved in the file {2}.\n'.format(
                len(output_snippets), tag, html_filename))
            
    elif wanted_classes != ("",) and wanted_tags == ("",):
        for similar_class in similar_classes:
            applicable_tags = soup.find_all(class_=similar_class)
            if len(similar_classes) > 0:
                for item in applicable_tags:
                    snippet = {}
                    snippet["given_path"] = html_filename
                    snippet["tag"] = item.name
                    if item.get("class") is not None: snippet["class"] = str(item.get("class"))
                    else: snippet["class"] = None
                    snippet["contents"] = str(item)
                    if item.get("href") is not None: snippet["href"] = str(item.get("href"))
                    else: snippet["href"] = None
                    snippet["file_index"] = file_index
                    snippet["pos_index"]  = all_tags_list.index(item)
                    # No plans to fully use RMDB yet, various data types will be converted to text

                    if snippet not in output_snippets: output_snippets.append(snippet)
            
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
    all_tags_list = list(soup.find_all())
    
    output_snippets = []
    
    print('      {0} tags of all types and classes were retrieved in the file {1}.'.format(
        len(all_tags), html_filename))

    for item in all_tags:
        snippet = {}
        snippet["given_path"] = html_filename
        snippet["tag"] = item.name
        if item.get("class") is not None: snippet["class"] = str(item.get("class"))
        else: snippet["class"] = None
        snippet["contents"] = str(item)
        if item.get("href") is not None: snippet["href"] = str(item.get("href"))
        else: snippet["href"] = None
        snippet["file_index"] = file_index
        snippet["pos_index"]  = all_tags_list.index(item)
        # No plans to fully use RMDB yet, various data types will be converted to text

        if snippet not in output_snippets: output_snippets.append(snippet)

    return output_snippets
