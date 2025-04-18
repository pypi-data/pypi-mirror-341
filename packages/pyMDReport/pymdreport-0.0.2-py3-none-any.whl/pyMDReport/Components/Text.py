from pyMDReport.Components.pyMDComponent import pyMDComponent, pyMDComponentData
from pyMDReport.types import Group, Text

class TextData(pyMDComponentData):

    def __init__(self,
            text: str,
        ):

        self.text = text



class Text(pyMDComponent):

    def __init__(
            self,
            parent: Group | None = None,
            identifier: str | None = None, 
            text: str | None = None,
            createAnchor: bool = False,
            anchorName: str | None = None,
        ):

        super().__init__(
            parent=parent, 
            identifier=identifier, 
            createAnchor=createAnchor,
            anchorName=anchorName,
        )
        
        self.text = ""
        if text:
            self.text = text.replace("\n", " \t\n")

    def Md( self ) -> str:

        return f"{self.text}"
    
    def Fill(
            self, 
            data: TextData,
        ):

        self.text = data.text.replace("\n", " \t")

    def __add__(
            self,
            other: Text,
        ):

        return Text