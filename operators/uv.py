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

# --- UV ACTION LOGIC --- #
class OBJECT_OT_UV_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
    """Tool tip"""
    bl_idname = "object.uv_action" # Naming object.add_cube so it will consistent with our class
    bl_label = "UV"
    bl_description = 'Custom tools for UV'

    action: EnumProperty(
        items=[
            ('RENAME_UVSET1', 'rename uvset1', 'rename uvset1'),
            ('DELETE_REDUNDANT_UVSET', 'delete redundant uvset', 'delete redundant uvset'),
        ]
    )

    def execute(self, context):
        if self.action == 'RENAME_UVSET1':
            self.rename_uvset1_function(context)
        elif self.action == 'DELETE_REDUNDANT_UVSET':
            self.delete_redundant_uvset_function(context)

        return {'FINISHED'}

    def rename_uvset1_function(self, context):
        mesh_list = [obj for obj in bpy.context.scene.objects if obj.type=='MESH']
        for obj in mesh_list:
            uv_maps = obj.data.uv_layers
            try:
                uv_maps[0].name = context.scene.uvset1_name
            except:
                pass

    def delete_redundant_uvset_function(self, context):
        mesh_list = [obj for obj in bpy.context.scene.objects if obj.type=='MESH']
        for obj in mesh_list:
            uv_maps = obj.data.uv_layers
            while len(uv_maps) > 1:
                uv_maps.remove(uv_maps[len(uv_maps)-1])