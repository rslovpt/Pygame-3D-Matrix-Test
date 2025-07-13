import json

def toTuple(Table : list): #Converts a list of lists to tuple
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
            FacesTable = toTuple(ObjectDict['faces'])
            Position = tuple(ObjectDict['global_position'])
            ColorList = toTuple(ObjectDict['color'])

            extractedDict = {
                'Points': PointsTable,
                'Vertices': VerticesTable,
                'Faces': FacesTable,
                'Position': Position,
                'Name': ObjectDict['name'],
                'Angles': {
                    'Global': tuple(ObjectDict['angles']['global']),
                    'Camera': tuple(ObjectDict['angles']['camera'])
                },
                'ColorList': ColorList
            }

            Objects.append(extractedDict)

        return Objects
        
    def convertToFile(self, file):
        return
    