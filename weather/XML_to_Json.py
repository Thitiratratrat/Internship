import xmltodict
import json

while True:
    filename = str(input("Please enter the xml file you wish to convert: "))
    if '.xml' not in filename:
        print("Invalid input")
        continue
    try:
        with open(filename) as xmlFile:
            xmlContent = xmltodict.parse(xmlFile.read())
        break
    except FileNotFoundError:
        print("Error! File could not be found.")
        continue

jsonFilename = filename.strip(".xml")
jsonFilename += ".json"
text = json.dumps(xmlContent)

text = text.replace('{"current": ', '')
text = text.replace('@', '')
text = text.replace('}}}', '}}')
text = text.replace('{', '{\n')
text = text.replace('"},', '"\n},')
text = text.replace('"}', '"\n}')
text = text.replace('},', '},\n')
text = text.replace('}}}', '}}')
text = text.replace('",', '",\n')

with open(jsonFilename, 'w') as jsonFile:
    jsonFile.write(text)



