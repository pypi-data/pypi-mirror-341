from pyMDReport.Components.Text import Text
from pyMDReport.types import Group

class Heading(Text):

    MAX_HEADING_LEVEL = 3

    def __init__(
            self,
            headingLevel: int,
            parent: Group | None = None,
            identifier: str | None = None, 
            text: str | None = None,
        ):

        super().__init__(
            parent = parent, 
            identifier = identifier,
            text = text,
        )

        if headingLevel > self.MAX_HEADING_LEVEL:
            headingLevel = self.MAX_HEADING_LEVEL
        if headingLevel < 1:
            self.headingLevel = 1

        self.headingLevel = headingLevel

    def Md(self) -> str:
        
        return f"{'#'*self.headingLevel} {self.text}"
    
    def GetLink(self):
        
        # https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#section-links
        
        link = self.text.lower().strip()
        link = link.replace(" ", "-")
        
        for c in ",.;:_!?^()[]}{":
            link = link.replace(c, "")
        
        return f"#{link}"
    


class H1(Heading):

     def __init__(
            self,
            parent: Group | None = None,
            identifier: str | None = None, 
            text: str | None = None,
        ):

        super().__init__(1, parent, identifier, text)



class H2(Heading):

     def __init__(
            self,
            parent: Group | None = None,
            identifier: str | None = None, 
            text: str | None = None, 
        ):

        super().__init__(2, parent, identifier, text)



class H3(Heading):

     def __init__(
            self,
            parent: Group | None = None,
            identifier: str | None = None, 
            text: str | None = None,
        ):

        super().__init__(3, parent, identifier, text)