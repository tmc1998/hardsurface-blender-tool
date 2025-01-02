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

# --- VERTEXGROUP ACTION LOGIC --- #
class OBJECT_OT_SELECT_ACTION(bpy.types.Operator):# Operator class should have _OT_ in it
    """Tool tip"""
    bl_idname = "object.select_action" # Naming object.add_cube so it will consistent with our class
    bl_label = "Selection"
    bl_description = 'Custom tools for selection'

    action: EnumProperty(
        items=[
			('SELECT_CONTINUE_EDGE_LOOP', 'select continue edge loop', 'select continue edge loop'),
			('SELECT_CONTINUE_EDGE_RING', 'select continue edge ring', 'select continue edge ring')
        ]
    )

    def execute(self, context):
        if self.action == 'SELECT_CONTINUE_EDGE_LOOP':
            self.select_continue_edge_loop_function(context)
        elif self.action == 'SELECT_CONTINUE_EDGE_RING':
            self.select_continue_edge_ring_function(context)

        return {'FINISHED'}

    def select_continue_edge_ring_function(self, context):
        current_object = bmesh.from_edit_mesh(bpy.context.active_object.data)
        current_edges = [e for e in current_object.edges if e.select]
        current_vertices = [v for v in current_object.verts if v.select]
        final_edges = []
        if len(current_edges) == len(current_vertices):
            bpy.ops.mesh.shortest_path_select(edge_mode='SELECT', use_face_step=True)
            bpy.ops.mesh.loop_multi_select(ring=False)
        else:
            for e in current_edges:
                if e not in final_edges:
                    bpy.ops.mesh.select_all(action = 'DESELECT')
                    e.select = True
                    bpy.ops.mesh.loop_multi_select(ring=True)
                    edge_ring = [e for e in current_object.edges if e.select]
                    bpy.ops.mesh.select_all(action = 'DESELECT')
                    e.select = True
                    bpy.ops.mesh.loop_multi_select(ring=False)
                    edge_loop = [e for e in current_object.edges if e.select]
                    try:
                        end_ring_edge = list(set(edge_ring) & set(current_edges) - set([e]) - set(edge_loop))[0]
                    except:
                        continue
                    # Find all edge from shortest path
                    bpy.ops.mesh.select_all(action = 'DESELECT')
                    end_ring_edge.select = True
                    e.select = True
                    bpy.ops.mesh.shortest_path_select(edge_mode='SELECT', use_face_step=True)
                    current_path_edges = [e for e in current_object.edges if e.select]
                    final_edges += current_path_edges
            bpy.ops.mesh.select_all(action = 'DESELECT')
            for e in final_edges:
                e.select = True

    def select_continue_edge_loop_function(self, context):
        current_object = bmesh.from_edit_mesh(bpy.context.active_object.data)
        current_edges = [e for e in current_object.edges if e.select]
        final_edges = []
        for e in current_edges:
            if e not in final_edges:
                # Find des edge from begin edge
                bpy.ops.mesh.select_all(action = 'DESELECT')
                e.select = True
                bpy.ops.mesh.loop_multi_select(ring=False)
                edge_loop = [e for e in current_object.edges if e.select]
                try:
                    end_loop_edge = list(set(edge_loop) & set(current_edges) - set([e]))[0]
                except:
                    continue
                
                # Find all edge from shortest path
                bpy.ops.mesh.select_all(action = 'DESELECT')
                end_loop_edge.select = True
                e.select = True
                bpy.ops.mesh.shortest_path_select(edge_mode='SELECT')
                current_path_edges = [e for e in current_object.edges if e.select]
                final_edges += current_path_edges
        
        bpy.ops.mesh.select_all(action = 'DESELECT')
        for e in final_edges:
            e.select = True