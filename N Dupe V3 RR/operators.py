import bpy
from .utils import change_sign
from .properties import DuplicateObjectProperties

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


###register/unregister
classes = [
    
    OBJECT_OT_Duplicate_All,
    OBJECT_OT_Toggle_X_Mode,
    OBJECT_OT_Toggle_Y_Mode,
    OBJECT_OT_Toggle_Z_Mode,
   
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.register_class(cls)
    
if __name__ == "__main__":
    register()