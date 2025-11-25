import bpy
from .operators import *
from .properties import *

###PANELS
class PanelMixin:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Duplicator"
    
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
        
        row2 = layout.row()
        row2.operator(OBJECT_OT_Duplicate_All.bl_idname, text="Fire")
        row2.operator(OBJECT_OT_Reset_All.bl_idname, text="Reset")

###PANELS END

###register/unregister
classes = [
    OBJECT_PT_Duplicates_Panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
if __name__ == "__main__":
    register()



