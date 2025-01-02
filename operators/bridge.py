import sys
import os
import json
import subprocess
import tempfile, platform
import bpy
import bmesh
import shutil

from bpy.props import EnumProperty

try:
	from importlib import reload
except:
	pass

from .. import variable as my_variables
reload(my_variables)

from .. import utility as my_utility
reload(my_utility)

# --- FILE ACTION LOGIC --- #

class OBJECT_OT_FILE_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
	"""Tool tip"""
	bl_idname = "object.file_action" # Naming object.add_cube so it will consistent with our class
	bl_label = "File"
	bl_description = 'Custom tools for file'

	action: EnumProperty(
		items=[
			('BLENDER_TO_MAYA', 'blender to maya', 'blender to maya'),
			('MAYA_TO_BLENDER', 'maya to blender', 'maya to blender'),
			('OPEN_RIZOM', 'open rizom', 'open rizom'),
		]
	)

	def execute(self, context):
		if self.action == 'BLENDER_TO_MAYA':
			self.blender_to_maya_function(context, my_variables.BLENDER_MAYA_FBX_PATH)
		elif self.action == 'MAYA_TO_BLENDER':
			self.maya_to_blender_function(context, my_variables.BLENDER_MAYA_FBX_PATH)
		elif self.action == 'BLENDER_TO_RIZOM':
			self.blender_to_rizom_function(context, my_variables.BLENDER_RIZOM_FBX_PATH)
		elif self.action == 'RIZOM_TO_BLENDER':
			self.rizom_to_blender_function(context, my_variables.BLENDER_RIZOM_FBX_PATH)
		elif self.action == 'OPEN_RIZOM':
			self.open_rizom(context)
		return {'FINISHED'}

	#region Support Function    
	def set_up_fbx_path(self):
		folder_path = r'C:/Blender_ImportExport'
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)

		return (folder_path)    

	def get_object_names(self, assets_path):
		names = []
		with bpy.data.libraries.load(assets_path) as (data_from, data_to):
			names = [name for name in data_from.objects]
		return names

	#endregion

	def blender_to_maya_function(self, context, temp_file):
		self.set_up_fbx_path()
		if context.scene.blender_maya_normal_radiobox == "Lock":
			lock_normal = 'OFF'
		else:
			lock_normal = 'EDGE'

		bpy.ops.export_scene.fbx(filepath=temp_file,
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
								 mesh_smooth_type=lock_normal,
								 use_mesh_edges=False,
								 use_tspace=False,
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
		
		my_utility.show_message(context, "INFO", "Export: Done!")

	def maya_to_blender_function(self, context, temp_file):
		if os.path.isfile(temp_file) == True:
			bpy.ops.import_scene.fbx(filepath=temp_file,
									 directory="",
									 filter_glob="*.fbx",
									 use_manual_orientation=False,
									 global_scale=1,
									 bake_space_transform=False,
									 use_custom_normals=True,
									 use_image_search=False,
									 use_alpha_decals=False,
									 decal_offset=0,
									 use_anim=True,
									 anim_offset=1,
									 use_custom_props=True,
									 use_custom_props_enum_as_string=True,
									 ignore_leaf_bones=False,
									 force_connect_children=False,
									 automatic_bone_orientation=False,
									 primary_bone_axis='Y',
									 secondary_bone_axis='X',
									 use_prepost_rot=True,
									 axis_forward='-Z',
									 axis_up='Y')
									 
		for item in (bpy.context.selected_objects):
			if '.' in item.name:
				old_name = str(item.name)
				new_name = old_name.replace('.', '_')
				item.name = new_name

		my_utility.show_message(context, "INFO", "Import: Done!")

	def open_rizom(self, context, exe_path, communicate):

		#subprocess.Popen([exe_path, "-cfi", RESOURCES + "py_construct.lua"])

		return True


	def blender_to_rizom_function(self, context, temp_file):
		print(11111)

	def rizom_to_blender_function(self, context, temp_file):
		print(22222)

# Support Functions

