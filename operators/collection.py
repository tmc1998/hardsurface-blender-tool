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

# --- COLLECTION ACTION LOGIC --- #
class OBJECT_OT_COLLECTION_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
    """Tool tip"""
    bl_idname = "object.collection_action" # Naming object.add_cube so it will consistent with our class
    bl_label = "Collection"
    bl_description = 'Custom tools for collection'

    action: EnumProperty(
        items=[
            ('TOGGLE_HIDE_COLLECTION', 'toggle hide_collection', 'toggle hide_collection'),
            ('TOGGLE_COLLECTION_COLOR0', 'toggle collection color 0', 'toggle collection color 0'),
            ('TOGGLE_COLLECTION_COLOR1', 'toggle collection color 1', 'toggle collection color 1'),
            ('TOGGLE_COLLECTION_COLOR2', 'toggle collection color 2', 'toggle collection color 2'),
            ('TOGGLE_COLLECTION_COLOR3', 'toggle collection color 3', 'toggle collection color 3'),
            ('TOGGLE_COLLECTION_COLOR4', 'toggle collection color 4', 'toggle collection color 4'),
            ('TOGGLE_COLLECTION_COLOR5', 'toggle collection color 5', 'toggle collection color 5'),
            ('TOGGLE_COLLECTION_COLOR6', 'toggle collection color 6', 'toggle collection color 6'),
            ('TOGGLE_COLLECTION_COLOR7', 'toggle collection color 7', 'toggle collection color 7'),
            ('TOGGLE_COLLECTION_COLOR8', 'toggle collection color 8', 'toggle collection color 8'),
        ]
    )

    def execute(self, context):
        if self.action == 'TOGGLE_HIDE_COLLECTION':
            self.toggle_hide_collection_function(context)
        elif 'TOGGLE_COLLECTION_COLOR' in self.action:
            index = int(self.action.replace('TOGGLE_COLLECTION_COLOR', ''))
            self.toggle_collection_color_function(context, index)

        return {'FINISHED'}

    def getChildrenCollectionRecursion(self, result_list, collection_list):
        for children_collection in collection_list:
            result_list.append(children_collection)
            self.getChildrenCollectionRecursion(result_list, children_collection.children)
    
    def toggle_hide_collection_function(self, context):
        # Fetch the area
        outliner = next(a for a in bpy.context.screen.areas if a.type == "OUTLINER") 
        outliner.spaces[0].show_restrict_column_viewport = True

        #Get all Layer Collection
        result_list = []
        children_list = bpy.context.view_layer.layer_collection.children
        self.getChildrenCollectionRecursion(result_list, children_list)
        if my_variables.UNHIDE_COLLECTION_BOOL == True:
            my_variables.HIDE_COLLECTION_LIST = []
            for collection in result_list:
                if collection.hide_viewport == True or bpy.data.collections[collection.name].hide_viewport == True:
                    collection.hide_viewport = False
                    bpy.data.collections[collection.name].hide_viewport = False
                    my_variables.HIDE_COLLECTION_LIST.append(collection)
                collection.exclude = False
                bpy.data.collections[collection.name].hide_select = False
                bpy.data.collections[collection.name].hide_render = False
        else:
            for collection in my_variables.HIDE_COLLECTION_LIST:
                collection.hide_viewport = True
                bpy.data.collections[collection.name].hide_viewport = True
                collection.exclude = False
                bpy.data.collections[collection.name].hide_select = False
                bpy.data.collections[collection.name].hide_render = False
        my_variables.UNHIDE_COLLECTION_BOOL = not my_variables.UNHIDE_COLLECTION_BOOL

    def toggle_collection_color_function(self, context, index):
        # Fetch the area
        outliner = next(a for a in bpy.context.screen.areas if a.type == "OUTLINER") 
        outliner.spaces[0].show_restrict_column_viewport = True

        # Get all Layer Collection
        result_list = []
        children_list = bpy.context.view_layer.layer_collection.children
        self.getChildrenCollectionRecursion(result_list, children_list)

        for collection in result_list:
            if index != 0:
                if bpy.data.collections[collection.name].color_tag == "COLOR_0" + str(index):
                    collection.hide_viewport = my_variables.TOGGLE_COLLECTION_BOOL_LIST[index]
                    bpy.data.collections[collection.name].hide_viewport = my_variables.TOGGLE_COLLECTION_BOOL_LIST[index]
                    collection.exclude = False
                    bpy.data.collections[collection.name].hide_select = False
                    bpy.data.collections[collection.name].hide_render = False
            else:
                if bpy.data.collections[collection.name].color_tag == "NONE":
                    collection.hide_viewport = my_variables.TOGGLE_COLLECTION_BOOL_LIST[index]
                    bpy.data.collections[collection.name].hide_viewport = my_variables.TOGGLE_COLLECTION_BOOL_LIST[index]
                    collection.exclude = False
                    bpy.data.collections[collection.name].hide_select = False
                    bpy.data.collections[collection.name].hide_render = False
        
        my_variables.TOGGLE_COLLECTION_BOOL_LIST[index] = not my_variables.TOGGLE_COLLECTION_BOOL_LIST[index]