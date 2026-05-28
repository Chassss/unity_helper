import unity_helper, ctypes.wintypes, time
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



class TransparentViewport():
    """
    Makes the viewport completely transparent and click through-able but still allows you to interact with inner windows (no support for any of the built in tools, example dpg.show_style_editor)
    
    Args:
        ui (callable, optional): Function containing the ui within the viewport
        every_frame (callable, optional): Function containing code that gets ran on every dearpygui frame. Defaults to None.
        on_startup (callable, optional): Function that gets ran on viewport startup. Defaults to None.
        on_close (callable, optional): Function that runs on viewport close. Defaults to None.
        always_on_top (bool, optional): Should be topmost. Defaults to False.
        should_auto_refresh_windows (bool, optional): Checks every dearpygui frame for new windows that were created. Defaults to False.
        fps_limit (int, optional): Sets the framerate limit of the overlay. Defaults to None.
        overlay_name (str, optional): Window title. Defaults to 'Interactable Overlay'.
    """
    def __init__(self, ui=None, every_frame:callable=None, on_startup:callable=None, on_close:callable=None, always_on_top=False, should_auto_refresh_windows=False, fps_limit:int=None, overlay_name:str = 'Interactable Overlay'):
        self.overlay_name = overlay_name
        self.ui = ui
        self.overlay_hwnd = None
        self.always_on_top = always_on_top
        self.every_frame = every_frame
        self.on_startup = on_startup
        self.on_close = on_close
        self.in_any_window = False
        self.was_in_any_window = False
        self.should_auto_refresh_windows = should_auto_refresh_windows
        self.fps_limit = fps_limit
        

    def __set_transparent_window(self):
        class MARGINS(ctypes.Structure):
            _fields_ = [("cxLeftWidth", ctypes.c_int),
                        ("cxRightWidth", ctypes.c_int),
                        ("cyTopHeight", ctypes.c_int),
                        ("cyBottomHeight", ctypes.c_int)]

        margins = MARGINS(-1, -1, -1, -1)
        
        exstyle = ctypes.windll.user32.GetWindowLongW(self.overlay_hwnd, -20)
        exstyle |= 0x00080000 | 0x00000020
        ctypes.windll.user32.SetWindowLongW(self.overlay_hwnd, -20, exstyle)
        
        style = ctypes.windll.user32.GetWindowLongW(self.overlay_hwnd, -16)
        style |= 0x80000000
        ctypes.windll.user32.SetWindowLongW(self.overlay_hwnd, -16, style)

        ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(self.overlay_hwnd, margins)
        

    def start(self):
        """
        Starts up the overlay
        
        """
        dpg.create_context()
        dpg.create_viewport(title=self.overlay_name, y_pos=0, x_pos=0, decorated=False, always_on_top=self.always_on_top, clear_color=(0,0,0,0))
        dpg.setup_dearpygui()
        dpg.show_viewport()
        self.overlay_hwnd = ctypes.windll.user32.GetActiveWindow()
        self.__set_transparent_window()
        if self.on_startup:
            self.on_startup()
        if self.ui:
            self.ui()
        dpg.maximize_viewport()
        
        self.in_any_window = False

        GetCursorPos = ctypes.windll.user32.GetCursorPos
        GetCursorPos.argtypes = [ctypes.wintypes.LPPOINT]
        GetCursorPos.restype  = ctypes.wintypes.BOOL

        GetWindowLongW = ctypes.windll.user32.GetWindowLongW
        SetWindowLongW = ctypes.windll.user32.SetWindowLongW
        
        windows = dpg.get_windows()

        mouse_pos = ctypes.wintypes.POINT()

        last_time = time.perf_counter()

        if self.fps_limit:
            frame_time = 1 / self.fps_limit

        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            
            if self.fps_limit:
                current_time = time.perf_counter()

                delta_time = current_time - last_time

                if delta_time >= frame_time:
                    time.sleep(max(0, frame_time - delta_time))

            if self.every_frame:
                self.every_frame()

            if self.should_auto_refresh_windows:
                windows = dpg.get_windows()

            GetCursorPos(ctypes.byref(mouse_pos))
            self.in_any_window = False

            for i in windows:
                try:

                    if not dpg.is_item_visible(i):
                        continue

                    x0, y0 = dpg.get_item_pos(i)
                    width, height = dpg.get_item_rect_size(i)

                    inside = (dx := mouse_pos.x - x0) >= 0 and dx <= width and (dy := mouse_pos.y - y0) >= 0 and dy <= height

                    if inside:
                        self.in_any_window = True
                        break

                except:
                    pass


            if self.in_any_window != self.was_in_any_window: # Make it so that we only ever change the window properties when the users cursor moves in or out of the window rect

                style = GetWindowLongW(self.overlay_hwnd, -20)

                if self.in_any_window:
                    SetWindowLongW(self.overlay_hwnd, -20, style & ~0x20)
                else:
                    SetWindowLongW(self.overlay_hwnd, -20, style | 0x20)

                self.was_in_any_window = self.in_any_window # Update our variable so our first if statement will return True to then be run again
                
        
        if self.on_close:
            self.on_close()
        dpg.destroy_context()

window = TransparentViewport(gui, every_frame=tree_node_handler, on_startup=on_startup)
window.start()