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
            if type(outer_key) is int: primary_keyistext = False
        except:
            primary_keyistext = True
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
# FUNCTIONS TO COMPARE DICTIONARIES AND TABLES
####################################################################################################

def compare_keysonly(input_dict,
                     sql_filename = "",
                     sql_table = "",
                     dbkey_column = "id",
                     printinstructions = True):
    """
    Inputs: filename, table that will opened, and a dictionary.
            The column in the database table is assumed to be called "id",
            but this can be changed at the input level.
            Intermediate steps are reported or not, according to printinstructions.
    Objective: compare keys in the dictionary against values in the table.
    Outputs: tup of the form (are values the same?, which values are different).
    """

    # Open the database and get the table name if none has been set
    my_connector = create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to get the keys in the database
    instruction    = """SELECT id FROM {1}""".format(
        dbkey_column, sql_table)                 

    # Execute the instruction
    my_cursor.execute(instruction)
    dbvalues_tups = my_cursor.fetchall()
    dbvalues_list = [x[0] for x in dbvalues_tups]
    if printinstructions == True:
        print("Instruction executed: {0} in {1}.\n{2} keys found in database: {3}\n".format(
            instruction, sql_filename, len(dbvalues_list), dbvalues_list))    

    # Get the dictionary keys
    dictvalues_list = [x for x in input_dict.keys()]
    if printinstructions == True:
        print("{0} keys found in dictionary: {1}\n".format(
            len(dictvalues_list), dictvalues_list))    

    # Get what is in one list but not in the other
    dictvalues_not_indb = [x for x in dictvalues_list if x not in dbvalues_list]
    if printinstructions == True:
        print("{0} keys found in dictionary but not in database: {1}\n".format(
            len(dictvalues_not_indb), dictvalues_not_indb))    
    dbvalues_not_indict = [x for x in dbvalues_list if x not in dictvalues_list]
    if printinstructions == True:
        print("{0} keys found in database but not in dictionary: {1}\n".format(
            len(dbvalues_not_indict), dbvalues_not_indict))    

    if dictvalues_not_indb == [] and dbvalues_not_indict == []: same = True
    else: same = False
    
    return (same, dictvalues_not_indb, dbvalues_not_indict)

####################################################################################################

def compare_keysfull(input_dict,
                     sql_filename = "",
                     sql_table = "",
                     dbkey_column = "id",
                     printinstructions = True):
    """
    Inputs: filename, table that will opened, and a dictionary.
            The column in the database table is assumed to be called "id",
            but this can be changed at the input level.
            Intermediate steps are reported or not, according to printinstructions.
    Objective: compare keys in the dictionary against values in the table.
            However, different values besides "id" are not compared.
    Outputs: tup of the form (are values the same?, which values are different).
    """

    # Open the database and get the table name if none has been set
    my_connector = create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to get the keys in the database
    instruction    = """SELECT * FROM {0}""".format(
        sql_table)                 

    # Execute the instruction
    dbvalues_tups = [x for x in my_cursor.execute(instruction)]
    db_colnames   = [x[0] for x in my_cursor.description]

    #Find the index of the key (probably "id") in the database table
    keycol_index  = db_colnames.index(dbkey_column)
    
    # Convert the tuples from the database into a dictionary of the form {"id" {"values": values}}
    db_dict = {}
    for tup in dbvalues_tups:
        db_dict[tup[keycol_index]] = {}
        for col in db_colnames:
            if col != dbkey_column:
                # key column (probably "id") is outside the inner dictionary
                db_dict[tup[keycol_index]][col] = tup[db_colnames.index(col)]
    
    if printinstructions == True:
        print("Instruction executed: {0} in {1}.\n{2} rows found in database: {3}\n".format(
            instruction, sql_filename, len(db_dict), db_dict))    

    # Get the dictionary keys
    if printinstructions == True:
        print("{0} rows found in dictionary: {1}\n".format(
            len(input_dict), input_dict))    

    # Get what is in one list but not in the other
    key_comparison = compare_keysonly(input_dict, sql_filename, sql_table, dbkey_column, False)
    dictkeys_not_indb = key_comparison[1]
    dbkeys_not_indict = key_comparison[2]

    # Get what is in one dictionary but not in the other
    dictvalues_not_indb = {x : input_dict[x] for x in dictkeys_not_indb}
    if printinstructions == True:
        print("{0} rows found in dictionary but not in database:".format(
            len(dictvalues_not_indb)))
        pprint.pprint(dictvalues_not_indb)
        print("")
    dbvalues_not_indict = {x : db_dict[x] for x in dbkeys_not_indict}
    
    if printinstructions == True:
        print("{0} rows found in database but not in dictionary:".format(
            len(dbvalues_not_indict)))
        pprint.pprint(dbvalues_not_indict)    
        print("")
        
    if dictvalues_not_indb == {} and dbvalues_not_indict == {}: same = True
    else: same = False
    
    return (same, dictvalues_not_indb, dbvalues_not_indict)

