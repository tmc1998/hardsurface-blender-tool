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

# --- SHAPE KEY ACTION LOGIC --- #
class OBJECT_OT_SHAPEKEYS_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
	"""Tool tip"""
	bl_idname = "object.shapekeys_action" # Naming object.add_cube so it will consistent with our class
	bl_label = "Shape Keys"
	bl_description = 'Custom tools for shape keys'

	action: EnumProperty(
		items=[
			('SETUP_SHAPE_KEYS', 'setup shape keys', 'setup shape keys'),
		]
	)

	def execute(self, context):
		if self.action == 'SETUP_SHAPE_KEYS':
			self.setup_shape_keys_function(context)

		return {'FINISHED'}
	
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