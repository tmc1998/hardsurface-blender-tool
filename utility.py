# THIS FILE INCLUDE ALL GLOBAL FUNCTION
import bpy
import os
import json
import tempfile
import bmesh

def get_context(type):
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == type:
                context_override = {"area": area, "screen": screen}
                return context_override

def change_mode_for_check_tool(edit_mode):
    bpy.ops.object.mode_set(mode='EDIT') #Activating Edit mode
    bpy.ops.mesh.select_mode(type=edit_mode) #Changing Edit mode
    bpy.ops.mesh.select_all(action = 'DESELECT') #Deselecting all
    
def read_data_from_json(path):
    json_data = {}
    try:
        with open(path, 'r') as file:
            json_data = json.load(file)
            file.close()
    except:
        pass
    return json_data

def write_json_file(path, content):
    # Serializing json 
    json_object = json.dumps(content, indent = 4)
    # Writing to sample.json
    with open(path, "w") as outfile:
        outfile.write(json_object)
    outfile.close()
    return True

def check_result_return_edit_mode(edit_mode):
    if edit_mode == 'VERTEX':
        selected = [s for s in bpy.context.active_object.data.verts if s.select]
    elif edit_mode == 'EDGE':
        selected = [s for s in bpy.context.active_object.data.edges if s.select]
    elif edit_mode == 'FACE':
        selected = [s for s in bpy.context.active_object.data.polygons if s.select]
    if len(selected) == 0:
        bpy.ops.object.mode_set(mode='OBJECT') #Going back to Object mode

def check_object_exists(object_name):
    current_object = bpy.context.scene.objects.get(object_name)
    if current_object:
        return True
    else:
        return False

def get_selected_vertices(edit_mode):
    # we need to switch from Edit mode to Object mode so the selection gets updated
    bpy.ops.object.mode_set(mode='OBJECT')
    selectedVerts = [v.index for v in bpy.context.active_object.data.vertices if v.select]
    # back to whatever mode we were in
    bpy.ops.object.mode_set(mode=edit_mode)
    return selectedVerts

def get_active_face_index(*arg):
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    if bm.select_history:
        elem = bm.select_history[-1]
        if isinstance(elem, bmesh.types.BMFace):
            return elem.index
    return 0


#region Show Message
global message_content

def draw_message(self, context):
    self.layout.label(text=message_content)

def show_message(context, icon, content):
    global message_content
    message_content = content
    context.window_manager.popup_menu(draw_message, icon=icon)
#endregion

#region bakeset
def make_empty(name, location): #string, vector, string of existing coll
    empty_obj = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(empty_obj)
    empty_obj.empty_display_type = "PLAIN_AXES"
    empty_obj.location = (0, 0, 0)
    return empty_obj

def join_mesh(mesh_list):
    for mesh_name in mesh_list:
        mesh = bpy.data.objects[mesh_name]
        mesh.select_set(state=True)
        bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.join()
    obj = bpy.data.objects[mesh_list[-1]]
    return obj
#endregion