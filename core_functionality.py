###1246am 10/16/2025 Thursday 
#bare bones script that duplicates selected object N times along chosen axis with specified distance and direction
#can be run in Blender's text editor

import bpy

#helper function that returns 1 or -1 based on direction of copies on axis
def change_sign(pos_or_neg):
    if pos_or_neg in {'RIGHT','FORWARD','UP'}:
        return 1
    else:
        return -1

def formula(n, distance, axis, negate, collection_n):
        
    for sing_obj in bpy.context.selected_objects:
            
        for i in range(n):
            
            newbie = sing_obj.copy()
            newbie.data = sing_obj.data.copy()
            collection_n.objects.link(newbie)
            
            newbie.location[axis] = sing_obj.location[axis] + (i+1) * distance * change_sign(negate)




n_x = bpy.data.collections.new("New Collection")
bpy.context.scene.collection.children.link(n_x)

#inputs
copies_x = 3
distance_x = 5.00
direction_x = 1

copies_y = 2
distance_y = 7.00
direction_y = 1

copies_z = 9
distance_z = 9.00
direction_z = 1

toggle_x = True if bool(1) else False
toggle_y = True if bool(1) else False
toggle_z = True if bool(1) else False 

if toggle_x:
    formula(3, 5.00, 0, 'RIGHT' if bool(direction_x) else 'LEFT', n_x)
            
if toggle_y:
    formula(2, 7.00, 1, 'FORWARD' if bool(direction_y) else 'BACKWARD', n_x)
            
if toggle_z:
    formula(9, 9.00, 2, 'UP' if bool(direction_z) else 'DOWN', n_x)      
        