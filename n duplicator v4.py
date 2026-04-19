bl_info = {
    "name": "N duplicator", 
    "blender": (2, 8, 0),
    "category": "Object",
    "author": "Lancine Doumbia", 
    "version": (4, 2, 0), 
    "location": "View3D > Sidebar", 
    "description": "Duplicate an object N times", 
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

import bpy

def object_available(obj, search):
   
    return (
        obj.name.startswith(search.lower()) or
        obj.name.startswith(search.upper()) or
        obj.name.startswith(search)
        )

def get_available_objects_in_scene(self, context):
    search = context.scene.dupe_props.object_search
    
    queue = []
   
    # if local items list is empty, add a default entry to prevent errors
    if context.scene.objects:
        queue = [(obj.name, obj.name, "") for obj in context.scene.objects if object_available(obj, search)]
       
        if queue:
            return queue
        else:
            return [("NOTHING", "Object(s) not found", "")]
   
    return [("EMPTY", "No objects in this scene", "")]

###PROPERTIES
class NDUPEADDON_PG_DuplicationProperties(bpy.types.PropertyGroup):
    
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
    
    # choose mode of duplication 
    mode_of_duplication: bpy.props.EnumProperty(
        name = "Mode of Duplication",
        description = "Choose the mode of duplication",
        items = [
            ('GRID', "Grid", "Copies will be created to the right"),
            ('SPAWN', "Spawn", "Copies will be created to the left"),
        ],
        default = 'GRID'
    )
    
    #select objects to duplicate from a dropdown list of all objects in the scene, filtered by search query
    object_selection: bpy.props.EnumProperty(
        name = "Object Scan",
        description = "Choose the type of objects to duplicate",
        items = get_available_objects_in_scene,
    )
    
    #search for objects to duplicate by name
    object_search: bpy.props.StringProperty(
        name = "Object Search",
        description = "Search for objects to duplicate by name",
        default = "",
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
def grid_duplication(n, distance, axis, negate, collection_n, linked_obj):
        
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


#duplicates an object to the location of each selected object
def spawn_duplication(main, collection_n, linked_obj):

    orig_obj = bpy.context.scene.objects[main]
    
    for sing_obj in bpy.context.selected_objects:

        #make new physical object
        newbie = orig_obj.copy()
            
        #handles objects w/o edit data
        if orig_obj.type != "EMPTY":
                
            # automate linked duplication. transfer data
            if linked_obj:
                newbie.data = orig_obj.data
            else:
                newbie.data = orig_obj.data.copy()
                
        #put object in new collectin    
        collection_n.objects.link(newbie)
  
        #move the new object to the location of the host object
        newbie.location = sing_obj.matrix_world.translation


#### core functionality end

#operator 1: runs the duplication program based on user input
class NDUPEADDON_OT_Duplicate_Grid(bpy.types.Operator):
    bl_idname = "ndupeaddon.grid_duplication"
    bl_label = "Duplicate in a Grid"
    bl_description = "Duplicate objects in a grid pattern"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls,context):
        dupe_props = context.scene.dupe_props
        active_x = dupe_props.toggle_copy_on_x_axis
        active_y = dupe_props.toggle_copy_on_y_axis
        active_z = dupe_props.toggle_copy_on_z_axis

        #prevent placeholder collections from being added if no axis is selected
        if context.selected_objects and (active_x or active_y or active_z):
            return True 
        else:
            return False

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
        
        
        n_x = bpy.data.collections.new("Duplicate Collection Grid")
        context.scene.collection.children.link(n_x)
       
        #run core program for each axis if toggled on
        if toggle_x:
            grid_duplication(copies_x, distance_x, 0, 'RIGHT' if bool(direction_x) else 'LEFT', n_x, linked)
            
        if toggle_y:
            grid_duplication(copies_y, distance_y, 1, 'FORWARD' if bool(direction_y) else 'BACKWARD', n_x, linked)
            
        if toggle_z:
            grid_duplication(copies_z, distance_z, 2, 'UP' if bool(direction_z) else 'DOWN', n_x, linked)     
        

        return {"FINISHED"}        


#operator 2: duplicates an object to the location of each selected object based on user input
class NDUPEADDON_OT_Duplicate_Spawn(bpy.types.Operator):
    bl_idname = "ndupeaddon.spawn_duplication"
    bl_label = "Duplicate to Selected Objects"
    bl_description = "Duplicate an object to the location of each selected object"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls,context):
        dupe_props = context.scene.dupe_props
        
        #prevent placeholder collections from being added if no object is selected
        if context.selected_objects and dupe_props.object_selection:
            return True 
        
        
    def execute(self, context):
        dupe_props = context.scene.dupe_props
        
        main = dupe_props.object_selection
        
        n_x = bpy.data.collections.new("Duplicate Collection Spawn")
        context.scene.collection.children.link(n_x)
        
        linked = dupe_props.linked_duplicate
        
        #run core program for spawn duplication
        spawn_duplication(main, n_x, linked)
        
        return {"FINISHED"}


