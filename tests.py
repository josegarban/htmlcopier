import pprint
import htmlparser
import filegenerator
import userinput
import main
import dbhandler
import structures

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
    htmlparser.extract_tags_classes_exact(file, tag, class_)
    
    print("\n2. Tag but no class:")
    htmlparser.extract_tags_classes_exact(file, tag, "")

    print("\n3. Class but no tag:")
    htmlparser.extract_tags_classes_exact(file, "", class_)

    print("\n4. No tag and no class:")
    htmlparser.extract_tags_classes_exact(file, "", "")    

    return None

####################################################################################################

def test_extract_tags_classes_approximate(file, tag, class_):    
    print("\n#####################################################################################")
    print("Testing approximate tag and class extraction")
    print("\n1. Both tag and class:")
    htmlparser.extract_tags_classes_approximate(file, tag, class_)
    
    print("\n2. Tag but no class:")
    htmlparser.extract_tags_classes_approximate(file, tag, "")

    print("\n3. Class but no tag:")
    htmlparser.extract_tags_classes_approximate(file, "", class_)

    print("\n4. No tag and no class:")
    htmlparser.extract_tags_classes_approximate(file, "", "")    

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
SEARCHTYPE_INPUTS = (#"Exact",
                     #"Approximate",
                     #"All",
                     "List"
                     )
TAG_INPUTS        = (("",),
                     ("title",),
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

MY_DICT = {"001": {"Name": "Ann"    , "Age": 0, "Russian": True },
           "002": {"Name": "Maya"   , "Age": 86, "Russian": False},
           "003": {"Name": "John"   , "Age": 90, "Russian": False},
           "004": {"Name": "Nadia"  , "Age": 87, "Russian": True },
           "005": {"Name": "Russell", "Age": 77, "Russian": False},
           "006": {"Name": "Hiroko" , "Age": 60, "Russian": False},
           "007": {"Name": "Arkady" , "Age": 71, "Russian": True },
           }
MY_DICTALT = {"001": {"Name": "Ann"    , "Age": 88, "Russian": True },
              "002": {"Name": "Maya"   , "Age": 86, "Russian": False},
              "003": {"Name": "John"   , "Age": 90, "Russian": False},
              "004": {"Name": "Nadia"  , "Age": 87, "Russian": True },
              "005": {"Name": "Russell", "Age": 77, "Russian": False},
              "006": {"Name": "Hiroko" , "Age": 60, "Russian": False},
              "008": {"Name": "Kasei"  , "Age": 25, "Russian": False},
             }
MY_SQLFILENAME = "martians.sqlite"
MY_SQLTABLE    = "First_Hundred"

HTMLDICT = {'alice - Copie.html': [{'class': ['story'],
                         'contents': '<p class="story">Once upon a time there were three little sisters; and their names were    <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,    <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and    <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;    and they lived at the bottom of a well.</p>',
                         'source': 'C:\\Temp\\alice - Copie.html',
                         'tag': 'p'},
                        {'class': ['story'],
                         'contents': '<p class="story">...</p>',
                         'source': 'C:\\Temp\\alice - Copie.html',
                         'tag': 'p'}],
 'alice.html': [{'class': ['story'],
                 'contents': '<p class="story">Once upon a time there were three little sisters; and their names were    <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,    <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and    <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;    and they lived at the bottom of a well.</p>',
                 'source': 'C:\\Temp\\alice.html',
                 'tag': 'p'},
                {'class': ['story'],
                 'contents': '<p class="story">...</p>',
                 'source': 'C:\\Temp\\alice.html',
                 'tag': 'p'}]}

####################################################################################################

def test_instruction_typing(input_dict):

    print("Testing categorizing fields in a nested dictionary...")
    print(dbhandler.dictfieldnames_to_tuplist(input_dict))
    print("The previous line should show a list of tuples describing database fields.")
    print("")
    
    print("Testing categorizing fields in a nested dictionary...")
    print(dbhandler.dictfields_to_string(input_dict))
    print("The previous line should show a tuple of strings describing database fields.")
    print("")
    
    return None

####################################################################################################

def test_manipulation(input_dict, sqlfilename, sqltable):
    print("Testing table creation from a nested dictionary...")
    dbhandler.create_table(input_dict, sqlfilename, sqltable)
    print("")
    
    print("Testing data insertion in database...")
    dbhandler.add_dbrows(MY_DICT, MY_SQLFILENAME, MY_SQLTABLE)
    print("")

    print("Testing simple key comparison between a dictionary and a database created from that same dictionary...")
    dbhandler.compare_keysonly(MY_DICT, MY_SQLFILENAME, MY_SQLTABLE)

    print("Testing simple key comparison between a dictionary and a database created from another dictionary...")
    dbhandler.compare_keysonly(MY_DICTALT, MY_SQLFILENAME, MY_SQLTABLE)

    print("Testing full key comparison between a dictionary and a database created from that same dictionary...")
    dbhandler.compare_keysfull(MY_DICT, MY_SQLFILENAME, MY_SQLTABLE)

    print("Testing full key comparison between a dictionary and a database created from another dictionary...")
    dbhandler.compare_keysfull(MY_DICTALT, MY_SQLFILENAME, MY_SQLTABLE)

    print("Testing row comparison between a dictionary and a database created from that same dictionary...")
    dbhandler.compare_rowsfull(MY_DICT, MY_SQLFILENAME, MY_SQLTABLE)

    print("Testing row comparison between a dictionary and a database created from another dictionary...")
    dbhandler.compare_rowsfull(MY_DICTALT, MY_SQLFILENAME, MY_SQLTABLE)

    print("Testing updating database from changes in dictionary...")
    dbhandler.update_dict_to_db(MY_DICTALT, MY_SQLFILENAME, MY_SQLTABLE)
    
    return None

####################################################################################################
def test_structures(input_dict):
    
    print("Testing conversion of a structure of the form dictionary → list to dictionary → dictionary")
    converted = structures.dictlist_to_dictdict(input_dict)
    pprint.pprint(converted)
    print("")
    
    print("Flattening a structure of the form dictionary → dictionary → dictionary to dictionary → dictionary")
    flattened = structures.flatten_dictdictdict(converted)
    pprint.pprint(flattened)
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
#test_instruction_typing(MY_DICT)
#test_manipulation(MY_DICT, MY_SQLFILENAME, MY_SQLTABLE)

# structures.py tests
test_structures(HTMLDICT)
