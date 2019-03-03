import pprint
import htmlparser
import main

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

## Uncomment to test:
#test_find_all_classes(ALICE)
#test_find_all_tags(ALICE)

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

## Uncomment to test:
#test_extract_tags_classes_exact(ALICE,"p","story")
#test_extract_tags_classes_approximate(ALICE,"p","tory")


####################################################################################################
# main.py tests
####################################################################################################

# Possible user inputs
SOURCETYPE_INPUTS = ("file", "folder", "website", "database")
SEARCHTYPE_INPUTS = ("Single", "Approximate", "All", "List")
TAG_INPUTS        = ("title", "p", "a")
CLASS__INPUTS     = ("story", "tory")

# Simulated user input through the generation of several dictionaries
def user_input_simulation (sourcetypes,
                           tags       ,
                           classes    , 
                           searchtypes):
    """
    Input: Tuples with possible inputs by the user.
    Output: List with dictionaries representing possible user input.
    """
    output_list = []
    
    innerdict = {"sourcetype": None,
                 "tag"       : None,
                 "class_"    : None,
                 "searchtype": None,
         }
    
    for sourcetype in sourcetypes:
        for tag in tags:
            for class_ in classes:
                for searchtype in searchtypes:
                    output_list.append({"sourcetype": sourcetype,
                                        "tag"       : tag,
                                        "class_"    : class_,
                                        "searchtype": searchtype
                                        })

    print("Generated {0} possible user inputs".format(len(output_list)))
    return output_list

## Uncomment to test:
test = user_input_simulation(SOURCETYPE_INPUTS, SEARCHTYPE_INPUTS, TAG_INPUTS, CLASS__INPUTS)
#pprint.pprint(test)

main.main(test[0])

####################################################################################################
