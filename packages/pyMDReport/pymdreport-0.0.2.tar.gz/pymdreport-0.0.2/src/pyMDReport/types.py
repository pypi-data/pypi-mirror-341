class pyMDComponent: pass

class Anchor: pass

class Group ( pyMDComponent ): pass

class Report ( Group ): pass

class Text ( pyMDComponent ): pass

class Heading ( Text ): pass

class H1 ( Heading ): pass
class H2 ( Heading ): pass
class H3 ( Heading ): pass



class pyMDComponent:
    identifier: str
    parent: Group | None
    def __init__( self, 
        identifier: str | None = None, 
        parent: Group | None = None, 
    ): pass
    def MdRows( self ) -> list[str]: pass
    def Md( self ) -> str: pass 
    def Fill( *data ): pass

class Group ( pyMDComponent ):
    components: dict[str, pyMDComponent]
    def __init__( self, 
        *components: pyMDComponent,
        parent: Group | Report | None = None,
        identifier: str | None = None, 
    ): pass
    def Add( self,
        component: pyMDComponent, 
        componentIdentifier : str | None = None, 
    ): pass

class Report ( Group ):
    pass

class Text ( pyMDComponent ):
    text: str

class Heading ( Text ):
    MAX_HEADING_LEVEL: int

class H1 (Heading): pass
class H2 (Heading): pass
class H3 (Heading): pass