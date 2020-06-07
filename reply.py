import csv

# Country attributes
headers = ["Capital", "Population", "Official languages", "GDP", "Flag"]

def make_reply(msg, countries_dict):
    """
        Makes reply based on a message received 

        Parameters: 
            msg (str): message received from a user
            countries_dict (dict): dictionary with data data for every country

        Returns: 
            str: A string with generated reply to a user
            str: A string with url to an image

    """
    # Format msg so that it match case of a country in countries_dict.keys()
    f = lambda word: word.title() if word != "the" and word != "and" else word
    msg = " ".join([f(word) for word in msg.lower().split(" ")])
    
    reply = 'Not found.'
    img_url = None
    if msg in countries_dict.keys(): 
        reply = "Country: " + msg
        for i in range(len(headers) - 1): 
            # Write a name of an attribute and corresponding data 
            reply += "\n" + headers[i] +": " + ", ".join(countries_dict[msg][i].split(";"))
        img_url = countries_dict[msg][-1] #URL to image of a flag on Wikipedia

    return reply, img_url

def read_data():
    '''
    Read all data from csv to dictionary
    
    Returns dictionaty with data for all countries 
    where country names are keys
    '''
    data_dict = {}
    with open("data/countries.csv", encoding="utf-8") as data_file:
        csv_data = csv.reader(data_file)

        next(csv_data) #Skip headers
    
        for row in csv_data:
            # Names of country is a key
            # Other data about country is stored in a list
            # [Capital, Population, Off. languages, GDP, Flag]
            data_dict[row[0]] = [entry for entry in row[1:]] 
    return data_dict



