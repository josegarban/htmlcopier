import pprint
import htmlparser
import filegenerator
import userinput
import main
import dbhandler


####################################################################################################
# htmlparser.py tests
####################################################################################################

def test_find_all_classes(html_filename):
    ## Test with class
    print("\n#####################################################################################")
    print("Test to find all classes in a .html file")
    html_string = filegenerator.file_to_string(html_filename)

    test = htmlparser.get_class_names(html_string)
    print(test)
    return None

####################################################################################################

def test_find_all_tags(html_filename):
    ## Test with tags
    print("\n#####################################################################################")
    print("Test to find all tags in a .html file")
    html_string = filegenerator.file_to_string(html_filename)
    
    test = htmlparser.get_tag_names(html_string)
    print(test)
    return None


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

####################################################################################################

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


####################################################################################################
# main.py tests
####################################################################################################

# Possible user inputs
SOURCETYPE_INPUTS = (#("file"    , "alice.html"),
                     ("folder"  , r"C:\Temp"),
                     #("website" , ""),
                     #("database", "")
                     )
SEARCHTYPE_INPUTS = ("Exact",
                     #"Approximate",
                     #"All",
                     #"List"
                     )
TAG_INPUTS        = (("",),
                     #("title",),
                     ("p",),
                     #("a",),
                     #("title", "head")
                     )
CLASS__INPUTS     = (("",),
                     #("story",),
                     #("tory",),
                     ("story", "tory"),
                     )
OUTPUTTYPE_INPUTS = ((".html", "output"),
                     #(".pdf", "output"),
                     #("current.sqlite", "output.sqlite"),
                     #("fresh.sqlite", "output"),
                     )

# Simulated user input through the generation of several dictionaries
def user_input_simulation (sourcetypes,
                           searchtypes,
                           tags       ,
                           classes    ,
                           outputtypes,
                           ):
    """
    Input: Tuples with possible inputs by the user.
    Output: List with dictionaries representing possible user input.
    """
    output_list = []
    
    for sourcetype in sourcetypes:
        for tag in tags:
            for class_ in classes:
                for searchtype in searchtypes:
                    for outputtype in outputtypes:
                        if searchtype == "All" and (class_ != ("",) or tag != ("",)): 
                            True    # Exclude incongruent choice
                        elif searchtype != "All" and (tag == ("",) and class_ == ("",)):
                            True    # Exclude incongruent choice
                        else:
                            output_list.append({"sourcetype": sourcetype,
                                                "tag"       : tag,
                                                "class_"    : class_,
                                                "searchtype": searchtype,
                                                "outputtype": outputtype
                                                })
    
    print("Generated {0} possible user inputs".format(len(output_list)))

    return output_list

####################################################################################################

def test_main():
    """
    Uses simulated input to create multiple search patterns
    """
    print("\n#####################################################################################")
    print("Testing valid user search requests")
    test = user_input_simulation(SOURCETYPE_INPUTS,
                                 SEARCHTYPE_INPUTS,
                                 TAG_INPUTS,
                                 CLASS__INPUTS,
                                 OUTPUTTYPE_INPUTS,
                                 )
    for condition in test: print(condition)
    
    for condition in test:
        index = test.index(condition) + 1
        print("\n\nTest", index, "/", len(test), condition)
        result = main.main(condition)
        print(type(result), len(result))
        pprint.pprint(result)
    return None
    

####################################################################################################
# filegenerator.py tests
####################################################################################################

TEXT    = "sampletest.txt"
CLASSES = "classlist.txt"
TAGS    = "taglist.txt"

def test_filegenerator():
    print("""
    TEXT    = "sampletest.txt"
    CLASSES = "classlist.txt"
    TAGS    = "taglist.txt"
    """)
    test    = filegenerator.txt_to_list(CLASSES)
    print(type(test))
    test    = filegenerator.txt_to_list(TAGS)
    print(type(test))

    return None

####################################################################################################
# userinput.py tests
####################################################################################################

def test_userinput():
    pprint.pprint(userinput.choose_primary_mode())


####################################################################################################
# dbhandler.py tests
####################################################################################################

MY_DICT = {"001": {"Name": "Ann"    , "Age": 88, "Russian": True },
           "002": {"Name": "Maya"   , "Age": 86, "Russian": False},
           "003": {"Name": "John"   , "Age": 90, "Russian": False},
           "004": {"Name": "Nadia"  , "Age": 87, "Russian": True },
           "005": {"Name": "Russell", "Age": 77, "Russian": False},
           "006": {"Name": "Hiroko" , "Age": 60, "Russian": False},
           "007": {"Name": "Arkady" , "Age": 71, "Russian": True },
           }
MY_SQLFILENAME = "martians.sqlite"
MY_SQLTABLE    = "First_Hundred"

####################################################################################################

def test_instruction_typing(input_dict):

    print("Testing categorizing fields in a nested dictionary...")
    test1 = dbhandler.dictfieldnames_to_tuplist(input_dict)
    print("The previous line should show a list of tuples describing database fields.")
    print(test1)
    print("")
    
    print("Testing categorizing fields in a nested dictionary...")
    test2 = dbhandler.dictfields_to_string(input_dict)
    print(test2)
    print("The previous line should show a tuple of strings describing database fields.")
    print("")
    
    return None

####################################################################################################

def test_manipulation(input_dict, sqlfilename, sqltable):
    print("Testing table creation from a nested dictionary...")
    test1 = dbhandler.create_table(input_dict, sqlfilename, sqltable)
    print("")
    
    print("Testing data insertion in database...")
    test2 = dbhandler.fill_table(MY_DICT, MY_SQLFILENAME, MY_SQLTABLE)
    print("")
    
    return None


####################################################################################################
# RUN ALL TESTS
####################################################################################################
## Uncomment to test:

## Test actual script
#pprint.pprint(main.main(""))

# htmlparser.py tests
ALICE = "alice.html"
#test_find_all_classes(ALICE)
#test_find_all_tags(ALICE)
#test_extract_tags_classes_exact(ALICE,"p","story")
#test_extract_tags_classes_approximate(ALICE,"p","tory")

# main.py tests
#test_main()

# filegenerator.py tests
#test_filegenerator()

# userinput.py tests
#test_userinput()

# dbhandler.py tests
test_instruction_typing(MY_DICT)
test_manipulation(MY_DICT, MY_SQLFILENAME, MY_SQLTABLE)

