"""
Sqlite functions
"""

import sqlite3
import userinput
import pprint

####################################################################################################
# INSTRUCTION CREATION 
####################################################################################################

def dictfieldnames_to_tuplist(input_dict):
    """
    Inputs: dictionary.
    Objective: gets fields in a dictionary and converts them to a list.
            Supports cases when different items in a dictionary don't all have the same fields.
    Returns: list containing tuples of the form (fieldname, fieldtype)
    """
    output_list = []
    
    # Check if the primary key is an integer or a string
    primarykey_istext = True
    for outer_key in input_dict.keys():
        try:
            if type(outer_key) is int: primarykey_istext = False
        except:
            primarykey_istext = True
            continue # At the first sight of a non-integer key, the loop will end
    
    if   primarykey_istext: output_list.append(("id", "VARCHAR(32) PRIMARY KEY"))
    else                  : output_list.append(("id", "INTEGER PRIMARY KEY"))
    
    # Search all inner dictionaries in a dictionary
    for outer_key in input_dict:  # It should not matter if the dictionary contains dictionaries or a list            
        for inner_key in input_dict[outer_key]:
            fieldname = str(inner_key)
        
            if   type(input_dict[outer_key][inner_key]) is int  : fieldtype = "INTEGER"
            elif type(input_dict[outer_key][inner_key]) is str  : fieldtype = "TEXT"
            elif type(input_dict[outer_key][inner_key]) is bool : fieldtype = "BINARY"
            elif type(input_dict[outer_key][inner_key]) is float: fieldtype = "REAL"
        
            if   (fieldname, fieldtype) not in output_list : output_list.append((fieldname, fieldtype))
    
    return output_list

####################################################################################################

def dictfieldnames_to_tup(input_dict):
    """
    Inputs: dictionary.
    Objective: gets fields in a dictionary and converts them to a list.
            Supports cases when different items in a dictionary don't all have the same fields.
    Returns: tuple containing fieldnames only
    """
    fieldfullinfo = dictfieldnames_to_tuplist(input_dict)
    fieldnames = [x[0] for x in fieldfullinfo]
    
    return tuple(fieldnames)

####################################################################################################

def dictfields_to_string(input_dict):
    """
    Inputs: dictionary.
    Objective: gets fields in a dictionary and converts them
                to a string representation of a list for use in SQL instructions.
    Returns: string.
    """
    # Field_list is a list containing tuples of the form (fieldname, fieldtype)
    field_list = dictfieldnames_to_tuplist(input_dict)
    
    output_string = ""
    for field_tup in field_list:
        field_string = "{0} {1}, ".format(field_tup[0], field_tup[1])
        output_string = output_string + field_string
    output_string = "(" + output_string[:-2] + ")" # -2 to remove the last comma and space
    
    return output_string

####################################################################################################

def dictfieldnames_to_string(input_dict):
    """
    Inputs: dictionary.
    Objective: gets field names in a dictionary and converts them
                to a string representation of a list for use in SQL instructions.
    Returns: string.
    """
    # Field_list is a list containing tuples of the form (fieldname, fieldtype)
    field_list = dictfieldnames_to_tuplist(input_dict)
    
    output_string = ""
    for field_tup in field_list:
        field_string = "{0}, ".format(field_tup[0])
        output_string = output_string + field_string
    output_string = "(" + output_string[:-2] + ")" # -2 to remove the last comma and space
    
    return output_string

####################################################################################################
# SQL MANIPULATION 
####################################################################################################

def create_connector(sql_filename = ""):
    """
    Inputs: filename or path.
    Objective: open the sqlite database.
    Outputs: connector.
    """

    # Get the filename if none has been set
    if sql_filename == "": sql_filename = userinput.input_filename()    

    # Open the Sqlite database we're going to use (my_cursor)
    my_connector = sqlite3.connect(sql_filename)

    return my_connector

####################################################################################################

def create_table(input_dict, sql_filename = "", sql_table = ""):
    """
    Inputs: filename, table that will be updated or created, and a dictionary.
            The table won't be created if it already exists.
    Objective: a table in a sql table will be created but not filled with data,
            based on the dictionary.
    Outputs: none.
    """

    # Open the database and get the table name if none has been set
    my_connector = create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to create the table 
    fieldnames = dictfields_to_string(input_dict)
    instruction = """CREATE TABLE IF NOT EXISTS {0} {1}""".format(sql_table, fieldnames)
    
    # Create the table
    my_cursor.execute(instruction)
    print("Instruction executed:", instruction)

    return None

####################################################################################################

def fill_table(input_dict, sql_filename = "", sql_table = ""):
    """
    Inputs: filename, table that will be updated or created, and a dictionary.
            The table won't be created if it already exists.
    Objective: a table in a sql table will be filled with data,
                or edited if existing, from a dictionary.
    Outputs: none.
    """

    # Open the database and get the table name if none has been set
    my_connector = create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to create the table
    fields_list    = dictfieldnames_to_tup(input_dict)
    fieldnames_str = dictfieldnames_to_string(input_dict)
    questionmarks  = "(" + (("?, ")*len(fields_list))[:-2] + ")"
    instruction    = """INSERT OR IGNORE INTO {0} {1} VALUES {2}""".format(
        sql_table, fieldnames_str, questionmarks)                 

    # Get the values in the instruction
    for outer_key in input_dict:    
        values     = [outer_key] # This is the id
        for value in input_dict[outer_key].values():
            values.append(value)
        
    # Execute the instruction
        my_cursor.execute(instruction, tuple(values))
        print("Instruction executed: {0} in {1}.\nValues: {2}\n".format(
            instruction, sql_filename, tuple(values)))    

    # Commit the changes
    my_connector.commit()
    return None


