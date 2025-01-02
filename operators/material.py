import bpy
import bmesh
import random
from bpy.props import EnumProperty

try:
    from imp import reload
except:
    pass

from .. import variable as my_variables
reload(my_variables)

from .. import utility as my_utility
reload(my_utility)

# --- MATERIAL ACTION LOGIC --- #
class OBJECT_OT_MATERIAL_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
    """Tool tip"""
    bl_idname = "object.material_action" # Naming object.add_cube so it will consistent with our class
    bl_label = "Material"
    bl_description = 'Custom tools for material'

    action: EnumProperty(
        items=[
            ('DELETE_ALL_MATERIALS', 'delete all material', 'delete all material'),
            ('DELETE_DUPLICATE_MATERIALS', 'delete duplicate materials', 'delete duplicate materials'),
            ('DELETE_ALL_MATERIAL_SLOTS', 'delete material slots', 'delete material slots')
        ]
    )

    def execute(self, context):
        if self.action == 'DELETE_ALL_MATERIALS':
            self.delete_all_materials_function(context)
        elif self.action == 'DELETE_DUPLICATE_MATERIALS':
            self.delete_duplicate_materials_function(context)
        elif self.action == 'DELETE_ALL_MATERIAL_SLOTS':
            self.delete_material_slots_function(context)
        return {'FINISHED'}

    def delete_all_materials_function(self, context):
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                obj.data.materials.clear()
        for material in bpy.data.materials:
            material.user_clear()
            bpy.data.materials.remove(material)
        my_utility.show_message(context, "INFO", "Clear Material: Done!")

    def delete_duplicate_materials_function(self, context):
        mats = bpy.data.materials
        for mat in mats:
            (original, _, ext) = mat.name.rpartition(".")
            if ext.isnumeric() and mats.find(original) != -1:
                mat.user_remap(mats[original])
                mats.remove(mat)
        my_utility.show_message(context, "INFO", "Delete: Done!")

    def delete_material_slots_function(self, context):
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.data.materials.clear()
        my_utility.show_message(context, "INFO", "Delete: Done!")
        