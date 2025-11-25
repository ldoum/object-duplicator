### [3.1.1]
1157pm 10/18/2025
1. Switched the arrangement of the items list in the property direction_of_x_line_copies for the sake of consistency. Tuples for the positive direction on the axis are first.

### [3.1.0]

1152pm 10/18/2025

1. Add reset button to set property data to default values.
2. Add operator to handle reset feature. Assign the value used as default to the 9 properties there.

### [3.0.0]

127am 10/16/2025

1. Renamed 2 properties and added 10 more.
2. Renamed Property group class and instance
3. Added Mixin classes for shared functionality
4. Added formula method in OperatorMixin to centralize the base code to duplicate copies of target object.
5. Added poll method in OBJECT_OT_Duplicate_All to activate button if at least one object is selected. Disable if not.
6. Added for loop in formula method to iterate through all selected objects
7. Added 2 lines in OBJECT_OT_Duplicate_All to put duplicates into new collection for sake of organization.
8. Added helper method change_sign to return either positive or negative 1 based on direction selected on the dropdowns for the axes
9. This add-on can duplicate objects in either a 2D or 3D grid.

### [2.1]

644pm 3/23/2025 Sunday Found a minor issue.

1. This add on only duplicates the first object out of all selected objects.

### [2.1]

329pm 3/13/2025
fixed 2 lines in execute()

Before:
context.scene.n.n
context.scene.distance.distance

Now:
context.scene.n
context.scene.distance

This add on can now duplicate objects and/or other items as many times as the user wants and separate the clones by a multiplied distance far from the main object as the user wants. The add-on's actions can now be undone.

### [2.0]

Blender threw attribute error.

Python: Traceback (most recent call last):
File "C:\Users\Home Base\AppData\Roaming\Blender Foundation\Blender\4.3\scripts\addons\Duplicate N RR\_\_init\_\_.py", line 99, in execute
many = context.scene.n.n
^^^^^^^^^^^^^^^^^
AttributeError: 'int' object has no attribute 'n'

1052am 3/12/25. Solve 3 issues.

1. Duplicator behaves well with objects and armatures, but not individual bones in Edit mode.
   Only the armatures get copied.
2. Whenever I try to undo the action of the duplicator add-on after , Blender 4.3.2 crashes.
3. The add-on only duplicates 5 times.
4. The add-on only moves each duplicate 2m \* N

5. Not an issue; lower minimum version of blender. Maybe 2.8

### [1.1]

611am 3/12/2025
Added metadata. Blender auto installed it. Showed up on Preferences. Fully operational

### [1.0]

606am 3/12/2025

First test. Blender threw an error. Forgot to add metadata.



