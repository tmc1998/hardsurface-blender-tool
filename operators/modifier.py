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

# --- MODIFIER ACTION LOGIC --- #
class OBJECT_OT_MODIFIER_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
    """Tool tip"""
    bl_idname = "object.modifier_action" # Naming object.add_cube so it will consistent with our class
    bl_label = "Modifier"
    bl_description = 'Custom tools for modifier'

    action: EnumProperty(
        items=[
            ('TOGGLE_MODIFIER', 'toggle modifier', 'toggle modifier'),
            ('APPLY_MODIFIER', 'apply modifier', 'apply modifier'),
            ('OPTIMAL_DISPLAY_SUBDIVISION', 'optimal display subdivision', 'optimal display subdivision'),
            ('SELECT_BEVEL_VERTEX_MODIFIER', 'select bevel vertex modifier', 'select bevel vertex modifier'),
            ('CREATE_BEVEL_MODIFIER', 'create bevel modifier', 'create bevel modifier'),
            ('SELECT_OBJECT_FROM_CURRENT_MIRROR', 'select object from mirror object', 'select object from mirror object'),
            ('SET_CURRENT_MIRROR_TO_TARGET_MIRROR', 'set current mirror to target mirror', 'set current mirror to target mirror'),
            ('SET_LAST_NORMAL_FACE_TO_SELECTED_FACES', 'set last normal face to selected faces', 'set last normal face to selected faces'),
        ]
    )

    def execute(self, context):
        if self.action == 'TOGGLE_MODIFIER':
            self.toggle_modifier_function(context)
        elif self.action == 'APPLY_MODIFIER':
            self.apply_modifier_function(context)
        elif self.action == 'OPTIMAL_DISPLAY_SUBDIVISION':
            self.optimal_display_subdivision_function(context)
        elif self.action == 'SELECT_BEVEL_VERTEX_MODIFIER':
            self.select_bevel_vertex_modifier_function(context)
        elif self.action == 'CREATE_BEVEL_MODIFIER':
            self.create_bevel_modifier_function(context)
        elif self.action == 'SELECT_OBJECT_FROM_CURRENT_MIRROR':
            self.select_object_from_current_mirror_function(context)
        elif self.action == 'SET_CURRENT_MIRROR_TO_TARGET_MIRROR':
            self.set_current_mirror_to_target_mirror_function(context)
        elif self.action == 'SET_LAST_NORMAL_FACE_TO_SELECTED_FACES':
            self.set_last_normal_face_to_selected_faces_function(context)

        return {'FINISHED'}

    def toggle_modifier_function(self, context):
        object_list = bpy.context.selected_objects
        if len(object_list) == 0:
            object_list = bpy.context.scene.objects
        for obj in object_list:
            try:
                modifier_list = obj.modifiers
                for mod in modifier_list:
                    if mod.show_viewport != my_variables.TOGGLE_MODIFIER_BOOL:
                        mod.show_viewport = my_variables.TOGGLE_MODIFIER_BOOL
                    if mod.show_in_editmode != my_variables.TOGGLE_MODIFIER_BOOL:
                        mod.show_in_editmode = my_variables.TOGGLE_MODIFIER_BOOL
                    if mod.show_render != my_variables.TOGGLE_MODIFIER_BOOL:
                        mod.show_render = my_variables.TOGGLE_MODIFIER_BOOL
            except:
                pass
        my_variables.TOGGLE_MODIFIER_BOOL = not my_variables.TOGGLE_MODIFIER_BOOL

    def apply_modifier_function(self, context):
        object_list = bpy.context.selected_objects
        if len(object_list) == 0:
            object_list = bpy.context.scene.objects
        for obj in object_list:
            try:
                bpy.context.view_layer.objects.active = obj
                for mod in obj.modifiers:
                    name = mod.name
                    try:
                        bpy.ops.object.modifier_apply(modifier = name)
                    except:
                        obj.modifiers.remove(mod)
            except:
                pass
        my_utility.show_message(context, "INFO", "Apply Modifier: Done!")

    def optimal_display_subdivision_function(self, context):
        object_list = bpy.context.selected_objects
        if len(object_list) == 0:
            object_list = bpy.context.scene.objects
        for obj in object_list:
            modifier_list = obj.modifiers
            for mod in modifier_list:
                if mod.name == "Subdivision":
                    mod.show_only_control_edges = not my_variables.TOGGLE_OPTIMAL_DISPLAY_BOOL
        my_variables.TOGGLE_OPTIMAL_DISPLAY_BOOL = not my_variables.TOGGLE_OPTIMAL_DISPLAY_BOOL

    def fix_bevel_unit_function(self, context):
        object_list = bpy.context.selected_objects
        for obj in object_list:
            modifier_list = obj.modifiers
            for mod in modifier_list:
                if mod.type == "BEVEL":
                    mod.width = mod.width * context.scene.bevel_unit_value

    def select_bevel_vertex_modifier_function(self, context):
        vtg_list = []
        have_vertex_group_bevel = False
        obj = bpy.context.selected_objects[0]
        selected_vertices = my_utility.get_selected_vertices("EDIT")
    
        for vert in selected_vertices:
            for group in obj.vertex_groups:
                vert_in_group = [vert.index for vert in obj.data.vertices if group.index in [i.group for i in vert.groups]]
                if vert in vert_in_group and group.name not in vtg_list:
                    vtg_list.append(group.name)

        modifier_list = obj.modifiers
        for mod in modifier_list:
            if mod.type == "BEVEL":
                if mod.limit_method == "VGROUP":
                    if mod.vertex_group in vtg_list:
                        mod.show_expanded = True
                        have_vertex_group_bevel = True
                    else:
                        mod.show_expanded = False
                else:
                    mod.show_expanded = False
            else:
                mod.show_expanded = False
        if not have_vertex_group_bevel:
            my_utility.show_message(context, "ERROR", "Object doesn't have bevel vertex group modifier!")

    def create_bevel_modifier_function(self, context):
        is_exists = False
        obj = context.active_object
        for mod in obj.modifiers:
            if mod.type == "BEVEL":
                if mod.name == context.scene.bevel_modifier_name:
                    is_exists = True
                    break
        if not is_exists:
            # Create Bevel Vertex Group Modifier
            mod = obj.modifiers.new(context.scene.bevel_modifier_name, 'BEVEL')
            mod.offset_type = 'OFFSET'
            mod.width = context.scene.bevel_unit_value
            mod.segments = context.scene.bevel_segment_value
            mod.limit_method = context.scene.bevel_type
            mod.miter_outer = 'MITER_ARC'
            mod.miter_inner = 'MITER_SHARP'
            mod.use_clamp_overlap = False
            mod.loop_slide = True
            if context.scene.bevel_type == "VGROUP":
                # Create Vertex Group
                new_vertex_group = bpy.context.object.vertex_groups.new(name=context.scene.bevel_modifier_name)
                bpy.ops.object.vertex_group_assign()
                mod.vertex_group = new_vertex_group.name
            elif context.scene.bevel_type == "WEIGHT":
                mode = bpy.context.active_object.mode
                if mode != 'OBJECT':
                    # we need to switch from Edit mode to Object mode so the selection gets updated
                    bpy.ops.object.mode_set(mode='OBJECT')
                    obj = bpy.context.active_object
                    obj_data = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
                    # create bevel weight edge data
                    if 'bevel_weight_edge' not in obj_data.attributes:
                        obj.data.attributes.new(
                            name='bevel_weight_edge',
                            type='FLOAT',
                            domain='EDGE'
                        )
                    for index, edge in enumerate(obj.data.edges):
                        if edge.select:
                            obj.data.attributes['bevel_weight_edge'].data[index].value = 1.0
                    # back to whatever mode we were in
                    bpy.ops.object.mode_set(mode=mode)
            elif context.scene.bevel_type == "ANGLE":
                mod.angle_limit = 1.0471975512 # 60 Degrees
        else:
            my_utility.show_message(context, "ERROR", "This name already exists. Please enter another name!")

    def select_object_from_current_mirror_function(self, context):
        if my_utility.check_object_exists(context.scene.current_mirror_object_name) or context.scene.current_mirror_object_name == '':
            mirror_object_list = []
            mesh_list = [obj for obj in bpy.context.scene.objects if obj.type=='MESH']
            for obj in mesh_list:
                bpy.context.view_layer.objects.active = obj
                for mod in obj.modifiers:
                    if mod.type == 'MIRROR':
                        if mod.mirror_object == None:
                            if context.scene.current_mirror_object_name == '':
                                mirror_object_list.append(obj)
                        else:
                            if mod.mirror_object.name == context.scene.current_mirror_object_name:
                                mirror_object_list.append(obj)
            if mirror_object_list == []:
                my_utility.show_message(context, "ERROR", "No object selected!")
            else:
                bpy.ops.object.mode_set(mode = 'OBJECT')
                for obj in mirror_object_list:
                    obj.select_set(True)
                my_utility.show_message(context, "INFO", "Select: Done!")
        else:
            my_utility.show_message(context, "ERROR", "Target Mirror isn't exists!")
        

    def set_current_mirror_to_target_mirror_function(self, context):
        if my_utility.check_object_exists(context.scene.current_mirror_object_name) or context.scene.current_mirror_object_name == '':
            mesh_list = [obj for obj in bpy.context.scene.objects if obj.type=='MESH']
            for obj in mesh_list:
                bpy.context.view_layer.objects.active = obj
                for mod in obj.modifiers:
                    if mod.type == 'MIRROR':
                        if mod.mirror_object != None:
                            if mod.mirror_object.name == context.scene.current_mirror_object_name:
                                if context.scene.target_mirror_object_name == '':
                                    mod.mirror_object = None
                                else:
                                    mod.mirror_object = bpy.data.objects[context.scene.target_mirror_object_name]
                        elif context.scene.current_mirror_object_name == '':
                            if context.scene.target_mirror_object_name == '':
                                    mod.mirror_object = None
                            else:
                                mod.mirror_object = bpy.data.objects[context.scene.target_mirror_object_name]
            empty_list = [obj for obj in bpy.context.scene.objects if obj.type=='EMPTY']
            for em in empty_list:
                if context.scene.current_mirror_object_name == em.name:
                    bpy.data.objects.remove(em, do_unlink=True)
            my_utility.show_message(context, "INFO", "Change: Done!")
        else:
            my_utility.show_message(context, "ERROR", "Target Mirror isn't exists!")
        
        