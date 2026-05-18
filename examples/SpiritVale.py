import unity_helper, cyminhook, ctypes.wintypes
from typing import Callable, TypeVar, Protocol, Any, ParamSpec

# Tested on SpiritVale playtest but should work on the full release too


# 1. Run game
# 2. Join a server and pick your character
# 3. Move your cursor where you want to teleport to
# 4. Run this script
# 5 (optional, read the bottom of the file). Press right shift to teleport around 


EXIT_HOOKS_HOTKEY = 35 # end


ref = unity_helper.Il2cpp(warn_on_missing=False)

Physics = unity_helper.objects.Physics()
NetworkObject = ref.get_class_from_name('FishNet.Runtime.dll', 'FishNet.Object.NetworkObject')
HasAuthority = NetworkObject.method.get_HasAuthority


P = ParamSpec("P")
R = TypeVar("R")
__ACTIVE_HOOKS = []
WM_KEYDOWN = 0x0100
WM_MBUTTONDOWN = 0x0207

class HookedFunction(Protocol[P, R]):
    original: Callable[P, R]
    close: None
    def __call__(self, *args, **kwargs) -> Any: ...

# Decorator helper for using cyminhook
def hook(sig, target) -> Callable[[Callable[P, R]], HookedFunction[P, R]]:
    def decorator(func: Callable[P, R]) -> HookedFunction[P, R]:
        if not target or type(target) == str:
            print('\033[31m' + f"Invalid target for func: {func} hook")
            return None
        h = cyminhook.MinHook(signature=sig, target=target, detour=func)
        h.enable()
        __ACTIVE_HOOKS.append(h)

        func.original = h.original
        func.close = h.close

        return func
    return decorator

# Struct used for DispatchMessageA
class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", ctypes.wintypes.HWND),
        ("message", ctypes.wintypes.UINT),
        ("wParam", ctypes.wintypes.WPARAM),
        ("lParam", ctypes.wintypes.LPARAM),
        ("time", ctypes.wintypes.DWORD),
        ("pt_x", ctypes.c_long),
        ("pt_y", ctypes.c_long),
    ]

# Handle all keyboard inputs sent to the game
def key_handler(key, modifiers=None):
    if key == EXIT_HOOKS_HOTKEY:
        print('Closing hooks and exiting')
        for i in __ACTIVE_HOOKS:
            i.close()


def tp():
    cam = ref.get_mainCamera()
    if not cam:
        return
    ray = cam.ScreenPointToRay()

    if not ray:
        return
    
    result = Physics.RaycastRay(ray, 9999, -1) # Create our ray so we can raycast

    if result: # Result returns non False if a hit was made
        for i in NetworkObject.find_objects_of_type(): # Get all network objects 
            NetworkObject.instance = i.ptr
            if HasAuthority(): # Check if we are the owner of the network object

                comp = unity_helper.objects.Component(i.ptr)
                player = comp.gameObject
                
                NavMeshAgent = None # Define this for when we try and access it later

                for i in player.GetComponents():
                    if i.name == 'NavMeshAgent':
                        NavMeshAgent = i
                        break
                    
                if not NavMeshAgent:
                    break

                NavMeshAgent.enabled = False # Disable the mesh allowing us to teleport around while its disabled (we cant move with it disabled)

                player.transform.position = result.point # Set our position to where our raycast hiit
                NavMeshAgent.enabled = True # Re-enable the mesh so we can freely move around (if the spot we teleported to is a valid spot)
                break


# Comment this out if you wish use a hotkey for teleporting around, default is right shift
tp()



# Uncomment down below if you wish to use a hotkey for teleporting around, default is right shift

# @hook(ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.POINTER(MSG)), ctypes.windll.user32.DispatchMessageW)
# def HookedDispatchMessageW(lpMsg): # Useful for program specific hotkeys although you can still use unity's GetKeyDown and GetKey but then you'd have to have your own for loop which will most likely be more expensive than this
#     normal = HookedDispatchMessageW.original(lpMsg)
#     if lpMsg[0].message == WM_KEYDOWN:
#         key_handler(lpMsg[0].wParam, lpMsg[0].lParam)
#     elif lpMsg[0].message == WM_MBUTTONDOWN:
#         tp()
#     return normal