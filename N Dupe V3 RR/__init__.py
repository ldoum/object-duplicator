bl_info = {
    "name": "N duplicator", #
    "blender": (2, 8, 0),
    "category": "Object",
    "author": "Lancine Doumbia", #maintainer
    "version": (3, 0, 0), 
    "location": "View3D > Sidebar", #important
    "description": "Duplicate an object N times", #
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

from . import operators, panels, properties

def register():
    
    properties.register()
    operators.register()    
    panels.register()

def unregister():
    properties.unregister()
    operators.unregister()    
    panels.unregister()

if __name__ == "__main__":
    register()