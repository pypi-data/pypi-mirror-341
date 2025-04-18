from pyMDReport.Components.Text import Text
from pyMDReport.types import Group

class Quote(Text):

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
            text=text,
            createAnchor=createAnchor,
            anchorName=anchorName
        )

    def MdRows(self):
        
        baseMd = super().MdPrec()
        if baseMd != "":
            return [baseMd, self.Md()]
        else:
            return [self.Md()]

    def Md(self) -> str:

        return f"> {self.text}\n"