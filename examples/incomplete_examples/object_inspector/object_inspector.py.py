import unity_helper, transparent_window, ctypes, time
import dearpygui.dearpygui as dpg

# Inspiration was from https://github.com/sinai-dev/UnityExplorer back in the early days of melonloader in 2021/2022


# This was meant to be a proof of concept so things like setting the dearpygui parent based off pid is completely broken
# Also the gui isnt optimized/good looking


# ===== WARNING =====
# This is a proof of concept/incomplete for a reason. Your game will more than likely crash "randomly".

# 1. Run game.
# 2. Run this script.

ref = unity_helper.Il2cpp()

tree_data = {}

time.sleep(5)

# def get_windowHWND(pid):
#     def callback(hwnd, b):
#         if ctypes.windll.user32.IsWindowVisible(hwnd):
#             pid_ = ctypes.c_ulong()
#             ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid_))

#             if pid_.value == pid:
#                 length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
#                 buff = ctypes.create_unicode_buffer(length + 1)
#                 ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
#                 if not buff.value == "Chasss's python mod loader":
#                     window_hwnd.append(hwnd)
#                     return True


#     window_hwnd = []
#     EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
#     ctypes.windll.user32.EnumWindows(EnumWindowsProc(callback), None)
#     return window_hwnd[0]

def refresh_objects():
    objects = ref._gameobject.find_objects_of_type()
    if len(objects) < 1:
        return
    
    for i in dpg.get_item_children('objects_holder', 1):
        dpg.delete_item(i)

    sorted_objects = {}

    for i in objects:
        sorted_objects[i.name] = i

    for i in sorted(sorted_objects):
        add_object(sorted_objects[i])


def tree_node_handler():
    for tree_id, data in list(tree_data.items()):

        if not dpg.get_value(tree_id):
            continue

        obj = data["obj"]
        inputs = data["inputs"]
        t = data["type"]
        try:
            if t in ("position", 'local_position', 'size', 'forward', 'up', 'right'):
                types = {
                    'position': obj.transform.position,
                    'local_position': obj.transform.localPosition,
                    'scale': obj.transform.localScale,
                    'forward': obj.transform.forward,
                    'up': obj.transform.up,
                    'right': obj.transform.right,
                }
                p = types[t]
                dpg.set_value(inputs["x"], p.x)
                dpg.set_value(inputs["y"], p.y)
                dpg.set_value(inputs["z"], p.z)

            elif t == "rotation":
                r = obj.transform.rotation
                dpg.set_value(inputs["x"], r.x)
                dpg.set_value(inputs["y"], r.y)
                dpg.set_value(inputs["z"], r.z)
                dpg.set_value(inputs["w"], r.w)
        except:
            pass


def labeled_input(label, obj, field):
    dpg.add_text(label)
    return dpg.add_input_float(width=150, step=0.0, step_fast=0.0, user_data=(label, obj, field), callback=input_callback, on_enter=True)


def input_callback(sender, app_data, user_data):
    axis, obj, field = user_data
    transform = obj.transform

    vec = getattr(transform, field)
    setattr(vec, axis, app_data)
    setattr(transform, field, vec)


def destroy_component(sender, app_data, comp):
    if comp.destroy():
        parent = dpg.get_item_parent(sender)
        dpg.delete_item(parent)

def toggle_component(sender, app_data, user_data):
    comp = user_data

    comp.enabled = app_data
    dpg.set_value(sender, comp.enabled)


