from pyMDReport.types import pyMDComponent
from pyMDReport.exceptions import InvalidAnchorException
import uuid

class Anchor:

    name: str

    def __init__(
            self,
            parent : pyMDComponent | None = None, 
            anchorName : str | None = None,
        ):

        self.parent = parent

        self.name = anchorName
        if not anchorName:
            self.name = self.GenerateAnchorName()

    def GenerateAnchorName( self ): 

        if self.parent:
            return self.parent.identifier
        return uuid.uuid4().hex

    def Md( self ) -> str: 
        
        return f'<a name="pyMDAnchor-{self.name}"></a>'
    
    def GetLink( self ) -> str:

        return f"#pyMDAnchor-{self.name}"