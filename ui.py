
import bpy

try:
    from imp import reload
except:
    pass

from . import variable as my_variables
reload(my_variables)

from .icons import preview_collections

# UI LOGIC

class HardSurfaceToolPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_HardSurfaceToolPanel" # _PT_ : help blender define which is Panel||Menu||Operator
    bl_label = "HardSurface Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "HS Tool"

    def draw(self, context):
        # Icon 
        pcoll = preview_collections['main']
        true_icon = pcoll['true_icon']
        false_icon = pcoll['false_icon']

        # Scene
        scene = context.scene

        # Main layout
        main_layout = self.layout

        # Tool Tab Box UI
        tab_box = main_layout.box()
        tab_row = tab_box.row(align=True)
        tab_row.scale_y = 1.5
        for index, item in enumerate(context.scene.bl_rna.properties["hardsurface_tool_tab"].enum_items):   
            tab_row.prop_enum(context.scene, "hardsurface_tool_tab", item.identifier)
            if index == 2: # new line after third item
                tab_row = tab_box.row(align=True) 
                tab_row.scale_y = 1.5
        
        # Modifier Tab UI
        if scene.hardsurface_tool_tab == "MODIFIER":
                        
            ## Toggle & Apply
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_apply_modifier_ui:
                split.prop(scene, "toggle_apply_modifier_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_apply_modifier_ui", text="", icon="RIGHTARROW")
            split.label(text="Toggle & Apply")
            if scene.toggle_apply_modifier_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.operator("object.modifier_action", text = "Toggle Modifiers").action = "TOGGLE_MODIFIER"
                row.scale_y = 2.0
                row = child_box.row(align=True)
                row.operator("object.modifier_action", text = "Apply Modifier").action = "APPLY_MODIFIER"
                row.scale_y = 1.5
            
            ## Subdivision
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_subdivision_modifier_ui:
                split.prop(scene, "toggle_subdivision_modifier_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_subdivision_modifier_ui", text="", icon="RIGHTARROW")
            split.label(text="Subdivision")
            if scene.toggle_subdivision_modifier_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.operator("object.modifier_action", text = "Optimal Display").action = "OPTIMAL_DISPLAY_SUBDIVISION"
                row.scale_y = 1.5

            ## Bevel
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_bevel_modifier_ui:
                split.prop(scene, "toggle_bevel_modifier_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_bevel_modifier_ui", text="", icon="RIGHTARROW")
            split.label(text="Bevel")
            if scene.toggle_bevel_modifier_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.prop(scene, "bevel_modifier_name", text="")
                row.prop(scene, "bevel_type", text="")
                row = child_box.row(align=True)
                row.prop(scene, "bevel_unit_value", text="Value")
                row = child_box.row(align=True)
                row.prop(scene, "bevel_segment_value", text="Segment")
                row = child_box.row(align=True)
                row.operator("object.modifier_action", text = "Create Bevel").action = "CREATE_BEVEL_MODIFIER"
                row.scale_y = 2.0
                row = child_box.row(align=True)
                row.operator("object.modifier_action", text = "Get Bevel Modifiers (Vertex)").action = "SELECT_BEVEL_VERTEX_MODIFIER"
                row.scale_y = 1.5

            ## Mirror
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_mirror_modifier_ui:
                split.prop(scene, "toggle_mirror_modifier_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_mirror_modifier_ui", text="", icon="RIGHTARROW")
            split.label(text="Mirror")
            if scene.toggle_mirror_modifier_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.prop(scene, "current_mirror_object_name", text="Source")

                row = child_box.row(align=True)
                row.prop(scene, "target_mirror_object_name", text="Target")

                row = child_box.row(align=True)
                row.operator("object.modifier_action", text = "Select Object From Source").action = "SELECT_OBJECT_FROM_CURRENT_MIRROR"
                row.scale_y = 1.5

                row = child_box.row(align=True)
                row.operator("object.modifier_action", text = "Set Mirror To Target").action = "SET_CURRENT_MIRROR_TO_TARGET_MIRROR"
                row.scale_y = 1.5

        # Model Tab UI
        if scene.hardsurface_tool_tab == "MODEL":

            ## Edge Length
            main_box = main_layout.box()
            row = main_box.row(align=True)
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_edge_length_ui:
                split.prop(scene, "toggle_edge_length_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_edge_length_ui", text="", icon="RIGHTARROW")
            split.prop(scene, "edge_length_value", text="")
            split.operator("object.model_action", text = "Set Edge").action = "SET_EDGE_LENGTH"
            row.scale_y = 2.0
            if scene.toggle_edge_length_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                col = row.column(align=True)
                col.operator("object.model_action", text = "Get Length").action = "GET_EDGE_LENGTH"
                col.scale_y = 2.0
                col = row.column(align=True)
                child_row = col.row(align=True)
                child_row.operator("object.model_action", text = "Add Lock Vertex").action = "ADD_LOCK_VERTEX"
                child_row = col.row(align=True)
                child_row.operator("object.model_action", text = "Clear").action = "CLEAR_LOCK_VERTEX_LIST"
                if my_variables.LOCK_VERTEX_INDEX_LIST == []:
                    child_row.enabled = False
            
            ## Circle Edge
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_circle_edge_ui:
                split.prop(scene, "toggle_circle_edge_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_circle_edge_ui", text="", icon="RIGHTARROW")
            split.operator("object.model_action", text = "Alignment Edge").action = "ALIGN_CIRCLE_VERTEX"
            row.scale_y = 2.0
            if scene.toggle_circle_edge_ui:
                # Line 1
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.scale_y = 1.2
                col = row.column(align=True)
                col.prop(scene, "circle_diameter_toggle", text="Diameter")
                col = row.column(align=True)
                col.prop(scene, "circle_diameter_value", text="")
                if context.scene.circle_diameter_toggle == False:
                    col.enabled = False 
                col = row.column(align=True)
                col.operator("object.model_action", text = "Get").action = "GET_CIRCLE_DIAMETER"
                # Line 2
                row = child_box.row(align=True)
                row.scale_y = 1.2
                col = row.column(align=True)
                col.prop(scene, "circle_angle_toggle", text="Angle")
                col = row.column(align=True)
                col.prop(scene, "circle_angle_value", text="")
                if context.scene.circle_angle_toggle == False:
                    col.enabled = False 
                col = row.column(align=True)
                col.operator("object.model_action", text = "Get").action = "GET_CIRCLE_ANGLE"
                # Line 3
                row = child_box.row(align=True)
                row.scale_y = 1.5
                col = row.column(align=True)
                col.operator("object.model_action", text = "Add Lock Vertex").action = "ADD_PRIORITY_VERTEX"
                col = row.column(align=True)
                col.operator("object.model_action", text = "Clear").action = "CLEAR_PRIORITY_VERTEX"
                if my_variables.PRIORITY_CIRCLE_VERTEX_INDEX_LIST == []:
                    col.enabled = False

                # row = child_box.row(align=True)
                # row.operator("object.model_action", text = "Alignment").action = "ALIGN_CIRCLE_VERTEX"
                # row.scale_y = 2.0

            ## Straight Edge
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_straight_edge_ui:
                split.prop(scene, "toggle_straight_edge_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_straight_edge_ui", text="", icon="RIGHTARROW")
            split.operator("object.model_action", text = "Straight Edge").action = "STRAIGHT_EDGE"
            row.scale_y = 2.0
            if scene.toggle_straight_edge_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.prop(scene, "straight_axis_radiobox", expand = True)
                row = child_box.row(align=True)
                row.prop(scene, "even_straight_toggle", text="Even")
                if context.scene.straight_axis_radiobox != "All":
                    row.enabled = False


            ## Relax Edge
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_relax_edge_ui:
                split.prop(scene, "toggle_relax_edge_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_relax_edge_ui", text="", icon="RIGHTARROW")
            split.operator("object.model_action", text = "Relax Edge").action = "RELAX_EDGE"
            row.scale_y = 2.0
            if scene.toggle_relax_edge_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.prop(scene, "relax_interpolation")
                row = child_box.row(align=True)
                row.prop(scene, "relax_input")
                row = child_box.row(align=True)
                row.prop(scene, "relax_iterations")
                row = child_box.row(align=True)
                row.prop(scene, "relax_regular")


            ## Space Edge
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_space_edge_ui:
                split.prop(scene, "toggle_space_edge_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_space_edge_ui", text="", icon="RIGHTARROW")
            split.operator("object.model_action", text = "Space Edge").action = "SPACE_EDGE"
            row.scale_y = 2.0
            if scene.toggle_space_edge_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.prop(scene, "space_interpolation")
                row = child_box.row(align=True)
                row.prop(scene, "space_input")
                row = child_box.row(align=True)
                if scene.space_lock_x:
                    row.prop(scene, "space_lock_x", text="X", icon="LOCKED")
                else:
                    row.prop(scene, "space_lock_x", text="X", icon="UNLOCKED")
                if scene.space_lock_y:
                    row.prop(scene, "space_lock_y", text="Y", icon="LOCKED")
                else:
                    row.prop(scene, "space_lock_y", text="Y", icon="UNLOCKED")
                if scene.space_lock_z:
                    row.prop(scene, "space_lock_z", text="Z", icon="LOCKED")
                else:
                    row.prop(scene, "space_lock_z", text="Z", icon="UNLOCKED")
                row = child_box.row(align=True)
                row.prop(scene, "space_influence")

            ## Flatten Face
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_flatten_face_ui:
                split.prop(scene, "toggle_flatten_face_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_flatten_face_ui", text="", icon="RIGHTARROW")
            split.operator("object.model_action", text = "Flatten Face").action = "FLATTEN_FACE"
            row.scale_y = 2.0
            if scene.toggle_flatten_face_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.prop(scene, "flatten_plane")
                row = child_box.row(align=True)
                row.prop(scene, "flatten_restriction")
                row = child_box.row(align=True)
                if scene.flatten_lock_x:
                    row.prop(scene, "flatten_lock_x", text="X", icon='LOCKED')
                else:
                    row.prop(scene, "flatten_lock_x", text="X", icon='UNLOCKED')
                if scene.flatten_lock_y:
                    row.prop(scene, "flatten_lock_y", text="Y", icon='LOCKED')
                else:
                    row.prop(scene, "flatten_lock_y", text="Y", icon='UNLOCKED')
                if scene.flatten_lock_z:
                    row.prop(scene, "flatten_lock_z", text="Z", icon='LOCKED')
                else:
                    row.prop(scene, "flatten_lock_z", text="Z", icon='UNLOCKED')
                row = child_box.row(align=True)
                row.prop(scene, "flatten_influence")
            
            ## Clone element
            main_box = main_layout.box()
            row = main_box.row()
            row.operator("object.model_action", text = "Clone Element").action = "CLONE_ELEMENT"
            row.scale_y = 2.0

        # Misc Tab UI
        if scene.hardsurface_tool_tab == "MISC":
            ## Select Group
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_selection_area_ui:
                split.prop(scene, "toggle_selection_area_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_selection_area_ui", text="", icon="RIGHTARROW")
            split.label(text="Select")
            if scene.toggle_selection_area_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.operator("object.select_action", text = "Select Continue Edge Loop").action = "SELECT_CONTINUE_EDGE_LOOP"
                row.scale_y = 1.5
                row = child_box.row(align=True)
                row.operator("object.select_action", text = "Select Continue Edge Ring").action = "SELECT_CONTINUE_EDGE_RING"
                row.scale_y = 1.5


            ## Collection
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_collection_area_ui:
                split.prop(scene, "toggle_collection_area_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_collection_area_ui", text="", icon="RIGHTARROW")
            split.label(text="Collection")
            if scene.toggle_collection_area_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.operator("object.collection_action", text = "Toggle Hide Collections").action = "TOGGLE_HIDE_COLLECTION"
                row.scale_y = 1.5
                row = child_box.row(align=True)
                row.operator("object.collection_action", icon = "OUTLINER_COLLECTION", text = " ").action = "TOGGLE_COLLECTION_COLOR0"
                row.operator("object.collection_action", icon = "COLLECTION_COLOR_01", text = " ").action = "TOGGLE_COLLECTION_COLOR1"
                row.operator("object.collection_action", icon = "COLLECTION_COLOR_02", text = " ").action = "TOGGLE_COLLECTION_COLOR2"
                row.operator("object.collection_action", icon = "COLLECTION_COLOR_03", text = " ").action = "TOGGLE_COLLECTION_COLOR3"
                row.operator("object.collection_action", icon = "COLLECTION_COLOR_04", text = " ").action = "TOGGLE_COLLECTION_COLOR4"
                row.operator("object.collection_action", icon = "COLLECTION_COLOR_05", text = " ").action = "TOGGLE_COLLECTION_COLOR5"
                row.operator("object.collection_action", icon = "COLLECTION_COLOR_06", text = " ").action = "TOGGLE_COLLECTION_COLOR6"
                row.operator("object.collection_action", icon = "COLLECTION_COLOR_07", text = " ").action = "TOGGLE_COLLECTION_COLOR7"
                row.operator("object.collection_action", icon = "COLLECTION_COLOR_08", text = " ").action = "TOGGLE_COLLECTION_COLOR8"

            ## Normal
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_normal_area_ui:
                split.prop(scene, "toggle_normal_area_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_normal_area_ui", text="", icon="RIGHTARROW")
            split.label(text="Normal")
            if scene.toggle_normal_area_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.operator("object.normal_action", text = "Set Normal From Last Face").action = "SET_LAST_NORMAL_FACE_TO_SELECTED_FACES"
                row.scale_y = 1.5

            ## Vertex Group
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_vertex_group_area_ui:
                split.prop(scene, "toggle_vertex_group_area_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_vertex_group_area_ui", text="", icon="RIGHTARROW")
            split.label(text="Vertex Group")
            if scene.toggle_vertex_group_area_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.operator("object.vertexgroup_action", text = "Clear Vertex Group").action = "CLEAR_VERTEX_GROUP"
                row.scale_y = 1.5

            ## Material
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_material_area_ui:
                split.prop(scene, "toggle_material_area_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_material_area_ui", text="", icon="RIGHTARROW")
            split.label(text="Material")
            if scene.toggle_material_area_ui:
                child_box = main_box.box()
                row = child_box.row(align=True)
                row.operator("object.material_action", text = "Delete Duplicate Materials").action = "DELETE_DUPLICATE_MATERIALS"
                row.scale_y = 1.5
                row = child_box.row(align=True)
                row.operator("object.material_action", text = "Delete All Material Slots").action = "DELETE_ALL_MATERIAL_SLOTS"
                row.scale_y = 1.5
                row = child_box.row(align=True)
                row.operator("object.material_action", text = "Clear All Materials").action = "DELETE_ALL_MATERIALS"
                row.scale_y = 1.5

            ## UV
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_uv_area_ui:
                split.prop(scene, "toggle_uv_area_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_uv_area_ui", text="", icon="RIGHTARROW")
            split.label(text="UV")
            if scene.toggle_uv_area_ui:
                child_box = main_box.box()
                row = child_box.row()
                row.prop(scene, "uvset1_name", text="UV1")
                row.operator("object.uv_action", text = "Rename").action = "RENAME_UVSET1"
                row.scale_y = 1.5
                row = child_box.row(align=True)
                row.operator("object.uv_action", text = "Delete Redundant UVSet").action = "DELETE_REDUNDANT_UVSET"
                row.scale_y = 1.5

            ## Bake Set
            main_box = main_layout.box()
            row = main_box.row()
            split = row.split(factor=0.15, align=True)
            if context.scene.toggle_bakeset_area_ui:
                split.prop(scene, "toggle_bakeset_area_ui", text="", icon="DOWNARROW_HLT")
                
            else:
                split.prop(scene, "toggle_bakeset_area_ui", text="", icon="RIGHTARROW")
            split.label(text="Bake Set")
            if scene.toggle_bakeset_area_ui:
                child_box = main_box.box()
                row = child_box.row()
                row.prop(scene, "bakeset_name", text="Name")
                row.scale_y = 1.5
                
                row = child_box.row()
                row.prop(scene, "threshold_value", text="Threshold")
                row.scale_y = 1.5

                row = child_box.row()
                row.operator("object.bakeset_action", text = "Rename Highpoly").action = "RENAME_HIGHPOLY"
                row.scale_y = 1.5
                row = child_box.row()
                row.operator("object.bakeset_action", text = "Create Bake Set").action = "CREATE_BAKESET"
                row.scale_y = 1.5
                row = child_box.row()
                row.operator("object.bakeset_action", text = "Auto Create Bake Set").action = "AUTO_CREATE_BAKESET"
                row.scale_y = 1.5

                row = child_box.row()
                row.prop(scene, "bakeset_export_path", text="Path")
                row.scale_y = 1.5

                row = child_box.row()
                row.prop(scene, "export_bakeset_mode", text="Mode")
                row.scale_y = 1.5

                row = child_box.row()
                row.prop(scene, "export_bakeset_unlock_normal", text="Unlock Normal")
                row.scale_y = 1.5

                row = child_box.row()
                row.operator("object.bakeset_action", text = "Export Selected High/Low Objects").action = "EXPORT_SELECTED_HIGH_LOW"
                row.scale_y = 1.5
                
                row = child_box.row()
                row.operator("object.bakeset_action", text = "Export All Bake Set").action = "EXPORT_ALL_BAKESET"
                row.scale_y = 1.5

        # Check Tab UI
        if scene.hardsurface_tool_tab == "CHECK":
            ## Check Model
            main_box = main_layout.box()
            row = main_box.row(align=True)
            row.label(text="Model")
            child_box = main_box.box()
            row = child_box.row(align=True)
            row.operator("object.check_action", text = "Check All").action = "CHECK_ALL"
            row.scale_y = 1.5
            row = child_box.row(align=True)
            split = row.split(factor=0.85, align=True)
            split.operator("object.check_action", text = "Check N-gons Face").action = "CHECK_NGONS_FACE"
            if scene.check_ngons_face:
                split.operator("object.check_action", text = "", icon_value = true_icon.icon_id)
            else:
                split.operator("object.check_action", text = "", icon_value = false_icon.icon_id)
            row.scale_y = 1.5
            
            row = child_box.row(align=True)
            split = row.split(factor=0.85, align=True)
            split.operator("object.check_action", text = "Check Non-manifold").action = "CHECK_NON_MANIFOLD"
            if scene.check_non_manifold:
                split.operator("object.check_action", text = "", icon_value = true_icon.icon_id)
            else:
                split.operator("object.check_action", text = "", icon_value = false_icon.icon_id)
            row.scale_y = 1.5

            row = child_box.row(align=True)
            split = row.split(factor=0.85, align=True)
            split.operator("object.check_action", text = "Check Concave Face").action = "CHECK_CONCAVE_FACE"
            if scene.check_concave_face:
                split.operator("object.check_action", text = "", icon_value = true_icon.icon_id)
            else:
                split.operator("object.check_action", text = "", icon_value = false_icon.icon_id)
            row.scale_y = 1.5

            row = child_box.row(align=True)
            split = row.split(factor=0.85, align=True)
            split.operator("object.check_action", text = "Check Isolated Vertex").action = "CHECK_ISOLATED_VERTEX"
            if scene.check_isolated_vertex:
                split.operator("object.check_action", text = "", icon_value = true_icon.icon_id)
            else:
                split.operator("object.check_action", text = "", icon_value = false_icon.icon_id)
            row.scale_y = 1.5


            child_box = main_box.box()
            row = child_box.row()
            split = row.split(factor=0.7)
            split.operator("object.check_action", text = "Check Silhouette").action = "CHECK_SILHOUETTE"
            split.prop(scene, "viewport_background_color", text="")
            split.scale_y = 1.5

            # ## Check UV
            # row = main_box.row(align=True)
            # row.label(text="UV - Coming Soon!")
            # child_box = main_box.box()

            # ## Check Material
            # row = main_box.row(align=True)
            # row.label(text="Material - Coming Soon!")
            # child_box = main_box.box()

        # Bridge Tab UI
        if scene.hardsurface_tool_tab == "BRIDGE":
            ## Maya - Blender
            main_box = main_layout.box()
            row = main_box.row(align=True)
            row.label(text="Maya")
            child_box = main_box.box()
            row = child_box.row(align=True)
            split = row.split(factor=0.2, align=True)
            row.label(text = "Normal:", icon="NORMALS_VERTEX_FACE")
            row.prop(scene, "blender_maya_normal_radiobox", expand = True)
            row = child_box.row(align=True)
            row.operator("object.file_action", text = "Export Maya", icon="EXPORT").action = "BLENDER_TO_MAYA"
            row.operator("object.file_action", text = "Import Maya", icon="IMPORT").action = "MAYA_TO_BLENDER"
            row.scale_y = 1.5


            ## RizomUV - Blender
            # main_box = main_layout.box()
            # row = main_box.row(align=True)
            # row.label(text="Rizom")
            # child_box = main_box.box()
            # row = child_box.row(align=True)
            # row.operator("object.file_action", text = "Open Rizom", icon="FILE").action  = "OPEN_RIZOM"
            # row.prop(scene, "rizom_path")
            # row.scale_y = 1.5
            # row = child_box.row(align=True)
            # row.operator("object.file_action", text = "Export Rizom", icon="EXPORT")
            # row.operator("object.file_action", text = "Import Rizom", icon="IMPORT")
            # row.scale_y = 1.5

        # Capture Tab UI
        if scene.hardsurface_tool_tab == "CAPTURE":
            main_box = main_layout.box()
            row = main_box.row(align=True)
            row.label(text="Screenshot")
            # Line 1
            row = main_box.row()
            row.prop(scene, "screenshot_path")
            row.scale_y = 1.5
            # Line 2
            row = main_box.row(align=True)
            row.prop(scene, "camera_zoom_value", text = "Zoom ")
            row.scale_y = 1.5
            # Line 3
            row = main_box.row()
            row.scale_y = 2.0
            row.operator("object.screenshot_action", text="Auto", icon="SCENE").action = "AUTO_SCREENSHOT"
            row.operator("object.screenshot_action", text="Custom", icon="RESTRICT_RENDER_OFF").action = "CUSTOM_SCREENSHOT"

class CoalitionToolPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_CoalitionToolPanel" # _PT_ : help blender define which is Panel||Menu||Operator
    bl_label = "Coalition Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Coalition"

    def draw(self, context):
        # Icon 
        pcoll = preview_collections['main']
        true_icon = pcoll['true_icon']
        false_icon = pcoll['false_icon']

        # Scene
        scene = context.scene

        # Main layout
        main_layout = self.layout

        # Tool Tab Box UI
        main_box = main_layout.box()
        row = main_box.row()
        split = row.split(factor=0.15, align=True)
        if context.scene.toggle_coalition_material_area_ui:
            split.prop(scene, "toggle_coalition_material_area_ui", text="", icon="DOWNARROW_HLT")
            
        else:
            split.prop(scene, "toggle_coalition_material_area_ui", text="", icon="RIGHTARROW")
        split.label(text="Material Setup")
        if context.scene.toggle_coalition_material_area_ui:
            child_box = main_box.box()
            row = child_box.row()
            row.prop(scene, "coalition_stage", text="Stage")
            row.scale_y = 1.5
            row = child_box.row()
            split = row.split(factor=0.24)
            split.label(text = "UDIM:")
            split.prop(scene, "udim_number")
            row.scale_y = 1.5
            row = child_box.row()
            row.operator("object.coalition_action", text = "Create Material List").action = "CREATE_COALITION_MATERIAL_LIST"
            row.scale_y = 1.5
            row = child_box.row()
            row.operator("object.coalition_action", text = "Clear Materials").action = "CLEAR_MATERIALS_IN_SCENE"
            row.scale_y = 1.5
    
        row = main_box.row()
        split = row.split(factor=0.15, align=True)
        if context.scene.toggle_coalition_shapekey_area_ui:
            split.prop(scene, "toggle_coalition_shapekey_area_ui", text="", icon="DOWNARROW_HLT")
            
        else:
            split.prop(scene, "toggle_coalition_shapekey_area_ui", text="", icon="RIGHTARROW")
        split.label(text="Shape Keys Setup")
        if context.scene.toggle_coalition_shapekey_area_ui:
            child_box = main_box.box()
            row = child_box.row()
            row.operator("object.coalition_action", text = "Setup Sculpting Shape Keys").action = "SETUP_SHAPE_KEYS"
            row.scale_y = 1.5

# class SelectPanel(ModelTool_UI, bpy.types.Panel):
#     bl_idname = "OBJECT_PT_SelectPanel" # _PT_ : help blender define which is Panel||Menu||Operator
#     bl_label = "Select"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "Model"

#     def draw(self, context):
#         # Scene
#         scene = context.scene
#         # Main layout
#         main_layout = self.layout

#         # Set panel size
#         main_col_layout = main_layout.column(align=True)
        
#         # Some data on the subpanel

#         #region Select edge loop, ring
#         fast_select_edges_layout = main_col_layout.column()
#         select_continue_edges_box = fast_select_edges_layout.box()
#         select_continue_edges_row = select_continue_edges_box.row(align=True)
#         select_continue_edges_row.operator("object.model_action", text = "Select Continue Edge Loop").action = "SELECT_CONTINUE_EDGE_LOOP"
#         select_continue_edges_row = select_continue_edges_box.row(align=True)
#         select_continue_edges_row.operator("object.model_action", text = "Select Continue Edge Ring").action = "SELECT_CONTINUE_EDGE_RING"
#         select_continue_edges_box.scale_y = 1.5

#         #endregion


