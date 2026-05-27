# Note: for python versions before 3.14 you may need to have a while True: time.sleep(1e6) at the end of the script so the script doesnt auto exit (i had issues with this on python 3.11 but never had that issue on 3.14)
# If your on python 3.14 you're gonna need to compile cyminhook yourself as its unmaintained as of 4/1/2026, https://github.com/segevfiner/cyminhook

import cyminhook, ctypes.wintypes, unity_helper
from typing import Callable, TypeVar, Protocol, Any, ParamSpec


# 1. Run game
# 2. Run this script
# 3. Join a server and pick your character
# 4. Press right shift to toggle noclip


# Define constants and variables to be used later
P = ParamSpec("P")
R = TypeVar("R")
__ACTIVE_HOOKS = []
WM_KEYDOWN = 0x0100
VERTICAL_SPEED = 0.25
SPEED = 0.5

CLOSE_HOTKEY = 35 # end
NOCLIP_HOTKEY = 16 # right shift

toggled = False
player = None
cam = None

ref = unity_helper.Il2cpp(warn_on_missing=False)

MoveComponent = ref.get_class_from_name('Assembly-CSharp.dll', 'MoveComponent')
MoveTo = MoveComponent.method.MoveTo
Move = MoveComponent.method.Move
Warp = MoveComponent.method.Warp

CameraController = ref.get_class_from_name('Assembly-CSharp.dll', 'CameraController')
tiltMin = CameraController.field.tiltMin
tiltMax = CameraController.field.tiltMax
zoomMax = CameraController.field.zoomMax

GetKey = ref.find_method('UnityEngine.InputLegacyModule.dll', 'UnityEngine.Input', 'GetKey')

NetworkObject = ref.get_class_from_name('FishNet.Runtime.dll', 'FishNet.Object.NetworkObject')
HasAuthority = NetworkObject.method.get_HasAuthority

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
    if key == CLOSE_HOTKEY:
        print('Closing hooks and exiting')
        for i in __ACTIVE_HOOKS:
            i.close()
    elif key == NOCLIP_HOTKEY:
        global toggled, player, cam
        
        # Re-initialize these every time we use our hotkey since these could possibly change from world to word/menu to menu and its not expensive
        player = None
        cam = None
        player = get_player()
        cam = ref.get_mainCamera()

        if not player or not cam:
            toggled = False
            return
        
        toggled = not toggled
        NavMeshAgent = None
        CameraController.instance = cam.transform.parent.parent.gameObject.GetComponent(CameraController.object).instance # Our CameraController instance is 2 objects away from our Main Camera object
        
        # Optional
        if zoomMax.value != 999.0: # Allow us to zoom out camera out as far as we wish
            zoomMax.value = 999.0


        if toggled and CameraController.instance:
            tiltMin.value = -89.0 # Allow us to look almost all the way up (but not straight up because then we dont move upwards)
            tiltMax.value = 89.0 # Allow us to look almost all the way up (but not straight up because then we dont move downwards)
        elif not toggled and CameraController.instance:
            tiltMin.value = 10.0 # Reset to default
            tiltMax.value = 80.0 # Reset to default


        for i in player.GetComponents():
            if i.name == 'NavMeshAgent':
                NavMeshAgent = i
                break
        
        NavMeshAgent.enabled = not toggled


def get_player():
    for i in NetworkObject.find_objects_of_type():
        NetworkObject.instance = i.instance
        if HasAuthority():
            comp = unity_helper.objects.Component(i.instance)
            player = comp.gameObject
            
    return player



# This game is a bit different from the rest, our Move function Vec3 isnt the coordinates of where we move to but rather our .forward Vec3
@hook(ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, unity_helper.structures.Vec3, ctypes.c_void_p), Move.address)
def HookedMove(this, position, method):
    global toggled

    if toggled and player:
        pos = player.transform.localPosition # You can use both position and localPosition but in this instance im using localPosition
        forward = cam.transform.forward
        right = cam.transform.right

        isKeyDown_w =  GetKey(ctypes.c_int(0x77))
        isKeyDown_a =  GetKey(ctypes.c_int(0x61))
        isKeyDown_s =  GetKey(ctypes.c_int(0x73))
        isKeyDown_d =  GetKey(ctypes.c_int(0x64))

        if isKeyDown_w: # Calculate forward speed based off of where your looking
            pos.x += forward.x * SPEED
            pos.y += forward.y * SPEED # Optional, comment out if you dont want your look angles to effect y axis
            pos.z += forward.z * SPEED

        if isKeyDown_s: # Calculate backwards speed based off of where your looking
            pos.x -= forward.x * SPEED
            pos.y -= forward.y * SPEED # Optional, comment out if you dont want your look angles to effect y axis
            pos.z -= forward.z * SPEED

        # Calculate right speed based off of where your looking
        if isKeyDown_d:
            pos.x += right.x * SPEED
            pos.z += right.z * SPEED

        # Calculate left speed based off of where your looking
        if isKeyDown_a:
            pos.x -= right.x * SPEED
            pos.z -= right.z * SPEED


        player.transform.localPosition = pos


    return HookedMove.original(this, position, method)


@hook(ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.POINTER(MSG)), ctypes.windll.user32.DispatchMessageW)
def HookedDispatchMessageW(lpMsg): # Useful for program specific hotkeys although you can still use unity's GetKeyDown and GetKey but then you'd have to have your own for loop which will most likely be more expensive than this
    normal = HookedDispatchMessageW.original(lpMsg)
    if lpMsg[0].message == WM_KEYDOWN:
        key_handler(lpMsg[0].wParam, lpMsg[0].lParam)
    return normal
