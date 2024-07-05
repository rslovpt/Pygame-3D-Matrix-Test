import json

def toTuple(Table : list):
    newTable = []
    for i in Table:
        newTable.append(tuple(i))
    return newTable

class jsonClass:
    def extractObjectsFromFile(self, file):
        ObjectList = json.load(open(file, "r+"))['Objects']
        Objects = []

        for ObjectDict in ObjectList:

            PointsTable = toTuple(ObjectDict['points'])
            VerticesTable = toTuple(ObjectDict['vertices'])
            Position = tuple(ObjectDict['global_position'])

            extractedDict = {
                'Points': PointsTable,
                'Vertices': VerticesTable,
                'Position': Position,
                'Name': ObjectDict['name']
            }

            Objects.append(extractedDict)

        return Objects
        
    def convertToFile(self, file):
        return
    