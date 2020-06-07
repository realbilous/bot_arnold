from bs4 import BeautifulSoup
import lxml
import requests
import csv
import re

# After data was fetched, a couple of corrections were made manually
# Among these are: Capital of Switzerland, Off. Languages of Mauritius,  Off. Languages of Belarus


# Data of interest 
countries = []
capitals = []
populations = []
gdps = []
flags = []
languages = []

# Get names of all countries from the List of countries by population
# Ignore all cities or states that are part of some country 
source = requests.get("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)").text
soup = BeautifulSoup(source, 'lxml')
countries = [entry.a['title'].strip() for entry in soup.find('table', {"id":"main"}).findAll('span', {"class":'datasortkey'}) if "(" not in entry.parent.text]

# Get population data for every country except Jersey and Guernsey from the same page
populations = [entry.text.strip() for entry in soup.find('table', {"id":"main"}).tbody.findAll(lambda tag:tag.name=="td" and 
"(" not in tag.parent.text and re.compile(r"[1-9]+").match(tag.text) and "%" in tag.find_next_sibling("td").text)]

# Remove territories that are not countries
del populations[countries.index("Western Sahara")]
del countries[countries.index("Western Sahara")]

# Get all other data by parsing Wikipedia page of every country individually
for country in countries:
    print(country)
    page = requests.get(f"https://en.wikipedia.org/wiki/{country}").text
    soup = BeautifulSoup(page, 'lxml')

    try:
        capital = soup.find("table",  {"class":"infobox geography vcard"}).find(lambda tag:tag.name=="th" and "Capital" in tag.text).find_next_sibling("td").a.text
    except AttributeError as e:
        print("   CAPITAL: ", e)
        capital = ''
    capitals.append(capital)

    try:
        language = ";".join([lang.text for lang in soup.find("table",  {"class":"infobox geography vcard"}).find(
            lambda tag:tag.name=="th" and "Official" in tag.text and "language" in tag.text).find_next_sibling("td").findAll(
            lambda tag:tag.name=="a" and "[" not in tag.text and not re.compile("[0-9]").search(tag.text))])
    except AttributeError as e:
        print("   LANGUAGE: ", e)
        try:
            language = ";".join([lang.text for lang in soup.find("table",  {"class":"infobox geography vcard"}).find(
                lambda tag:tag.name=="th" and "National" in tag.text and "language" in tag.text).find_next_sibling("td").findAll(
                lambda tag:tag.name=="a" and "[" not in tag.text and not re.compile("[0-9]").search(tag.text))])
        except AttributeError as e:
            print("   LANGUAGE: ", e)

    languages.append(language)
    language = ""
    try:
        gdp = soup.find("table",  {"class":"infobox geography vcard"}).find(
            lambda tag:tag.name=="th" and "GDP" in tag.text and "nominal" in tag.span.text).parent.find_next_sibling(
            lambda tag:tag.name=="tr" and "Total" in tag.th.text).td.text.split("[")[0].strip()
    except AttributeError as e:
        print("   GDP: ", e)
        gdp = ''
    gdps.append(gdp)
    
    flag = [a for a in soup.findAll('a', {"class":"image", "href":re.compile("(F|f)lag")})] 
    flags.append("https:" + flag[0].img["src"])

    response = requests.get("https:" + flag[0].img["src"])

    # Save image of a flag
    with open(f"data\\flags\\Flag of {country}.png", "wb") as file:
        file.write(response.content)

    
#Wtite the data to csv
with open('data\\countries.csv' , 'w', newline='', encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Country', 'Capital', 'Population', 'Off. languages', 'GDP', 'Flag'])
    for country, capital, population, language, gdp, flag in zip(countries, capitals, populations, languages, gdps, flags):
        csv_writer.writerow([country, capital, population, language, gdp, flag]) 
        

