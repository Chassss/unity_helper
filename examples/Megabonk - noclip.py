# Note: for python versions before 3.14 you may need to have a while True: time.sleep(1e6) at the end of the script so the script doesnt auto exit (i had issues with this on python 3.11 but never had that issue on 3.14)
# If your on python 3.14 you're gonna need to compile cyminhook yourself as its unmaintained as of 4/28/2026, https://github.com/segevfiner/cyminhook

import cyminhook, ctypes.wintypes, unity_helper
from typing import Callable, TypeVar, Protocol, Any, ParamSpec
from pymousekey import VK_KEYS

# Define constants and variables to be used later
P = ParamSpec("P")
R = TypeVar("R")
__ACTIVE_HOOKS = []
WM_KEYDOWN = 0x0100

toggled = False

ref = unity_helper.Il2cpp()
GetKey = ref.find_method('UnityEngine.InputLegacyModule.dll', 'UnityEngine', 'Input', 'GetKey') # Built in unity function
PlayerMovement = ref.get_class_from_name('Assembly-CSharp.dll', '', 'PlayerMovement') # Game specific
NoclipMovement = PlayerMovement.find_method('NoclipMovement') # Game specific

# Helper for a decorator
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
    if key == VK_KEYS['end']:
        print('Closing hooks and exiting')
        for i in __ACTIVE_HOOKS:
            i.close()
    elif key == VK_KEYS['f']:
        global toggled
        
        player = ref.find_object('Player')

        if not player:
            return
        
        if toggled: # If we want to disable noclip theres no reason to run the code below so thats what this if is for
            for i in player.GetComponents():
                if i.name == 'CapsuleCollider':
                    i.enabled = True
            
            toggled = False
            return
        
        toggled = True

        for i in player.GetComponents():
            if i.name == 'CapsuleCollider':
                i.enabled = False


@hook(ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p), PlayerMovement.find_method('MovementTick').address)
def HookedPlayerMovement(this, method):
    
    if toggled:
        PlayerMovement.instance = this # PlayerMovement isnt a static class so we need to set its instance before calling its methods
        return NoclipMovement()
    
    return HookedPlayerMovement.original(this, method)


@hook(ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.POINTER(MSG)), ctypes.windll.user32.DispatchMessageA)
def HookedDispatchMessageA(lpMsg): # Useful for program specific hotkeys although you can still use unity's GetKeyDown and GetKey but then you'd have to have your own for loop which will most likely be more expensive than this
    normal = HookedDispatchMessageA.original(lpMsg)
    if lpMsg[0].message == WM_KEYDOWN:
        key_handler(lpMsg[0].wParam, lpMsg[0].lParam)
    return normal