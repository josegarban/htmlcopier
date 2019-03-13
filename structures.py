"""
Functions to handle data structures (dictionaries, tuples or lists)"
"""

####################################################################################################
# FUNCTIONS TO DESCRIBE LISTS AND DICTIONARIES
####################################################################################################

def print_dictdescription(input_dict, printinstructions = True):
    """
    Input: any dictionary
             printinstructions will let some intermediate stepts to be reported on-screen
    Objective: count the rows in the dictionary and print it.
    Returns: a string describing the dictionary.
    """
    dictdescription_string = "{0} rows found in dictionary: {1}\n".format(len(input_dict), input_dict)
    if printinstructions == True: print(dictdescription_string)

    return dictdescription_string

####################################################################################################

####################################################################################################
# FUNCTIONS TO COMPARE LISTS AND DICTIONARIES
####################################################################################################

def getdictkeys(input_dict, name = "dictionary", printinstructions = True):
    """
    Input: any dictionary and its name (optional)
             printinstructions will let some intermediate stepts to be reported on-screen
    Objective: count the rows in the dictionary and print it.
    Returns: a list containing the dictionary keys.
    """

    # Get the dictionary keys
    dictvalues_list = [x for x in input_dict.keys()]
    if printinstructions == True:
        print("{0} keys found in {1}: {2}\n".format(
            len(dictvalues_list), name, dictvalues_list))

    return dictvalues_list

####################################################################################################

def compare_twolists(list1, list2, list1name = "", list2name = "", printinstructions = True):
    """
    Input: two dictionaries and their names (optional strings),
            printinstructions will let some intermediate stepts to be reported on-screen.
    Objective: comparing two lists.
    Output: tuple of the form (are values the same?, which values are different).
    """

    # Get what is in list1 but not in list2
    list1_notin_list2 = [x for x in list1 if x not in list2]
    if printinstructions == True:
        print("{0} keys found in {2} but not in {3}: {1}\n".format(
            len(list1_notin_list2), list1_notin_list2, list1name, list2name))    
    
    # Get what is in list2 but not in list1
    list2_notin_list1 = [x for x in list2 if x not in list1]
    if printinstructions == True:
        print("{0} keys found in {3} but not in {2}: {1}\n".format(
            len(list2_notin_list1), list2_notin_list1, list1name, list2name))    

    if list1_notin_list2 == [] and list2_notin_list1 == []: same = True
    else: same = False

    return (same, list1_notin_list2, list2_notin_list1)

####################################################################################################

def compare_twodictkeys(dict1, dict2, dict1name = "", dict2name = "", printinstructions = True):
    """
    Input: two dictionaries and their names (optional strings),
            printinstructions will let some intermediate stepts to be reported on-screen.
    Objective: comparing two dictionary keys.
    Output: tuple of the form (are values the same?, which values are different).
    """
    # Get lists with dictionary keys
    dict1keys = getdictkeys(dict1, dict1name, printinstructions)
    dict2keys = getdictkeys(dict2, dict2name, printinstructions)
    
    # Generate names for the dictionary key names to appear on screen
    if dict1name == "": dict1keysname = "dictionary keys"
    else: dict1keysname = dict1name + " keys"
    
    if dict2name == "": dict2keysname = "dictionary keys"
    else: dict2keysname = dict2name + " keys"
    
    dictkey_comparison = compare_twolists(dict1keys, 
                                          dict2keys,
                                          dict1keysname,
                                          dict2keysname,
                                          printinstructions)
    
    dict1keys_notin_dict2keys = dictkey_comparison[1]
    dict2keys_notin_dict1keys = dictkey_comparison[2]

    # Get what is in one dictionary but not in the other
    dict1_notin_dict2 = {x : dict1[x] for x in dict1keys_notin_dict2keys}
    if printinstructions == True:
        print("{0} rows found in {1} but not in {2}:".format(
            len(dict1_notin_dict2), dict1name, dict2name))
        pprint.pprint(dict1_notin_dict2)
        print("")
        
    dict2_notin_dict1 = {x : dict2[x] for x in dict2keys_notin_dict1keys}
    if printinstructions == True:
        print("{0} rows found in {2} but not in {1}:".format(
            len(dict2_notin_dict1), dict1name, dict2name))
        pprint.pprint(dict2_notin_dict1)    
        print("")
        
    if dict1_notin_dict2 == {} and dict2_notin_dict1 == {}: same = True
    else: same = False
    
    return (same, dict1_notin_dict2, dict2_notin_dict1)

