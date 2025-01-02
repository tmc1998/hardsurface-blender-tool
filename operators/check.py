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

# --- CHECK ACTION LOGIC --- #
class OBJECT_OT_CHECK_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
    """Tool tip"""
    bl_idname = "object.check_action" # Naming object.add_cube so it will consistent with our class
    bl_label = "Check"
    bl_description = 'Custom tools for checking'

    action: EnumProperty(
        items=[
            ('CHECK_ALL', 'check all', 'check all'),
            ('CHECK_NGONS_FACE', 'check n-gons face', 'check n-gons face'),
            ('CHECK_NON_MANIFOLD', 'check non-manifold vertex/edge', 'check non-manifold vertex/edge'),
            ('CHECK_CONCAVE_FACE', 'check concave face', 'check concave face'),
            ('CHECK_ISOLATED_VERTEX', 'check isolated vertex', 'check isolated vertex'),
            ('CHECK_SILHOUETTE', 'check silhouette', 'check silhouette'),
        ]
    )

    def execute(self, context):
        if self.action == 'CHECK_ALL':
            self.check_all(context)
        elif self.action == 'CHECK_NGONS_FACE':
            self.check_ngons_face_function(context)
        elif self.action == 'CHECK_NON_MANIFOLD':
            self.check_non_manifold_function(context)
        elif self.action == 'CHECK_CONCAVE_FACE':
            self.check_concave_face_function(context)
        elif self.action == 'CHECK_ISOLATED_VERTEX':
            self.check_isolated_vertex_function(context)
        elif self.action == 'CHECK_SILHOUETTE':
            self.preview_silhouette_function(context)

        return {'FINISHED'}

    def check_all(self, context):
        selection = [obj for obj in bpy.context.selected_objects]
        if selection:
            err = []
            bpy.ops.object.select_all(action='DESELECT')
            for obj in selection:
                obj.select_set(True)
            err = list(set(err + self.check_ngons_face_function(context)))
            bpy.ops.object.mode_set(mode='OBJECT')

            bpy.ops.object.select_all(action='DESELECT')
            for obj in selection:
                obj.select_set(True)
            err = list(set(err + self.check_non_manifold_function(context)))
            bpy.ops.object.mode_set(mode='OBJECT')

            bpy.ops.object.select_all(action='DESELECT')
            for obj in selection:
                obj.select_set(True)
            err = list(set(err + self.check_concave_face_function(context)))
            bpy.ops.object.mode_set(mode='OBJECT')

            bpy.ops.object.select_all(action='DESELECT')
            for obj in selection:
                obj.select_set(True)
            err = list(set(err + self.check_isolated_vertex_function(context)))
            bpy.ops.object.mode_set(mode='OBJECT')

            # Select error mesh
            for obj in err:
                obj.select_set(True)
        else:
            my_utility.show_message(context, "ERROR", "Please select object to checking!")

    def check_ngons_face_function(self, context):
        selection = [obj for obj in bpy.context.selected_objects]
        if selection:
            err_obj = []
            # check n-gons face
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='FACE')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER', extend=True)

            # Get error mesh list
            for obj in selection:
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='FACE')
                bm = bmesh.from_edit_mesh(context.edit_object.data)
                selected_faces = [f for f in bm.faces if f.select]
                if len(selected_faces) > 0:
                    err_obj.append(obj)

            # Select error elements on mesh
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            if len(err_obj) > 0: 
                for obj in err_obj:
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='FACE')
                # Change button icon
                context.scene.check_ngons_face = False
            else:
                context.scene.check_ngons_face = True
            return err_obj
        else:
            my_utility.show_message(context, "ERROR", "Please select object to checking!")
            return None

    def check_non_manifold_function(self, context):
        selection = [obj for obj in bpy.context.selected_objects]
        if selection:
            err_obj = []
            # check non-manifold
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='VERT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_non_manifold(extend=True)

            # Get error mesh list
            for obj in selection:
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='VERT')
                bm = bmesh.from_edit_mesh(context.edit_object.data)
                selected_verts = [v for v in bm.verts if v.select]
                if len(selected_verts) > 0:
                    err_obj.append(obj)

            # Select error elements on mesh
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            if len(err_obj) > 0: 
                for obj in err_obj:
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='VERT')
                # Change button icon
                context.scene.check_non_manifold = False
            else:
                context.scene.check_non_manifold = True
            return err_obj
        else:
            my_utility.show_message(context, "ERROR", "Please select object to checking!")
            return None

    def check_concave_face_function(self, context):
        selection = [obj for obj in bpy.context.selected_objects]
        if selection:
            err_obj = []
            # check concave face
            tolerance = 0  # increase to something like .01 or .1 to ignore small concavities
            for obj in selection:
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode = 'EDIT') 
                bpy.ops.mesh.select_mode(type="FACE")
                bpy.ops.mesh.select_all(action = 'DESELECT')
                bpy.ops.object.mode_set(mode = 'OBJECT')

                me = bpy.context.active_object.data
                me.calc_loop_triangles()
                poly_i_to_tris = {}
                for tri in me.loop_triangles:
                    poly_i_to_tris.setdefault(tri.polygon_index, []).append(tri)

                for i, tris in poly_i_to_tris.items():
                    try:
                        t1, t2 = tris
                    except ValueError:
                        continue  # not a quad
                    dist = (t1.center - t2.center).length
                    tolerance *= dist  # makes tolerance relative
                    ray_len = dist/2  # making sure to not overshoot, but I don't think it would be possible
                    test1 = t1.center + t1.normal*ray_len
                    test2 = t2.center + t2.normal*ray_len
                    test_dist = (test1 - test2).length
                    if test_dist < dist - tolerance:
                        # concave
                        me.polygons[i].select = True

            # Get error mesh list
            for obj in selection:
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='FACE')
                bm = bmesh.from_edit_mesh(context.edit_object.data)
                selected_faces = [f for f in bm.faces if f.select]
                if len(selected_faces) > 0:
                    err_obj.append(obj)

            # Select error elements on mesh
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            if len(err_obj) > 0: 
                for obj in err_obj:
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='FACE')
                # Change button icon
                context.scene.check_concave_face = False
            else:
                context.scene.check_concave_face = True
            return err_obj
        else:
            my_utility.show_message(context, "ERROR", "Please select object to checking!")
            return None

    def check_isolated_vertex_function(self, context):
        selection = [obj for obj in bpy.context.selected_objects]
        if selection:
            err_obj = []
            # check isolated vertex
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='VERT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_loose(extend=True)

            # Get error mesh list
            for obj in selection:
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='VERT')
                bm = bmesh.from_edit_mesh(context.edit_object.data)
                selected_verts = [v for v in bm.verts if v.select]
                if len(selected_verts) > 0:
                    err_obj.append(obj)

            # Select error elements on mesh
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            if len(err_obj) > 0: 
                for obj in err_obj:
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='VERT')
                # Change button icon
                context.scene.check_isolated_vertex = False
            else:
                context.scene.check_isolated_vertex = True
            return err_obj
        else:
            my_utility.show_message(context, "ERROR", "Please select object to checking!")
            return None

    def preview_silhouette_function(self, context):
        
        light_types = ["STUDIO", "MATCAP", "FLAT"]
        bg_types = ["THEME", "WORLD", "VIEWPORT"]
        bg_black = [0.0, 0.0, 0.0]
        bg_default = [0.188, 0.188, 0.188]

        
        for area in bpy.context.screen.areas: 
            if area.type == 'VIEW_3D':
                for space in area.spaces: 
                    if space.type == 'VIEW_3D':
                        if my_variables.CHECK_SILHOUETTE == False:
                            # Light
                            space.shading.type = 'SOLID'
                            space.shading.light = light_types[2]
                            space.shading.color_type = 'SINGLE'
                            space.shading.single_color = bg_black
                            # Background
                            space.shading.background_type = bg_types[2]
                            space.shading.background_color = list(context.scene.viewport_background_color)
                            # Overlays
                            bpy.context.space_data.overlay.show_overlays = False

                            my_variables.CHECK_SILHOUETTE  = not my_variables.CHECK_SILHOUETTE
                        else:
                            # Light
                            space.shading.type = 'SOLID'
                            space.shading.light = light_types[0]
                            space.shading.color_type = 'MATERIAL'
                            space.shading.single_color = bg_black
                            # Background
                            space.shading.background_type = bg_types[0]
                            # Overlays
                            bpy.context.space_data.overlay.show_overlays = True

                            my_variables.CHECK_SILHOUETTE  = not my_variables.CHECK_SILHOUETTE 
