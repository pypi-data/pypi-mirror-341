from pyMDReport.Components.Group import Group
from pyMDReport.types import Text

class ComposedText(Group):

    def __init__(
            self, 
            *text: Text,
            parent: Group | None = None,
            identifier: str | None = None,
            createAnchor: bool = False,
            anchorName: str | None = None,
            sep: str = "",
        ):
        
        super().__init__(
            parent=parent, 
            identifier=identifier,
            createAnchor=createAnchor,
            anchorName=anchorName,
        )

        self.text : dict[str, Text] = {}
        self.sep = sep

        if len(text) > 0:
            for component in text:
                self.Add(component)

    def Md( self ):

        md = ""
        for componentIdentifier in self.components.keys():
            component = self.components[componentIdentifier]
            md += component.Md() + self.sep
        return md