def add_object(obj:unity_helper.objects.Object):
    name = obj.name
    with dpg.collapsing_header(label=name, parent='objects_holder'):
        with dpg.tree_node(label='Tag'):
            dpg.add_text(default_value=str(obj.tag))

        with dpg.tree_node(label='Position') as pos_tree:
            with dpg.group(horizontal=True):
                pos_inputs = {
                    "x": labeled_input('x', obj, 'position'),
                    "y": labeled_input('y', obj, 'position'),
                    "z": labeled_input('z', obj, 'position'),
                }

            tree_data[pos_tree] = {
                "type": "position",
                "inputs": pos_inputs,
                "obj": obj
            }


        with dpg.tree_node(label='Local Position') as localpos_tree:
            with dpg.group(horizontal=True):
                localpos_inputs = {
                    "x": labeled_input('x', obj, 'localPosition'),
                    "y": labeled_input('y', obj, 'localPosition'),
                    "z": labeled_input('z', obj, 'localPosition'),
                }

            tree_data[localpos_tree] = {
                "type": "local_position",
                "inputs": localpos_inputs,
                "obj": obj
            }


        with dpg.tree_node(label='Forward') as forward_tree:
            with dpg.group(horizontal=True):
                forward_inputs = {
                    "x": labeled_input('x', obj, 'forward'),
                    "y": labeled_input('y', obj, 'forward'),
                    "z": labeled_input('z', obj, 'forward'),
                }

            tree_data[forward_tree] = {
                "type": "forward",
                "inputs": forward_inputs,
                "obj": obj
            }

        with dpg.tree_node(label='up') as up_tree:
            with dpg.group(horizontal=True):
                up_inputs = {
                    "x": labeled_input('x', obj, 'up'),
                    "y": labeled_input('y', obj, 'up'),
                    "z": labeled_input('z', obj, 'up'),
                }

            tree_data[up_tree] = {
                "type": "up",
                "inputs": up_inputs,
                "obj": obj
            }


        with dpg.tree_node(label='Forward') as right_tree:
            with dpg.group(horizontal=True):
                right_inputs = {
                    "x": labeled_input('x', obj, 'right'),
                    "y": labeled_input('y', obj, 'right'),
                    "z": labeled_input('z', obj, 'right'),
                }

            tree_data[right_tree] = {
                "type": "right",
                "inputs": right_inputs,
                "obj": obj
            }


        with dpg.tree_node(label='Rotation') as rot_tree:
            with dpg.group(horizontal=True):
                rot_inputs = {
                    "x": labeled_input('x', obj, 'rotation'),
                    "y": labeled_input('y', obj, 'rotation'),
                    "z": labeled_input('z', obj, 'rotation'),
                    "w": labeled_input('w', obj, 'rotation')
                }

            tree_data[rot_tree] = {
                "type": "rotation",
                "inputs": rot_inputs,
                "obj": obj
            }



        with dpg.tree_node(label='Size') as size_tree:
            with dpg.group(horizontal=True):
                size_inputs = {
                    "x": labeled_input('x', obj, 'localScale'),
                    "y": labeled_input('y', obj, 'localScale'),
                    "z": labeled_input('z', obj, 'localScale'),
                }

            tree_data[size_tree] = {
                "type": "size",
                "inputs": size_inputs,
                "obj": obj
            }

        # with dpg.tree_node(label='Enabled'): # We dont need to check if its enabled every frame or not
        #     # Make the checkbox automatically tick itself if its enabled or not
        #     dpg.add_checkbox(default_value=ref._UnityEngine_Behaviour__get_enabled(obj.ptr, ref._methodInfoData['_UnityEngine_Behaviour__get_enabled']), label='Enabled')


        with dpg.tree_node(label='Components'): # We will need to be updating the list when this tree is open            
            components = obj.GetComponents()
            if not components:
                return
            
            for i in components:
                with dpg.group(horizontal=True):
                    btn = dpg.add_button(label="X", width=24, height=24, user_data=i, callback=destroy_component)
                    dpg.bind_item_theme(btn, 'destroy_theme')
                    # dpg.add_checkbox(default_value=i.enabled, callback=lambda sender, value, data, comp=comp: toggle_component(sender, comp, value))
                    dpg.add_checkbox(default_value=i.enabled, user_data=i, callback=toggle_component)
                    dpg.add_text(i.name)

        
        dpg.add_checkbox(label='Enabled', default_value=obj.activeSelf, callback=lambda sender, value: obj.SetActive(value))

        with dpg.group(horizontal=True):
            dpg.add_button(label='Instantiate', callback=lambda: obj.Instantiate())
            dpg.add_button(label='Destroy', callback=lambda sender: (dpg.delete_item(dpg.get_item_parent(dpg.get_item_parent(sender))), obj.destroy()))


def on_startup():
    # ctypes.windll.user32.SetParent(window.overlay_hwnd, get_windowHWND(ctypes.windll.kernel32.GetCurrentProcess()))
    ...

def gui():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvTreeNode):
            dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 60, 65))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (75, 75, 80))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (90, 90, 95))
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 6)
        
        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, y=8)


    with dpg.theme(tag='destroy_theme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 50, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 80, 80, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (150, 30, 30, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)


    with dpg.window(label='Object viewer', no_title_bar=True, no_resize=False, width=600, height=765, horizontal_scrollbar=True):
        dpg.add_button(label='Refresh objects', callback=refresh_objects)
        dpg.add_child_window(tag='objects_holder', border=False, horizontal_scrollbar=True)

    dpg.bind_theme(global_theme)




window = transparent_window.TransparentViewport(gui, every_frame=tree_node_handler, on_startup=on_startup)
window.start()