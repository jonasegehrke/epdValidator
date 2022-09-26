import json

FILE_NAME = "final-list.json"

def checkDubes(material, allMaterials):
    #Checks if a dube has been found. If it has. then a log will apear
    found = [i for i, x in enumerate(allMaterials) if x["shortName"] == material["shortName"]]
    if(len(found) > 1):
        for f in found:
            if allMaterials[f]["additionalSources"] == allMaterials[f + 1]["additionalSources"]:
                print("Dubes where found!")

def fixWeirdCharacters(material):
    #fixes weird characters in name, decsription, tags
    material["shortName"] = material["shortName"].replace("Ã¦", "æ")
    material["description"] = material["description"].replace("Ã¦", "æ")
    newTags = []
    for tag in material["tags"]:
        tag = tag.replace("Ã¦", "æ")
        tag = tag.replace(",", "")
        newTags.append(tag)
    material["tags"] = newTags
    return material

def checkTags(material):
    #checks if tags are not found
    if len(material["tags"]) <= 0:
        print("Material without tags has been found: ", material["shortName"])

def checkEpdInfo(material):
    #checks if something is going on in epdinfo
    if material["epdInfo"]["validTo"] == "":
        print("ValidTo not set: ", material["shortName"])
    if material["epdInfo"]["issuedAt"] == "":
        print("IssuedAt not set: ", material["shortName"])
    if material["epdInfo"]["epdSpecificationForm"] != 0 and material["epdInfo"]["epdSpecificationForm"] != 1:
        print("epdSpecificationForm not set: ", material["shortName"])
    if material["epdInfo"]["epdProductIndustryType"] != 0 and material["epdInfo"]["epdProductIndustryType"] != 1:
        print("epdProductIndustryType not set: ", material["shortName"])
    
def checkDescription(material):
    # Removes newlines in description and unnecessary spaces
    material['description'] = material['description'].replace("\n\n", "")
    material['description'] = material['description'].strip()


def checkLifespan(material):
    # Checks if expectedLifespan is in the material, if it is and the value is -1 or -2 it removes it from the material
    key = 'expectedLifespan'
    if key in material:
        if material[key] == -1 or material[key] == -2:
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
        if material[key] == "":
            print("look here", material["shortName"])
    else:
        print("look here", material["shortName"])


def removeMetadata(material):
    if "conversionFactor" in material["declaredUnit"]:
        del material["declaredUnit"]["conversionFactor"]
    if "transportationInfo" in material:
        del material["transportationInfo"]
    if "id" in material:
        del material["id"]
    if "createdAt" in material:
        del material["createdAt"]
    if "createdBy" in material:
        del material["createdBy"]
    if "lastModifiedAt" in material:
        del material["lastModifiedAt"]
    if "lastModifiedBy" in material:
        del material["lastModifiedBy"]
    if "deleted" in material:
        del material["deleted"]
    if "deletedBy" in material:
        del material["deletedBy"]

def checkLink(material):
    if "link" not in material:
        return material
    if len(material["link"]) == 0:
        return material

with open(FILE_NAME, "r", encoding="utf8") as outfile:
    allMaterials = json.loads(outfile.read())

materialsWithoutLink = []

for material in allMaterials:
    removeMetadata(material)
    material = fixWeirdCharacters(material)
    checkDubes(material, allMaterials) 
    checkTags(material)
    checkEpdInfo(material)
    checkDescription(material)
    checkLifespan(material)
    checkAdditionalSources(material)
    checkDeclaredUnits(material)
    checkOwnerId(material)
    m = checkLink(material)
    if m is not None:
        materialsWithoutLink.append(m)
        allMaterials.remove(material)



noLink = json.dumps(materialsWithoutLink, indent=2)
with open("no-links.json", "w") as wfile:
    wfile.write(noLink)

final = json.dumps(allMaterials, indent=2)
with open("fixed-final.json", "w") as wfile:
    wfile.write(final)