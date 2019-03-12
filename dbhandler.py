"""
Sqlite functions
"""

import sqlite3
import userinput

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

def create_table(input_dict, sql_filename = "", sql_table = ""):
    """
    Inputs: filename, table that will be updated or created, and a dictionary.
            The table won't be created if it already exists.
    Objective: a table in a sql table will be created but not filled with data,
            based on the dictionary.
    Outputs: none.
    """

    # Get the filename if none has been set
    if sql_filename == "": sql_filename = userinput.input_filename()    
    if sql_table    == "": sql_table = input("Insert table name:")

    # Open the Sqlite database we're going to use (my_cursor)
    my_connector = sqlite3.connect(sql_filename)
    my_cursor    = my_connector.cursor()    

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
    Outputs: none."""

    # Get the filename if none has been set
    if sql_filename == "": sql_filename = userinput.input_filename()    
    if sql_table    == "": sql_table = input("Insert table name:")

    # Open the Sqlite database we're going to use (my_cursor)
    my_connector   = sqlite3.connect(sql_filename)
    my_cursor      = my_connector.cursor()    

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

    my_connector.commit()
    return None


####################################################################################################

