import pprint
from bs4 import BeautifulSoup

####################################################################################################

def txt_to_string (filename):
    """
        Input: filename
        Objective: open a file and return a string, to be handled in-memory
        Output: string 
    """
    output_string = ""
    
    try:        
        with open(filename, "r") as myfile:
            for line in myfile:
                output_string = output_string + line    
                print("\n{0} was successfully opened.\n".format(filename))
        return output_string
      
    except:
        print("\nFailed to open {0}.\n".format(filename))

####################################################################################################

def file_to_string (filename):
    """
        Input: filename
        Objective: open a file and return a string, to be handled in-memory
        Output: string 
    """
    output_string = ""
    
    try:
        with open(filename, "r", errors="replace") as myfile:
            print("Successfully opened {0}.\n".format(filename))
            for line in myfile:
                try:
                    line = line.rstrip()
                    line = line.encode('latin-1').decode('unicode-escape').encode('latin-1').decode('utf-8')
                    output_string = output_string + line
                except:
                    #print("Failed line", line)
                    pass

        return output_string  

    except:
        print("\nFailed to open {0}.\n".format(filename))

####################################################################################################

def extract_tags_classes(html_filename, tag, class_):
    """
    Inputs: filename of an html file, tag we want to retrieve, class (optional) we want to retrieve.
    Objective: an html file is opened, converted to a string, the string is converted to a soup,
                and a list of tags belonging to the sought tag AND class is returned.
    Output: list with extracted tags.
    """

    html_string = file_to_string(html_filename)
    soup = BeautifulSoup(html_string, "html.parser")
    
    if class_ != "" and tag != "":
        wanted_tags = soup.find_all(tag, class_)   
        print('{0} <{1}> tags with the class "{2}" were retrieved in the file {3}.\n'.format(
            len(wanted_tags), tag, class_, html_filename))

    elif class_ == "" and tag != "":
        wanted_tags = soup.find_all(tag)   
        print('{0} <{1}> tags were retrieved in the file {2}.\n'.format(
            len(wanted_tags), tag, html_filename))

    elif class_ != "" and tag == "":
        wanted_tags = soup.find_all(class_)   
        print('{0} tags with the class "{1}" were retrieved in the file {2}.\n'.format(
            len(wanted_tags), class_, html_filename))

    elif class_ == "" and tag == "":
        wanted_tags = soup.find_all()   
        print('{0} tags of all types and classes were retrieved in the file {1}.\n'.format(
            len(wanted_tags), html_filename))

    return wanted_tags

## Test with class
#file = "alice.html"
#test = extract_tags_classes(file,"p","story")
#pprint.pprint(test)
## Test without class
#file = "alice.html"
#test = extract_tags_classes(file,"p")
#pprint.pprint(test)