from pyMDReport.Components.pyMDComponent import pyMDComponent, pyMDComponentData
from pyMDReport.exceptions import AddComponentException
from pyMDReport.types import Group, Report

class Group(pyMDComponent):

    def __init__(
            self, 
            *components: pyMDComponent,
            parent: Group | Report | None = None,
            identifier: str | None = None,
            createAnchor: bool = False,
            anchorName: str | None = None,
        ):
        
        super().__init__(
            parent=parent, 
            identifier=identifier,
            createAnchor=createAnchor,
            anchorName=anchorName,
        )

        self.components : dict[str, pyMDComponent] = {}

        if len(components) > 0:
            for component in components:
                self.Add(component)

    def Add(
            self,
            component: pyMDComponent,
            componentIdentifier: str | None = None,
        ):

        componentId = component.identifier
        if componentIdentifier:
            componentId = componentIdentifier

        if componentId in self.components.keys():
            raise AddComponentException("A pyMDComponent with the given identifier already exists in this group")
        
        self.components[componentId] = component
        component.parent = self

    def MdRows(self):
        
        return [super().MdPrec(), self.Md()]

    def Md( self ) -> str:

        md = ""
        for componentIdentifier in self.components.keys():
            component = self.components[componentIdentifier]
            md += component.MdString() + "\n"
        return md
    
    def Fill(
            self,
            **componentData: pyMDComponentData, 
        ):

        for componentIdentifier in componentData.keys():
            if componentIdentifier in self.components.keys():
                component = self.components[componentIdentifier]
                cd = componentData[componentIdentifier]
                if type(component) == Group:
                    component.Fill(**cd)
                else:
                    component.Fill( cd )