####################################################################################################
# FUNCTIONS TO DESCRIBE AND COMPARE LISTS AND DICTIONARIES
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


    
####################################################################################################
# FUNCTIONS TO COMPARE DATA IN A DICTIONARY AND DATA IN A TABLE DATABASE
####################################################################################################

def get_alldbkeys(sql_filename = "",
                  sql_table = "",
                  dbkey_column = "id",
                  printinstructions = True):
    """
    Inputs: filename,
            table that will opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: get all keys in a database table.
    Outputs: list with keys in the database table.
    """

    # Open the database and get the table name if none has been set
    my_connector  = create_connector(sql_filename)
    my_cursor     = my_connector.cursor()
    if sql_table  == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to get the keys in the database
    instruction   = """SELECT {0} FROM {1}""".format(dbkey_column, sql_table)                 

    # Execute the instruction to get a tuple for each table row
    my_cursor.execute(instruction)
    dbvalues_tups = my_cursor.fetchall()
    
    # Create and report the output
    output_list   = [x[0] for x in dbvalues_tups]
    if printinstructions == True:
        print("Instruction executed: {0} in {1}.\n{2} keys found in database: {3}\n".format(
            instruction, sql_filename, len(output_list), output_list))    

    return output_list

####################################################################################################

def get_alldbrows(sql_filename = "",
                  sql_table = "",
                  dbkey_column = "id",
                  printinstructions = True):
    """
    Inputs: filename,
            table that will opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: get all values in a database table.
    Outputs: nested dictionary of the form { id value: {"column name": column value}...}.
    """
    # Open the database and get the table name if none has been set
    my_connector  = create_connector(sql_filename)
    my_cursor     = my_connector.cursor()
    if sql_table  == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to get the keys in the database
    instruction   = """SELECT * FROM {0}""".format(sql_table)                 

    # Execute the instruction
    dbvalues_tups = [x for x in my_cursor.execute(instruction)]

    #Find the index of the key (probably "id") in the database table
    db_colnames   = [x[0] for x in my_cursor.description]
    keycol_index  = db_colnames.index(dbkey_column)
    
    # Convert the tuples from the database into a dictionary of the form {"id" {"values": values}}
    output_dict = {}
    for tup in dbvalues_tups:
        output_dict[tup[keycol_index]] = {}
        for col in db_colnames:
            if col != dbkey_column: # key column (probably "id") is outside the inner dictionary
                output_dict[tup[keycol_index]][col] = tup[db_colnames.index(col)]
    
    # Report the output
    if printinstructions == True:
        print("Instruction executed: {0} in {1}.\n{2} rows found in database: {3}\n".format(
            instruction, sql_filename, len(output_dict), output_dict))    
    
    return output_dict
    
####################################################################################################

def compare_keysonly(input_dict,
                     sql_filename = "",
                     sql_table = "",
                     dbkey_column = "id",
                     printinstructions = True):
    """
    Inputs: dictionary that will be compared with the database,
            filename,
            table that will opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: compare keys in the dictionary against values in the table.
    Outputs: tuple of the form (are values the same?, which values are different).
    """

    # Get the keys in the dictionary and in the database table
    dictvalues_list = getdictkeys(input_dict)        
    dbvalues_list = get_alldbkeys(sql_filename, sql_table, dbkey_column, printinstructions)

    # Get what is in one list but not in the other
    actual_comparison = compare_twolists(dictvalues_list, dbvalues_list, "dictionary", "database", printinstructions)
    
    return actual_comparison

####################################################################################################

def compare_keysfull(input_dict,
                     sql_filename = "",
                     sql_table = "",
                     dbkey_column = "id",
                     printinstructions = True):
    """
    Inputs: dictionary that will be compared with the database,
            filename,
            table that will opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: compare keys in the dictionary against values in the table.
            However, different values besides "id" are not compared.
    Outputs: tup of the form (are values the same?, which values are different).
    """

    # Convert the table into a dictionary to compare with input_dict
    db_dict = get_alldbrows(sql_filename, sql_table, dbkey_column, printinstructions)

    # Describe the dictionary
    print_dictdescription(input_dict, printinstructions)    

    # Compare the dictionary
    actual_comparison = compare_twodictkeys(input_dict, db_dict, "input dictionary", "database dictionary")
    
    return actual_comparison

####################################################################################################

def compare_rowsfull(input_dict,
                     sql_filename = "",
                     sql_table = "",
                     dbkey_column = "id",
                     printinstructions = True):
    """
    Inputs: dictionary that will be compared with the database,
            filename,
            table that will opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: compare full rows in the dictionary against values in the table.
            Values other than "id" are compared.
    Outputs: tup of the form (are rows the same?, which rows are different).
    """

    # Convert the table into a dictionary to compare with input_dict
    db_dict = get_alldbrows(sql_filename, sql_table, dbkey_column, printinstructions)

    # Describe the dictionary
    print_dictdescription(input_dict, printinstructions)    

    
    
    return (same, dictvalues_not_indb, dbvalues_not_indict)

