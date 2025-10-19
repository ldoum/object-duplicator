import bpy

###PROPERTIES
class DuplicateObjectProperties(bpy.types.PropertyGroup):
    
    ### Number of copies on X, Y and Z axis
    copies_x_line: bpy.props.IntProperty(
        name = "Copies on X Axis",
        description = "Number of copies on X axis",
        default = 1,
        min = 1,
        max = 100
    )
    
    copies_y_line: bpy.props.IntProperty(
        name = "Copies on Y Axis",
        description = "Number of copies on Y axis",
        default = 1,
        min = 1,
        max = 100
    )

    copies_z_line: bpy.props.IntProperty(
        name = "Copies on Z Axis",
        description = "Number of copies on Z axis",
        default = 1,
        min = 1,
        max = 100
    )
    
    ### Distance between copies on X, Y and Z axis
    distance_x_line: bpy.props.FloatProperty(
        name = "X Distance",
        description = "Space between copies on X axis",
        default = 1.00,
        min = 1.00,
        max = 100.00
    )
    
    distance_y_line: bpy.props.FloatProperty(
        name = "Y Distance",
        description = "Space between copies on Y axis",
        default = 1.00,
        min = 1.00,
        max = 100.00
    )

    distance_z_line: bpy.props.FloatProperty(
        name = "Z Distance",
        description = "Space between copies on Z axis",
        default = 1.00,
        min = 1.00,
        max = 100.00
    )

    ### set direction of duplication
    direction_of_x_line_copies: bpy.props.EnumProperty(
        name = "X Direction",
        description = "Direction of copies on X axis",
        items = [
            ('RIGHT', "Right", "Copies will be created to the right"),
            ('LEFT', "Left", "Copies will be created to the left")
        ],
        default = 'RIGHT'
    )
    
    direction_of_y_line_copies: bpy.props.EnumProperty(
        name = "Y Direction",
        description = "Direction of copies on Y axis",
        items = [
            ('FORWARD', "Forward", "Copies will be created forward"),
            ('BACKWARD', "Backward", "Copies will be created backward")
        ],
        default = 'FORWARD'
    )
    
    direction_of_z_line_copies: bpy.props.EnumProperty(
        name = "Z Direction",
        description = "Direction of copies on Z axis",
        items = [
            ('UP', "Up", "Copies will be created upward"),
            ('DOWN', "Down", "Copies will be created downward")
        ],
        default = 'UP'
    )
    
    toggle_x_axis: bpy.props.BoolProperty(
        name = "X Axis",    
        description = "Toggle duplication on X axis",
        default = False
    )
    
    toggle_y_axis: bpy.props.BoolProperty(
        name = "Y Axis",    
        description = "Toggle duplication on Y axis",
        default = False
    )
    
    toggle_z_axis: bpy.props.BoolProperty(
        name = "Z Axis",    
        description = "Toggle duplication on Z axis",
        default = False
    )
    
### PROPERTIES END    

###register/unregister
classes = [
    DuplicateObjectProperties,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.dupe_props = bpy.props.PointerProperty(type=DuplicateObjectProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.register_class(cls)
    del bpy.types.Scene.dupe_props
    
if __name__ == "__main__":
    register()
