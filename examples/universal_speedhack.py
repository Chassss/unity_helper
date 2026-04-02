# Note: for python versions before 3.14 you may need to have a while True: time.sleep(1e6) at the end of the script so the script doesnt auto exit (i had issues with this on python 3.11 but never had that issue on 3.14)
# If your on python 3.14 you're gonna need to compile cyminhook yourself as its unmaintained as of 4/1/2026, https://github.com/segevfiner/cyminhook

import cyminhook, ctypes.wintypes, unity_helper, time
from typing import Callable, TypeVar, Protocol, Any, ParamSpec
from pymousekey import VK_KEYS

time.sleep(1) # Not needed if your not auto loading scripts into the game instance via a dll on startup (this stops us from crashing because you have to wait for unity to be properly initialized)

P = ParamSpec("P")
R = TypeVar("R")

__ACTIVE_HOOKS = []

WM_KEYDOWN = 0x0100

ref = unity_helper.Il2cpp()
MULT = 2

# Helper for a decorator
class HookedFunction(Protocol[P, R]):
    original: Callable[P, R]
    close: None
    def __call__(self, *args, **kwargs) -> Any: ...

# Decorator for cyminhook
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

def key_handler(key, modifiers=None):
    if key == VK_KEYS['end']:
        print('Closing hooks and exiting')
        for i in __ACTIVE_HOOKS:
            i.close()


# Move is a relative move not an absolute move
@hook(ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, unity_helper.structures.Vec3, ctypes.c_void_p), ref.find_method('UnityEngine.PhysicsModule.dll', 'UnityEngine', 'CharacterController', 'Move').address)
def HookedMove(this, pos, method):
    pos.x *= MULT
    # pos.y = pos.y * mult if pos.y > 0.0 else pos.y # Gives us superjump if we want
    pos.z *= MULT
    return HookedMove.original(this, pos, method)


# For keybinds
@hook(ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.POINTER(MSG)), ctypes.windll.user32.DispatchMessageA)
def HookedDispatchMessageA(lpMsg):
    normal = HookedDispatchMessageA.original(lpMsg)
    if lpMsg[0].message == WM_KEYDOWN:
        key_handler(lpMsg[0].wParam, lpMsg[0].lParam)
    return normal