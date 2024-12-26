import bpy
import bmesh
from bpy.props import EnumProperty

try:
    from imp import reload
except:
    pass

import Shiro_Tools.variable as my_variables
reload(my_variables)

import Shiro_Tools.utility as my_utility
reload(my_utility)

# --- NORMAL ACTION LOGIC --- #
class OBJECT_OT_NORMAL_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
    """Tool tip"""
    bl_idname = "object.normal_action" # Naming object.add_cube so it will consistent with our class
    bl_label = "Normal"
    bl_description = 'Custom tools for vertex normal'

    action: EnumProperty(
        items=[
            ('SET_LAST_NORMAL_FACE_TO_SELECTED_FACES', 'set last normal face to selected faces', 'set last normal face to selected faces'),
        ]
    )

    def execute(self, context):
        if self.action == 'SET_LAST_NORMAL_FACE_TO_SELECTED_FACES':
            self.set_last_normal_face_to_selected_faces_function(context)

        return {'FINISHED'}

    def get_active_face_index(self):
        bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
        if bm.select_history:
            elem = bm.select_history[-1]
            if isinstance(elem, bmesh.types.BMFace):
                return elem.index
        return 0

    def set_last_normal_face_to_selected_faces_function(self, context):
        active_face_index = my_utility.get_active_face_index()
        face_normal_vector = (0,0,0)
        for f in bmesh.from_edit_mesh(bpy.context.active_object.data).faces:
            if f.select and f.index == active_face_index:
                face_normal_vector = tuple(f.normal)
                break
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        mesh = bpy.context.object.data
        #mesh.use_auto_smooth = True
        #mesh.calc_normals_split()
        selected_vertices = [v.index for v in bpy.context.active_object.data.vertices if v.select]


        normals = []
        for l in mesh.loops:
            if l.vertex_index in selected_vertices:
                normals.append(face_normal_vector)
            else:
                normals.append(tuple(l.normal))
        mesh.normals_split_custom_set(normals)
        
        bpy.ops.object.mode_set(mode = 'EDIT')