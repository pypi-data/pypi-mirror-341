from pyMDReport.Components.Text import Text
from pyMDReport.types import Group, pyMDComponent

class Link(Text):

    def __init__(
            self,
            target: pyMDComponent,
            parent: Group | None = None,
            identifier: str | None = None, 
            text: str | None = None,
        ):

        super().__init__(
            parent=parent, 
            identifier=identifier, 
            text=text,
        )

        self.target = target

    def Md(self) -> str:

        return f"[{self.text}]({self.target.GetLink()})"