#operator 3: resets all properties to default values
class NDUPEADDON_OT_Reset_All(bpy.types.Operator):
    bl_idname = "ndupeaddon.reset_everything"
    bl_label = "Reset All"
    bl_description = "Reset all properties to default values"
    bl_options = {'REGISTER', 'UNDO'}
    
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

class NDUPEADDON_PT_Duplicates_Panel(bpy.types.Panel):
    bl_idname = "NDUPEADDON_PT_Duplicates_Panel"
    bl_label = "Object Duplicator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "N Duplicator"

    def draw(self, context):
        layout = self.layout
        props = context.scene.dupe_props
      
        
        layout.prop(props, "mode_of_duplication", expand=True)
        
        if props.mode_of_duplication == 'GRID':
         
            ###axis toggles
            row1 = layout.row()
            col1 = row1.column(align=True)
            col1.prop(props, "toggle_copy_on_x_axis", toggle=True)
            col1.prop(props, "copies_on_x_axis")
            col1.prop(props, "distance_on_x_axis")
            col1.prop(props, "positive_x_axis", toggle=True)
      
        
            row2 = layout.row()
            col2 = row2.column(align=True)
            col2.prop(props, "toggle_copy_on_y_axis", toggle=True)
            col2.prop(props, "copies_on_y_axis")
            col2.prop(props, "distance_on_y_axis")
            col2.prop(props, "positive_y_axis", toggle=True)
       
        
            row3 = layout.row()
            col3 = row3.column(align=True)
            col3.prop(props, "toggle_copy_on_z_axis", toggle=True)
            col3.prop(props, "copies_on_z_axis")
            col3.prop(props, "distance_on_z_axis")
            col3.prop(props, "positive_z_axis", toggle=True)
        
        else:
            layout.prop(props, "object_search")
            layout.prop(props, "object_selection")
        
        
        #linked duplicate toggle
        row_linked = layout.row()   
        row_linked.prop(props, "linked_duplicate", toggle=True)
        
        ##buttons
        row4 = layout.row(align=True)
        
        #swap button text and functionality based on mode of duplication
        if props.mode_of_duplication == 'GRID':
            row4.operator(NDUPEADDON_OT_Duplicate_Grid.bl_idname, text="Fire")
        else:
            row4.operator(NDUPEADDON_OT_Duplicate_Spawn.bl_idname, text="Populate")
            
        row4.operator(NDUPEADDON_OT_Reset_All.bl_idname, text="Reset")

###PANELS END


###register/unregister
classes = [
    
    NDUPEADDON_PG_DuplicationProperties,
    NDUPEADDON_OT_Duplicate_Grid,
    NDUPEADDON_OT_Duplicate_Spawn,
    NDUPEADDON_OT_Reset_All,
    NDUPEADDON_PT_Duplicates_Panel,
    
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.dupe_props = bpy.props.PointerProperty(type=NDUPEADDON_PG_DuplicationProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.register_class(cls)
    del bpy.types.Scene.dupe_props
    
if __name__ == "__main__":
    register()


