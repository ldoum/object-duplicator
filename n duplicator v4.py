bl_info = {
    "name": "N duplicator", #
    "blender": (2, 8, 0),
    "category": "Object",
    "author": "Lancine Doumbia", #maintainer
    "version": (4, 0, 1), 
    "location": "View3D > Sidebar", #important
    "description": "Duplicate an object N times", #
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

import bpy

###PROPERTIES
class DuplicationProperties(bpy.types.PropertyGroup):
    
    ### Number of copies on X, Y and Z axis
    copies_on_x_axis: bpy.props.IntProperty(
        name = "Copies on X Axis",
        description = "Number of copies on X axis",
        default = 1,
        min = 1,
        max = 1000
    )
    
    copies_on_y_axis: bpy.props.IntProperty(
        name = "Copies on Y Axis",
        description = "Number of copies on Y axis",
        default = 1,
        min = 1,
        max = 1000
    )

    copies_on_z_axis: bpy.props.IntProperty(
        name = "Copies on Z Axis",
        description = "Number of copies on Z axis",
        default = 1,
        min = 1,
        max = 1000
    )
    
    ### Distance between copies on X, Y and Z axis
    distance_on_x_axis: bpy.props.FloatProperty(
        name = "X Distance",
        description = "Space between copies on X axis",
        default = 1.00,
        min = 0.001,
        max = 1000.00
    )
    
    distance_on_y_axis: bpy.props.FloatProperty(
        name = "Y Distance",
        description = "Space between copies on Y axis",
        default = 1.00,
        min = 0.001,
        max = 1000.00
    )

    distance_on_z_axis: bpy.props.FloatProperty(
        name = "Z Distance",
        description = "Space between copies on Z axis",
        default = 1.00,
        min = 0.001,
        max = 1000.00
    )
    
    ### Toggle positive direction of copies on X, Y and Z axis
    positive_x_axis: bpy.props.BoolProperty(
        name = "Positive X",
        description = "Toggle duplication on X axis",
        default = False
    )
    
    positive_y_axis: bpy.props.BoolProperty(
        name = "Positive Y",
        description = "Toggle duplication on Y axis",
        default = False
    )
    
    positive_z_axis: bpy.props.BoolProperty(
        name = "Positive Z",
        description = "Toggle duplication on Z axis",
        default = False
    )
    
    # toggle duplication on axis
    toggle_copy_on_x_axis: bpy.props.BoolProperty(
        name = "X Axis",    
        description = "Toggle duplication on X axis",
        default = False
    )
    
    toggle_copy_on_y_axis: bpy.props.BoolProperty(
        name = "Y Axis",    
        description = "Toggle duplication on Y axis",
        default = False
    )
    
    toggle_copy_on_z_axis: bpy.props.BoolProperty(
        name = "Z Axis",    
        description = "Toggle duplication on Z axis",
        default = False
    )
    
    # toggle linked duplication
    linked_duplicate: bpy.props.BoolProperty(
        name = "Linked Duplicate",    
        description = "Toggle linked duplication",
        default = False
    )
    
### PROPERTIES END    


#### core functionality
#helper function that returns 1 or -1 based on direction of copies on axis
def change_sign(pos_or_neg):
    if pos_or_neg in {'RIGHT','FORWARD','UP'}:
        return 1
    else:
        return -1

#duplicated objects remain active for multi axes copying
def formula(n, distance, axis, negate, collection_n, linked_obj):
        
    for sing_obj in bpy.context.selected_objects:
            
        for i in range(n):
            
            #make new physical object
            newbie = sing_obj.copy()
            
            #handles objects w/o edit data
            if sing_obj.type != "EMPTY":
                
                # automate linked duplication. transfer data
                if linked_obj:
                    newbie.data = sing_obj.data
                else:
                    newbie.data = sing_obj.data.copy()
                
            #put object in new collectin    
            collection_n.objects.link(newbie)
            
            #move the new object
            newbie.location[axis] = sing_obj.location[axis] + (i+1) * distance * change_sign(negate)

#### core functionality end

#operator 1: runs the duplication program based on user input
class OT_Duplicate_All(bpy.types.Operator):
    bl_idname = "n_operator.apply_duplication"
    bl_label = "My Class Name"
    bl_description = "Description that shows in blender tooltips"

    @classmethod
    def poll(cls,context):
        return context.selected_objects

    def execute(self, context):
        
        dupe_props = context.scene.dupe_props
        
        #inputs
        copies_x = dupe_props.copies_on_x_axis
        distance_x = dupe_props.distance_on_x_axis
        direction_x = dupe_props.positive_x_axis
        toggle_x = dupe_props.toggle_copy_on_x_axis
        
        copies_y = dupe_props.copies_on_y_axis
        distance_y = dupe_props.distance_on_y_axis
        direction_y = dupe_props.positive_y_axis
        toggle_y = dupe_props.toggle_copy_on_y_axis
        
        copies_z = dupe_props.copies_on_z_axis
        distance_z = dupe_props.distance_on_z_axis
        direction_z = dupe_props.positive_z_axis
        toggle_z = dupe_props.toggle_copy_on_z_axis
        
        linked = dupe_props.linked_duplicate
        
        ########
        if not self.poll(context):
            self.report({'WARNING'}, "No active object, cannot execute operator")
            return {'CANCELLED'}
        
        n_x = bpy.data.collections.new("Duplicate Collection")
        context.scene.collection.children.link(n_x)
       
        #run core program for each axis if toggled on
        if toggle_x:
            formula(copies_x, distance_x, 0, 'RIGHT' if bool(direction_x) else 'LEFT', n_x, linked)
            
        if toggle_y:
            formula(copies_y, distance_y, 1, 'FORWARD' if bool(direction_y) else 'BACKWARD', n_x, linked)
            
        if toggle_z:
            formula(copies_z, distance_z, 2, 'UP' if bool(direction_z) else 'DOWN', n_x, linked)     
        

        return {"FINISHED"}        


#operator 2: resets all properties to default values
class OT_Reset_All(bpy.types.Operator):
    bl_idname = "n_operator.reset_dupe_data"
    bl_label = "My Class Name"
    bl_description = "Description that shows in blender tooltips"
    
    def execute(self, context):
        
        dupe_props = context.scene.dupe_props
        
        dupe_props.copies_on_x_axis = 1
        dupe_props.distance_on_x_axis = 1.00
        dupe_props.positive_x_axis = False
        dupe_props.toggle_copy_on_x_axis = False
        
        dupe_props.copies_on_y_axis = 1
        dupe_props.distance_on_y_axis = 1.00
        dupe_props.positive_y_axis = False
        dupe_props.toggle_copy_on_y_axis = False
        
        dupe_props.copies_on_z_axis = 1
        dupe_props.distance_on_z_axis = 1.00
        dupe_props.positive_z_axis = False
        dupe_props.toggle_copy_on_z_axis = False
        
        dupe_props.linked_duplicate = False

        return {"FINISHED"} 

    

###OPERATORS END


###PANELS

class PT_Duplicates_Panel(bpy.types.Panel):
    bl_idname = "n_panel.duplicates"
    bl_label = "Object Duplicator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        props = context.scene.dupe_props
      
        
        ###axis toggles
        row1 = layout.row(align=True)
        row1.prop(props, "toggle_copy_on_x_axis", toggle=True)
        row1.prop(props, "copies_on_x_axis")
        row1.prop(props, "distance_on_x_axis")
        row1.prop(props, "positive_x_axis", toggle=True)
      
        
        row2 = layout.row(align=True)
        row2.prop(props, "toggle_copy_on_y_axis", toggle=True)
        row2.prop(props, "copies_on_y_axis")
        row2.prop(props, "distance_on_y_axis")
        row2.prop(props, "positive_y_axis", toggle=True)
       
        
        row3 = layout.row(align=True)
        row3.prop(props, "toggle_copy_on_z_axis", toggle=True)
        row3.prop(props, "copies_on_z_axis")
        row3.prop(props, "distance_on_z_axis")
        row3.prop(props, "positive_z_axis", toggle=True)
        
        #linked duplicate toggle
        row_linked = layout.row()   
        row_linked.prop(props, "linked_duplicate", toggle=True)
        
        ##buttons
        row4 = layout.row(align=True)
        row4.operator(OT_Duplicate_All.bl_idname, text="Fire")
        row4.operator(OT_Reset_All.bl_idname, text="Reset")

###PANELS END


###register/unregister
classes = [
    
    DuplicationProperties,
    PT_Duplicates_Panel,
    OT_Duplicate_All,
    OT_Reset_All,
    
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.dupe_props = bpy.props.PointerProperty(type=DuplicationProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.register_class(cls)
    del bpy.types.Scene.dupe_props
    
if __name__ == "__main__":

    register()
