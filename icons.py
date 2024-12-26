import bpy
import os
import bpy.utils.previews

preview_collections = {}

def register():
    global preview_collections
    # --- ICON
    pcoll = bpy.utils.previews.new()
    
    # --- GENERAL
    my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    # --- General
    pcoll.load("false_icon", os.path.join(my_icons_dir, "false.png"), 'IMAGE')
    pcoll.load("true_icon", os.path.join(my_icons_dir, "true.png"), 'IMAGE')
    
    preview_collections["main"] = pcoll

def unregister():
    global preview_collections
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()