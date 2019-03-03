import htmlparser

####################################################################################################
# htmlparser.py tests
####################################################################################################

ALICE = "alice.html"

####################################################################################################

def test_find_all_classes(html_filename):
    ## Test with class
    print("\n#####################################################################################")
    print("Test to find all classes in a .html file")
    html_string = htmlparser.file_to_string(html_filename)

    test = htmlparser.get_class_names(html_string)
    print(test)
    return None

def test_find_all_tags(html_filename):
    ## Test with tags
    print("\n#####################################################################################")
    print("Test to find all tags in a .html file")
    html_string = htmlparser.file_to_string(html_filename)
    
    test = htmlparser.get_tag_names(html_string)
    print(test)
    return None

test_find_all_classes(ALICE)
test_find_all_tags(ALICE)

####################################################################################################

def test_extract_tags_classes_exact(file, tag, class_):
    print("\n#####################################################################################")
    print("Testing exact tag and class extraction")
    print("\n1. Both tag and class:")
    test = htmlparser.extract_tags_classes_exact(file, tag, class_)
    
    print("\n2. Tag but no class:")
    test = htmlparser.extract_tags_classes_exact(file, tag, "")

    print("\n3. Class but no tag:")
    test = htmlparser.extract_tags_classes_exact(file, "", class_)

    print("\n4. No tag and no class:")
    test = htmlparser.extract_tags_classes_exact(file, "", "")    

    return None


def test_extract_tags_classes_approximate(file, tag, class_):    
    print("\n#####################################################################################")
    print("Testing approximate tag and class extraction")
    print("\n1. Both tag and class:")
    test = htmlparser.extract_tags_classes_approximate(file, tag, class_)
    
    print("\n2. Tag but no class:")
    test = htmlparser.extract_tags_classes_approximate(file, tag, "")

    print("\n3. Class but no tag:")
    test = htmlparser.extract_tags_classes_approximate(file, "", class_)

    print("\n4. No tag and no class:")
    test = htmlparser.extract_tags_classes_approximate(file, "", "")    

    return None

test_extract_tags_classes_exact(ALICE,"p","story")
test_extract_tags_classes_approximate(ALICE,"p","tory")

