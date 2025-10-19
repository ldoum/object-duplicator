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
    
    direction_of_x_line_copies: bpy.props.EnumProperty(
        name = "X Direction",
        description = "Direction of copies on X axis",
        items = [
            ('RIGHT', "Right", "Copies will be created to the right"),
            ('LEFT', "Left", "Copies will be created to the left"),
        ],
        default = 'RIGHT'
    )
    
    direction_of_y_line_copies: bpy.props.EnumProperty(
        name = "Y Direction",
        description = "Direction of copies on Y axis",
        items = [
            ('FORWARD', "Forward", "Copies will be created forward"),
            ('BACKWARD', "Backward", "Copies will be created backward"),
        ],
        default = 'FORWARD'
    )
    
    direction_of_z_line_copies: bpy.props.EnumProperty(
        name = "Z Direction",
        description = "Direction of copies on Z axis",
        items = [
            ('UP', "Up", "Copies will be created upward"),
            ('DOWN', "Down", "Copies will be created downward"),
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


#### UTILS

### Utility function to change sign based on matching string input
def change_sign(pos_or_neg):
    if pos_or_neg in {'RIGHT','FORWARD','UP'}:
        return 1
    else:
        return -1

### UTILS END

###OPERATORS
class OperatorMixin:
    bl_options = {'REGISTER', 'UNDO'}
    
    @property
    def props(self):
        return bpy.context.scene.dupe_props

    def formula(self, n, distance, axis, negate, collect_it):
        
        for sing_obj in bpy.context.selected_objects:
            for i in range(n):
            
                newbie = sing_obj.copy()
                newbie.data = sing_obj.data.copy()
                collect_it.objects.link(newbie)
            
                newbie.location[axis] = sing_obj.location[axis] + (i+1) * distance * change_sign(negate)


class OBJECT_OT_Toggle_X_Mode(OperatorMixin, bpy.types.Operator):
    bl_idname = "my_operator.toggle_x_axis"
    bl_label = "My Class Name"
    bl_description = "Description that shows in blender tooltips"
    
    def execute(self, context):
        self.props.toggle_x_axis = not self.props.toggle_x_axis
        
        return {"FINISHED"}  
    
class OBJECT_OT_Toggle_Y_Mode(OperatorMixin, bpy.types.Operator):
    bl_idname = "my_operator.toggle_y_axis"
    bl_label = "My Class Name"
    bl_description = "Description that shows in blender tooltips"
    
    def execute(self, context):
        self.props.toggle_y_axis = not self.props.toggle_y_axis
        
        return {"FINISHED"}  
        
class OBJECT_OT_Toggle_Z_Mode(OperatorMixin, bpy.types.Operator): 
    bl_idname = "my_operator.toggle_z_axis"
    bl_label = "My Class Name"
    bl_description = "Description that shows in blender tooltips"
    
    def execute(self, context):
        self.props.toggle_z_axis = not self.props.toggle_z_axis
        
        return {"FINISHED"}  

class OBJECT_OT_Reset_All(OperatorMixin, bpy.types.Operator):
    bl_idname = "my_operator.reset_dupe_data"
    bl_label = "My Class Name"
    bl_description = "Description that shows in blender tooltips"
    
    def execute(self, context):
        
        self.props.copies_x_line = 1
        self.props.distance_x_line = 1.00
        self.props.direction_of_x_line_copies = "RIGHT"
        
        self.props.copies_y_line = 1
        self.props.distance_y_line = 1.00
        self.props.direction_of_y_line_copies = "FORWARD"
        
        self.props.copies_z_line = 1
        self.props.distance_z_line = 1.00
        self.props.direction_of_z_line_copies = "UP"
        
        return {"FINISHED"} 

class OBJECT_OT_Duplicate_All(OperatorMixin, bpy.types.Operator):
    bl_idname = "my_operator.apply_duplication"
    bl_label = "My Class Name"
    bl_description = "Description that shows in blender tooltips"

    @classmethod
    def poll(cls,context):
        return context.selected_objects

    def execute(self, context):
        
        ########
        if not self.poll(context):
            self.report({'WARNING'}, "No active object, cannot execute operator")
            return {'CANCELLED'}
        
        n_x = bpy.data.collections.new("Duplicate Collection")
        context.scene.collection.children.link(n_x)
       
       
        if self.props.toggle_x_axis:
            self.formula(self.props.copies_x_line, 
                        self.props.distance_x_line, 
                        0, 
                        self.props.direction_of_x_line_copies, 
                        n_x)
            
        if self.props.toggle_y_axis:
            self.formula(self.props.copies_y_line, 
                        self.props.distance_y_line, 
                        1, 
                        self.props.direction_of_y_line_copies, 
                        n_x)
            
        if self.props.toggle_z_axis:
            self.formula(self.props.copies_z_line, 
                        self.props.distance_z_line, 
                        2, 
                        self.props.direction_of_z_line_copies,
                        n_x)    
        

        return {"FINISHED"}        
    

###OPERATORS END


###PANELS
class PanelMixin:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    
class OBJECT_PT_Duplicates_Panel(PanelMixin, bpy.types.Panel):
    bl_idname = "panelname"
    bl_label = "N Duplicator"
    

    def draw(self, context):
        layout = self.layout
        props = context.scene.dupe_props
      
        #all in the box
        boxy = layout.box()
        column1 = boxy.column(align=True)
       
        set_panel = [
            ("X", props.toggle_x_axis, "copies_x_line", "distance_x_line" ,"direction_of_x_line_copies" ),
            ("Y", props.toggle_y_axis, "copies_y_line", "distance_y_line" ,"direction_of_y_line_copies" ),
            ("Z", props.toggle_z_axis, "copies_z_line", "distance_z_line" ,"direction_of_z_line_copies" ),
        
        ]
        
        for axis_name, visible, number_copies, distance_from_item, axis_path in set_panel:
        
            if visible:
                column1.label(text = axis_name)
                column1.prop(props, number_copies)
                column1.prop(props, distance_from_item)
                column1.prop(props, axis_path, expand=True)
            
        ###axis toggles
        row1 = layout.row(align=True)
        row1.operator(OBJECT_OT_Toggle_X_Mode.bl_idname, text="X", depress=props.toggle_x_axis)
        row1.operator(OBJECT_OT_Toggle_Y_Mode.bl_idname, text="Y", depress=props.toggle_y_axis)
        row1.operator(OBJECT_OT_Toggle_Z_Mode.bl_idname, text="Z", depress=props.toggle_z_axis)

        ##buttons
        row2 = layout.row()
        row2.operator(OBJECT_OT_Duplicate_All.bl_idname, text="Fire")
        row2.operator(OBJECT_OT_Reset_All.bl_idname, text="Reset")

###PANELS END


###register/unregister
classes = [
    
    DuplicateObjectProperties,
    OBJECT_PT_Duplicates_Panel,
    OBJECT_OT_Duplicate_All,
    OBJECT_OT_Reset_All,
    OBJECT_OT_Toggle_X_Mode,
    OBJECT_OT_Toggle_Y_Mode,
    OBJECT_OT_Toggle_Z_Mode,
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
