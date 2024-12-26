import os
import bpy
import bmesh
import math
from bpy.props import EnumProperty
from mathutils import Vector

try:
    from imp import reload
except:
    pass

import Shiro_Tools.variable as my_variables
reload(my_variables)

import Shiro_Tools.utility as my_utility
reload(my_utility)

# --- BAKESET ACTION LOGIC --- #
class OBJECT_OT_BAKESET_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
    """Tool tip"""
    bl_idname = "object.bakeset_action" # Naming object.add_cube so it will consistent with our class
    bl_label = "Bakeset"
    bl_description = 'Custom tools for bakeset'

    action: EnumProperty(
        items=[
            ('RENAME_HIGHPOLY', 'rename highpoly', 'rename highpoly'),
            ('CREATE_BAKESET', 'create bakeset', 'create bakeset'),
            ('AUTO_CREATE_BAKESET', 'auto create bakeset', 'auto create bakeset'),
            ('SELECT_FBX_EXPORT_PATH', 'select fbx export path', 'select fbx export path'),
            ('EXPORT_SELECTED_HIGH_LOW', 'export selected high/low', 'export selected high/low'),
            ('EXPORT_ALL_BAKESET', 'export all bakeset', 'export all bakeset'),
        ]
    )

    def execute(self, context):
        if self.action == 'RENAME_HIGHPOLY':
            self.rename_highpoly_function(context)
        elif self.action == 'CREATE_BAKESET':
            self.create_bakeset_function(context)
        elif self.action == 'AUTO_CREATE_BAKESET':
            self.auto_create_bakeset_function(context)
        elif self.action == 'SELECT_FBX_EXPORT_PATH':
            self.select_fbx_export_path_function(context)
        elif self.action == 'EXPORT_SELECTED_HIGH_LOW':
            self.export_bakeset_function(context, 'selected')
        elif self.action == 'EXPORT_ALL_BAKESET':
            self.export_bakeset_function(context, 'all')

        return {'FINISHED'}
    
    def rename_highpoly_function(self, context):
        selected_object_list = [obj for obj in bpy.context.selected_objects]
        if len(selected_object_list) == 0:
            my_utility.show_message(context, "ERROR", "Please select mesh for rename!")
            return False
        
        i = 1
        new_name = "HSTool_High_1"
        for m in selected_object_list:
            object_list = [obj.name for obj in bpy.context.scene.objects]
            while new_name in object_list:
                i += 1
                new_name = "HSTool_High_" + str(i)
            m.name = new_name

        my_utility.show_message(context, "INFO", "Rename Highpoly: Done!")
        return True

    def check_highpoly_name(self, name):
        split_list = name.rsplit("_", 1)
        if split_list[0] == "HSTool_High" and split_list[-1].isnumeric():
            return True
        else:
            return False

    def get_distance(self, a_pos, b_pos):
        distance = math.sqrt(pow((a_pos[0]-b_pos[0]),2) + pow((a_pos[1]-b_pos[1]),2) + pow((a_pos[2]-b_pos[2]),2))
        return distance

    def get_bounding_box(self, obj):
        vertices_world = [obj.matrix_world @ vertex.co for vertex in obj.data.vertices]
        x, y, z = zip(*(p for p in vertices_world))
        return [(min(x), min(y), min(z)), (max(x), max(y), max(z))]

    def check_overlap(self, context, object_a, object_b):
        a_bbox = self.get_bounding_box(object_a)
        b_bbox = self.get_bounding_box(object_b)
        diagonal_line_length = self.get_distance(b_bbox[0], b_bbox[-1])
        min_distance = diagonal_line_length * context.scene.threshold_value
        if self.get_distance(a_bbox[0], b_bbox[0]) >= min_distance or self.get_distance(a_bbox[-1], b_bbox[-1]) >= min_distance:
            return False
        else:
            return True

    def create_bakeset_function(self, context):
        # Create BakeSet group
        selected_object_list = [obj for obj in bpy.context.selected_objects]

        # Get lowpoly & highpoly mesh list
        highpoly_mesh_list = []
        lowpoly_mesh_list = []
        for i in range(0, len(selected_object_list)):
            if self.check_highpoly_name(selected_object_list[i].name):
                highpoly_mesh_list.append(selected_object_list[i].name)
            else:
                lowpoly_mesh_list.append(selected_object_list[i].name)

        # Combine highpoly mesh
        bpy.ops.object.select_all(action='DESELECT')
        highpoly_mesh = my_utility.join_mesh(highpoly_mesh_list)

        # Combine lowpoly mesh
        bpy.ops.object.select_all(action='DESELECT')
        lowpoly_mesh = my_utility.join_mesh(lowpoly_mesh_list)

        # Rename & group mesh
        object_list = [obj.name for obj in bpy.context.scene.objects]
        i = 1
        bakeset_name = context.scene.bakeset_name + "_1"
        while bakeset_name in object_list:
            i += 1
            bakeset_name = context.scene.bakeset_name + "_" + str(i)
        bakeset_empty = my_utility.make_empty(bakeset_name, (0,0,0))
        high_group = my_utility.make_empty("High_" + str(i), (0,0,0))
        low_group = my_utility.make_empty("Low_" + str(i), (0,0,0))
        high_group.parent = bakeset_empty
        low_group.parent = bakeset_empty

        # Assign mesh to group
        highpoly_mesh.parent = high_group
        lowpoly_mesh.parent = low_group

        highpoly_mesh.name = bakeset_name + "_High"
        lowpoly_mesh.name = bakeset_name + "_Low"

        my_utility.show_message(context, "INFO", "Create Bakeset: Done!")
    
    def auto_create_bakeset_function(self, context):
        #Create BakeSet Group
        object_pair_list = []
        checked_object_list = []
        selected_object_list = [obj for obj in bpy.context.selected_objects]
        for i in range(0, len(selected_object_list)):
            for j in range(i+1, len(selected_object_list)):
                if i not in checked_object_list:
                    if self.check_overlap(context, selected_object_list[i], selected_object_list[j]):
                        object_pair_list.append([selected_object_list[i], selected_object_list[j]])
                        checked_object_list.append(j)
                        break
        print(object_pair_list)
        for obj_pair in object_pair_list:
            if self.check_highpoly_name(obj_pair[0].name):
                highpoly_mesh = obj_pair[0]
                lowpoly_mesh = obj_pair[1]
            elif self.check_highpoly_name(obj_pair[-1].name):
                highpoly_mesh = obj_pair[1]
                lowpoly_mesh = obj_pair[0]

            # Rename & group mesh
            object_list = [obj.name for obj in bpy.context.scene.objects]
            i = 1
            bakeset_name = context.scene.bakeset_name + "_1"
            while bakeset_name in object_list:
                i += 1
                bakeset_name = context.scene.bakeset_name + "_" + str(i)
            bakeset_empty = my_utility.make_empty(bakeset_name, (0,0,0))
            high_group = my_utility.make_empty("High_" + str(i), (0,0,0))
            low_group = my_utility.make_empty("Low_" + str(i), (0,0,0))
            high_group.parent = bakeset_empty
            low_group.parent = bakeset_empty

            # Assign mesh to group
            highpoly_mesh.parent = high_group
            lowpoly_mesh.parent = low_group

            highpoly_mesh.name = bakeset_name + "_High"
            lowpoly_mesh.name = bakeset_name + "_Low"

        my_utility.show_message(context, "INFO", "Auto create Bakeset: Done!")

    def export_fbx_for_baking(self, context, object_name, folder_path):
        # Setting for low/high mesh
        if "high" in object_name.rsplit('_', 1)[-1].lower():
            triangle = False
        else:
            triangle = True
        # Unlock normal
        if context.scene.export_bakeset_unlock_normal:
            smooth_type = 'FACE' 
        else:
            smooth_type = 'OFF'

        fbx_path = folder_path + object_name + ".fbx"
        bpy.ops.export_scene.fbx(filepath=fbx_path,
                                check_existing=True,
                                filter_glob="*.fbx",
                                use_selection=True,
                                use_active_collection=False,
                                global_scale=1,
                                apply_unit_scale=True,
                                apply_scale_options='FBX_SCALE_ALL',
                                bake_space_transform=True,
                                object_types={'MESH','EMPTY'},
                                use_mesh_modifiers=True,
                                use_mesh_modifiers_render=True,
                                mesh_smooth_type=smooth_type,
                                use_mesh_edges=False,
                                use_tspace=False,
                                use_triangles=triangle,
                                use_custom_props=False,
                                add_leaf_bones=False,
                                primary_bone_axis='Y',
                                secondary_bone_axis='X',
                                use_armature_deform_only=False,
                                armature_nodetype='NULL',
                                bake_anim=False,
                                bake_anim_use_all_bones=False,
                                bake_anim_use_nla_strips=False,
                                bake_anim_use_all_actions=False,
                                bake_anim_force_startend_keying=False,
                                bake_anim_step=1,
                                bake_anim_simplify_factor=1,
                                path_mode='AUTO',
                                embed_textures=False,
                                batch_mode='OFF',
                                use_batch_own_dir=True,
                                use_metadata=True,
                                axis_forward='Y',
                                axis_up='Z')


    def export_bakeset_function(self, context, mode):
        # Get FBX folder
        fbx_path = context.scene.bakeset_export_path
        
        # Get Bakeset name
        bakeset_name = context.scene.bakeset_name

        # Get object list
        if mode == 'selected':
            mesh_list = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        else:
            mesh_list = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and bakeset_name in obj.name]
        # Get export mode: Single/Multiple
        export_mode = context.scene.export_bakeset_mode
        
        # Export FBX
        bpy.ops.object.select_all(action='DESELECT')
        if export_mode == "Multiple":
            # Multiple Files
            for mesh in mesh_list:
                if bakeset_name in mesh.name:
                    bpy.ops.object.select_all(action='DESELECT')
                    mesh.select_set(True)
                    self.export_fbx_for_baking(context, mesh.name, fbx_path)
        else:
            # Single Files
            low_mesh_list = [m for m in mesh_list if m.name.rsplit("_", 1)[-1].lower() == "low"]
            high_mesh_list = [m for m in mesh_list if m.name.rsplit("_", 1)[-1].lower() == "high"]
            if len(low_mesh_list) > 0:
                for m in low_mesh_list:
                    m.select_set(True)
                self.export_fbx_for_baking(context, 'Object_Low', fbx_path)
            if len(high_mesh_list) > 0:
                bpy.ops.object.select_all(action='DESELECT')
                for m in high_mesh_list:
                    m.select_set(True)
                self.export_fbx_for_baking(context, 'Object_High', fbx_path)

        bpy.ops.object.select_all(action='DESELECT')
        my_utility.show_message(context, "INFO", "Export Bakeset: Done!")