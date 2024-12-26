import os
import bpy
import bmesh
import math
from mathutils import *
from bpy.props import EnumProperty

try:
    from imp import reload
except:
    pass

import Shiro_Tools.variable as my_variables
reload(my_variables)

import Shiro_Tools.utility as my_utility
reload(my_utility)

# --- SCREENSHOT ACTION LOGIC --- #
class OBJECT_OT_SCREENSHOT_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
    """Tool tip"""
    bl_idname = "object.screenshot_action" # Naming object.add_cube so it will consistent with our class
    bl_label = "Screenshot"
    bl_description = 'Custom tools for screenshot'

    action: EnumProperty(
        items=[
            ('AUTO_SCREENSHOT', 'auto screenshot', 'auto screenshot'),
            ('CUSTOM_SCREENSHOT', 'custom screenshot', 'custom screenshot'),
        ]
    )

    def execute(self, context):
        if self.action == 'CUSTOM_SCREENSHOT':
            self.screenshot_function(context, 'custom')
        elif self.action == 'AUTO_SCREENSHOT':
            self.screenshot_function(context, 'auto')
        return {'FINISHED'}

    def setting_auto_screenshot_function(self, context, camera_name, camera_zoom):
        if 'persp' not in camera_name:
            bpy.ops.view3d.view_axis(type=camera_name.upper(), align_active=False, relative=False)
            if camera_name == 'top' or camera_name == 'bottom':
                for i in range(6):
                    bpy.ops.view3d.view_orbit(type='ORBITLEFT')
        else:
            bpy.ops.view3d.view_axis(type='LEFT', align_active=False, relative=False)
            bpy.context.space_data.region_3d.view_perspective = 'PERSP'
            if camera_name == 'persp1':
                for i in range(3):
                    bpy.ops.view3d.view_orbit(type='ORBITRIGHT')
            elif camera_name == 'persp2':
                for i in range(9):
                    bpy.ops.view3d.view_orbit(type='ORBITRIGHT')
            elif camera_name == 'persp3':
                for i in range(3):
                    bpy.ops.view3d.view_orbit(type='ORBITLEFT')
            elif camera_name == 'persp4':
                for i in range(9):
                    bpy.ops.view3d.view_orbit(type='ORBITLEFT')
        if len(bpy.context.selected_objects) > 0:
            bpy.ops.view3d.view_selected()
            bpy.ops.object.select_all(action='DESELECT')
        else:
            bpy.ops.view3d.view_all(center=False)
        if 'persp' not in camera_name:
            bpy.ops.view3d.zoom(delta=1)
        zoom_value = int((context.scene.camera_zoom_value - 100) / 10)
        for _ in range(abs(zoom_value)):
            if zoom_value > 0:
                bpy.ops.view3d.zoom(delta=1)
            else:
                bpy.ops.view3d.zoom(delta=-1)

    def toggle_scene_elements(self, context, toggle):
        bpy.context.space_data.overlay.show_floor = toggle
        bpy.context.space_data.overlay.show_cursor = toggle
        bpy.context.space_data.overlay.show_ortho_grid = toggle
        bpy.context.space_data.overlay.show_axis_x = toggle
        bpy.context.space_data.overlay.show_axis_y = toggle
        bpy.context.space_data.region_3d.view_perspective = 'PERSP'

    def screenshot_function(self, context, mode):

        # Get file name
        file_name = bpy.path.basename(bpy.context.blend_data.filepath).rsplit(".", 1)[0]
        folder_path = context.scene.screenshot_path
        # Screenshot path
        image_path = folder_path + file_name

        # Get selected objects
        selected_objects = bpy.context.selected_objects

        # Get camera zoom
        camera_zoom = context.scene.camera_zoom_value

        # Capture
        ## Auto
        if mode == 'auto':
            # Loop Camera
            for camera_name in my_variables.CAMERA_LIST:
                self.setting_auto_screenshot_function(context, camera_name, camera_zoom)
                self.capture_on_current_view(context, image_path, camera_name)
                for o in selected_objects:
                    o.select_set(True)
        ## Custom
        else:
            tmp_image_path = folder_path + file_name + "_custom_1.png"
            i = 1
            while os.path.exists(tmp_image_path):
                i += 1
                tmp_image_path = folder_path + file_name + "_custom_" + str(i) + ".png" 
            self.capture_on_current_view(context, image_path, "custom_" + str(i))
        
        # Open screenshot folder
        my_utility.show_message(context, "INFO", "Screenshot: Done!")	
        os.startfile(folder_path)
    
    def capture_on_current_view(self, context, image_path, camera_name):
        context.scene.render.filepath = image_path + "_" + camera_name + ".png"
        context.scene.render.resolution_x = 3840
        context.scene.render.resolution_y = 2160
        bpy.ops.render.opengl(write_still=True, view_context=True)