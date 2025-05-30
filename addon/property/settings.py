import bpy

class TMC_Settings(bpy.types.PropertyGroup):

    font_size: bpy.props.IntProperty(
        name = 'Font Size', description = 'Size of the font',
        min = 10, max = 32, default = 16)

def draw_settings(prefs, layout):
    layout.label(text='General Settings', icon='TOOL_SETTINGS')

    # Tools
    box = layout.box()

    row = box.row()
    row.label(text='Font Size')
    row.prop(prefs.settings, 'font_size', text='')