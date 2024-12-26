import bpy
import bmesh
import random
from bpy.props import EnumProperty

try:
	from imp import reload
except:
	pass

import Shiro_Tools.variable as my_variables
reload(my_variables)

import Shiro_Tools.utility as my_utility
reload(my_utility)

# --- MATERIAL ACTION LOGIC --- #
class OBJECT_OT_COALITION_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
	"""Tool tip"""
	bl_idname = "object.coalition_action" # Naming object.add_cube so it will consistent with our class
	bl_label = "Material"
	bl_description = 'Custom tools for material'

	action: EnumProperty(
		items=[
			('CREATE_COALITION_MATERIAL_LIST', 'create coalition material list', 'create coalition material list'),
			('CLEAR_MATERIALS_IN_SCENE', 'clear materials in scene', 'clear materials in scene'),
			('SETUP_SHAPE_KEYS', 'setup shape keys', 'setup shape keys')
		]
	)

	def execute(self, context):
		if self.action == 'CREATE_COALITION_MATERIAL_LIST':
			self.create_coalition_material_list_function(context)
		elif self.action ==	'CLEAR_MATERIALS_IN_SCENE':
			self.delete_all_materials_function(context)
		elif self.action == 'SETUP_SHAPE_KEYS':
			self.setup_shape_keys_function(context)
		return {'FINISHED'}

	def create_coalition_material_list_function(self, context):
		gp01_stage = context.scene.coalition_stage
		udim_number = context.scene.udim_number
		material_file = open('S:\Coalition_Fairlight_HS_23\Documents\From_GE\Tech\Data\MaterialList_' + gp01_stage + '.txt', 'r')
		material_list = material_file.readlines()
		udim_material_file = open('S:\Coalition_Fairlight_HS_23\Documents\From_GE\Tech\Data\MaterialList_UDIM.txt', 'r')
		udim_material_list = udim_material_file.readlines()
		udim_material_list = [m.strip() for m in udim_material_list]
		
		for m in material_list:
			material_name = m.strip()
			if material_name.rsplit(":", 1)[-1] in udim_material_list and udim_number > 1:
				for i in range(0, udim_number):
					udim_material_name = material_name + "100" + str(i+1)
					if udim_material_name not in bpy.data.materials:
						r = random.randint(0, 255) * 1.0 / 255
						g = random.randint(0, 255) * 1.0 / 255
						b = random.randint(0, 255) * 1.0 / 255
						mat = bpy.data.materials.new(udim_material_name)
						# Viewport Display
						mat.diffuse_color = (r, g, b, 1)
						# Base Color
						mat.use_nodes = True
						bpy.data.materials[udim_material_name].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (r, g, b, 1)


			elif material_name not in bpy.data.materials:
				r = random.randint(0, 255) * 1.0 / 255
				g = random.randint(0, 255) * 1.0 / 255
				b = random.randint(0, 255) * 1.0 / 255
				mat = bpy.data.materials.new(material_name)
				# Viewport Display
				mat.diffuse_color = (r, g, b, 1)
				# Base Color
				mat.use_nodes = True
				bpy.data.materials[material_name].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (r, g, b, 1)
					
		my_utility.show_message(context, "INFO", "Create Material: Done!")

	def delete_all_materials_function(self, context):
		for obj in context.scene.objects:
			if obj.type == 'MESH':
				obj.data.materials.clear()
		for material in bpy.data.materials:
			material.user_clear()
			bpy.data.materials.remove(material)
		my_utility.show_message(context, "INFO", "Clear Material: Done!")

	def setup_shape_keys_function(self, context):
		selected_objects = bpy.context.selected_objects
		for obj in selected_objects:
			if not obj.data.shape_keys:
				obj.shape_key_add(name = "Basis")
				obj.shape_key_add(name = "Damaged Version")
				shape_key_blocks = obj.data.shape_keys.key_blocks
				shape_key_blocks["Damaged Version"].value = 1
			else:
				current_shape_key_blocks = obj.data.shape_keys.key_blocks
				obj.data.shape_keys.key_blocks[0].name = "Basis"
				if len(current_shape_key_blocks) == 1:
					obj.shape_key_add(name = "Damaged Version", from_mix=True)
					shape_key_blocks = obj.data.shape_keys.key_blocks
					shape_key_blocks["Damaged Version"].value = 1
				elif len(current_shape_key_blocks) >= 2:
					current_shape_key_blocks = obj.data.shape_keys.key_blocks
					for skb in current_shape_key_blocks:
						if skb.name == "Damaged Version":
							skb.name = "Temp Version (Tool)"
							break
					obj.shape_key_add(name = "Damaged Version", from_mix=True)

				shape_key_blocks = obj.data.shape_keys.key_blocks
				shape_key_blocks["Damaged Version"].value = 1
				for i in range(0, len(shape_key_blocks)-2):
					obj.shape_key_remove(shape_key_blocks[1])



