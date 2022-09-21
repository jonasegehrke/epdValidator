def checkDescription(material):
    # Removes newlines in description and unnecessary spaces
    material['description'] = material['description'].replace("\n", "")
    material['description'] = material['description'].strip()


def checkLifespan(material):
    # Checks if expectedLifespan is in the material, if it is and the value is -1 or -2 it removes it from the material
    key = 'expectedLifespan'
    if key in material:
        if material[key] == -1 or material[key] == -2:
            print(material["shortName"])
            del material[key]


def checkAdditionalSources(material):
    # Logs that somethins fishy if additionalSources doesnt contain anything
    key = 'additionalSources'
    if len(material[key]) > 0 and len(material[key]) < 2:
        if "https://www.epddanmark.dk/epd-databasen/" not in material[key][0]:
            print("somethings fishy, look here: ", material['shortName'])


def checkDeclaredUnits(material):
    # Logs that somethings fishy if declaredUnit is either missing key: value or if the value is null
    key = 'declaredUnit'
    if key in material:
        if 'declaredUnit' and 'declaredValue' and 'mass' and 'massUnit' in material[key]:
            if material[key]['declaredUnit'] == None or material[key]['declaredValue'] == None or material[key]['mass'] == None or material[key]['massUnit'] == None:
                print("somethings fishy, look here: ", material["shortName"])
        else:
            print("somethings fishy, look here: ", material["shortName"])


def checkOwnerId(material):
    # Checks if ownerId is existing and not null, if not logs the name of the material
    key = 'ownerId'
    if key in material:
        if material[key] == None:
            print("look here", material["shortName"])
    else:
        print("look here", material["shortName"])

