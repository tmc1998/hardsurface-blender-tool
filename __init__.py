bl_info = {
    "name" : "HardSurface Tool",
    "author" : "Canh Tran",
    "description" : "This add-on provides a set of custom tools for working efficiently in Blender.",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 1),
    "location" : "3D View > N",
    "warning" : "",
    "category" : "Object",
}

try:
    from imp import reload
except:
    pass

import os
import sys
import bpy
from . import addon_updater_ops

# Find root path
SHIRO_TOOL_PATH = os.path.dirname(os.path.abspath(__file__))
SHIRO_TOOL_PATH = SHIRO_TOOL_PATH.replace("\\", "/")

sys.path.append(SHIRO_TOOL_PATH)

# Import function
import Shiro_Tools.operators.select as select_operators
import Shiro_Tools.operators.bridge as bridge_operators
import Shiro_Tools.operators.modifier as modifier_operators
import Shiro_Tools.operators.vertex_normal as vertex_normal_operators
import Shiro_Tools.operators.vertex_group as vertex_group_operators
import Shiro_Tools.operators.shapekey as shapekey_operators
import Shiro_Tools.operators.collection as collection_operators
import Shiro_Tools.operators.uv as uv_operators
import Shiro_Tools.operators.material as material_operators
import Shiro_Tools.operators.model as model_operators
import Shiro_Tools.operators.check as check_operators
import Shiro_Tools.operators.capture as capture_operators
import Shiro_Tools.operators.bakeset as bakeset_operators
import Shiro_Tools.operators.coalition as coalition_operators
import Shiro_Tools.properties as properties
import Shiro_Tools.icons as icons

# Import UI
import Shiro_Tools.ui as ui

# Preferences

@addon_updater_ops.make_annotations
class HardSurfaceToolPreferences(bpy.types.AddonPreferences):
	"""HardSurface Tool bare-bones preferences"""
	bl_idname = __package__

	# Addon updater preferences.

	auto_check_update = bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False)

	updater_interval_months = bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)

	updater_interval_days = bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)

	updater_interval_hours = bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)

	updater_interval_minutes = bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)

	def draw(self, context):
		layout = self.layout

		# Works best if a column, or even just self.layout.
		mainrow = layout.row()
		col = mainrow.column()

		# Updater draw function, could also pass in col as third arg.
		addon_updater_ops.update_settings_ui(self, context)

		# Alternate draw function, which is more condensed and can be
		# placed within an existing draw function. Only contains:
		#   1) check for update/update now buttons
		#   2) toggle for auto-check (interval will be equal to what is set above)
		# addon_updater_ops.update_settings_ui_condensed(self, context, col)

		# Adding another column to help show the above condensed ui as one column
		# col = mainrow.column()
		# col.scale_y = 2
		# ops = col.operator("wm.url_open","Open webpage ")
		# ops.url=addon_updater_ops.updater.website

# Classes
classes = (
    # Preferences
    HardSurfaceToolPreferences,
    # Actions
    select_operators.OBJECT_OT_SELECT_ACTION,
    modifier_operators.OBJECT_OT_MODIFIER_ACTION,
    vertex_normal_operators.OBJECT_OT_NORMAL_ACTION,
    vertex_group_operators.OBJECT_OT_VERTEXGROUP_ACTION,
    shapekey_operators.OBJECT_OT_SHAPEKEYS_ACTION,
    collection_operators.OBJECT_OT_COLLECTION_ACTION,
    material_operators.OBJECT_OT_MATERIAL_ACTION,
    uv_operators.OBJECT_OT_UV_ACTION,
    bridge_operators.OBJECT_OT_FILE_ACTION,
    model_operators.OBJECT_OT_MODEL_ACTION,
    check_operators.OBJECT_OT_CHECK_ACTION,
    capture_operators.OBJECT_OT_SCREENSHOT_ACTION,
    bakeset_operators.OBJECT_OT_BAKESET_ACTION,
    coalition_operators.OBJECT_OT_COALITION_ACTION,
    # Properties
    properties.My_Properties_Setup,
    # UI
    ui.HardSurfaceToolPanel,
    ui.CoalitionToolPanel,
)

def register():
    # Reload scripts
    reload(select_operators)
    reload(bridge_operators)
    reload(modifier_operators)
    reload(vertex_normal_operators)
    reload(vertex_group_operators)
    reload(shapekey_operators)
    reload(collection_operators)
    reload(uv_operators)
    reload(material_operators)
    reload(model_operators)
    reload(check_operators)
    reload(capture_operators)
    reload(bakeset_operators)
    reload(coalition_operators)
    reload(properties)
    reload(icons)
    reload(ui)

    # Update add-ons
    addon_updater_ops.register(bl_info)

    ## HardSurface Tool
    icons.register()

    # Register
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    # Update add-ons
    addon_updater_ops.unregister()
                               
    ## HardSurface Tool
    icons.unregister()

    # Unregister
    for cls in classes:
        bpy.utils.unregister_class(cls)
    

    