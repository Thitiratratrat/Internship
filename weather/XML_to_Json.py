import xmltodict
import json

while True:
    filename = str(input("Please enter the xml file you wish to convert: "))
    try:
        with open(filename) as xmlFile:
            xmlContent = xmltodict.parse(xmlFile.read())
        break
    except FileNotFoundError:
        print("Error! File could not be found.")
        continue

jsonFilename = filename.strip(".xml")
jsonFilename += ".json"
with open(jsonFilename, 'w') as jsonFile:
    json.dump(xmlContent, jsonFile)

