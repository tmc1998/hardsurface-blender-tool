import bpy
import bmesh
from bpy.props import EnumProperty

try:
    from imp import reload
except:
    pass

from .. import variable as my_variables
reload(my_variables)

from .. import utility as my_utility
reload(my_utility)

# --- VERTEXGROUP ACTION LOGIC --- #
class OBJECT_OT_VERTEXGROUP_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
    """Tool tip"""
    bl_idname = "object.vertexgroup_action" # Naming object.add_cube so it will consistent with our class
    bl_label = "Vertex Group"
    bl_description = 'Custom tools for vertex group'

    action: EnumProperty(
        items=[
            ('CLEAR_VERTEX_GROUP', 'clear vertex group of selected', 'clear vertex group of selected'),
        ]
    )

    def execute(self, context):
        if self.action == 'CLEAR_VERTEX_GROUP':
            self.clear_vertex_group_function(context)

        return {'FINISHED'}

    def clear_vertex_group_function(self, context):
        mode = bpy.context.active_object.mode
        if mode == 'OBJECT':
            obj = bpy.context.selected_objects
            for o in obj:
                vg_list = o.vertex_groups
                for vg in vg_list:
                    if vg is not None:
                        o.vertex_groups.remove(vg)
        else:
            bpy.ops.object.vertex_group_remove_from(use_all_groups=True)