from pyMDReport.Components.Group import Group
from io import TextIOWrapper

class Report ( Group ):

    def __init__(self, *components): super().__init__(*components)

    def Export( 
            self,
            outputFile: TextIOWrapper | str,
        ):

        outputFileHandle = outputFile
        if type(outputFile) == str:
            outputFileHandle = open(outputFile, "w")

        outputFileHandle.write( self.MdString() )