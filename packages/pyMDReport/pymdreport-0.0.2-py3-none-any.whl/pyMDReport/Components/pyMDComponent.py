import uuid
from pyMDReport.Components.Anchor import Anchor
from pyMDReport.types import Group

class pyMDComponentData: pass

class pyMDComponent:

    parent: Group | None
    identifier: str
    anchor: Anchor | None

    def __init__(
            self,
            parent: Group | None = None,
            identifier: str | None = None,
            createAnchor: bool = False,
            anchorName: str | None = None,
        ):

        if not identifier:
            identifier = uuid.uuid4().hex
        self.identifier = identifier

        self.parent = parent
        if parent:
            parent.Add(self)

        self.anchor = None
        if createAnchor:
            self.anchor = Anchor( 
                parent=self, 
                anchorName=anchorName 
            )

    def MdPrec( self ) -> str:

        baseMd = ""
        if self.anchor:
            baseMd += self.anchor.Md()
        
        return baseMd
    
    def MdRows( self ) -> list[str]:
        
        baseMd = self.MdPrec()
        
        mdRows = [baseMd + self.Md()]
        
        return mdRows
    
    def MdString( self ) -> str:

        return '\t\n'.join(self.MdRows()) + "\t"
    
    def Md( 
            self 
        ) -> str:
        
        return ""
    
    def Fill(
            data: pyMDComponentData,
        ):

        return
    
    def GetLink(
            self,
        ):

        if self.anchor:
            return self.anchor.GetLink()