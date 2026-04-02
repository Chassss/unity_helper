# Note: for python versions before 3.14 you may need to have a while True: time.sleep(1e6) at the end of the script so the script doesnt auto exit (i had issues with this on python 3.11 but never had that issue on 3.14)
# If your on python 3.14 you're gonna need to compile cyminhook yourself as its unmaintained as of 4/1/2026, https://github.com/segevfiner/cyminhook


# This was tested on Electrician Simulator

import cyminhook, ctypes.wintypes, unity_helper, time
from typing import Callable, TypeVar, Protocol, Any, ParamSpec
from pymousekey import VK_KEYS


time.sleep(1) # Not needed if your not auto loading scripts into the game instance via a dll on startup (this stops us from crashing because you have to wait for unity to be properly initialized)


# Define constants and variables to be used later
P = ParamSpec("P")
R = TypeVar("R")
__ACTIVE_HOOKS = []
WM_KEYDOWN = 0x0100
VERTICAL_SPEED = 0.25
SPEED = 1

toggled = False
player = None
cam = None

ref = unity_helper.Il2cpp()
GetKey = ref.find_method('UnityEngine.InputLegacyModule.dll', 'UnityEngine', 'Input', 'GetKey') # Built in unity function
CharacterController = ref.get_class_from_name('UnityEngine.PhysicsModule.dll', 'UnityEngine', 'CharacterController') # Built in unity function
FirstPersonController = ref.get_class_from_name('Assembly-CSharp.dll', 'Player.Movement', 'FirstPersonController') # Game specific so you'll need to find out how your game does this
previouslyGrounded = FirstPersonController.find_field('_previouslyGrounded') # Game specific

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
        global toggled, player, cam
        
        player = ref.find_object_with_tag('Player')

        if not player: # If we dont find a valid player then we shouldnt toggle fly on
            return

        for i in player.GetComponents(): # Loop through components to set our gravity so we dont end up smashing into the floor upon disabling noclip
            if i.name == 'FirstPersonController':
                FirstPersonController.instance = i.ptr
                break
        
        if toggled: # If we want to disable noclip theres no reason to run the code below so thats what this if is for
            previouslyGrounded.value = True # This stops me from gaining insane amounts of y velocity while fly is toggled, stopping me from smashing into the floor when toggling off (may be different for other games)
            toggled = False
            player = cam = None
            return
        
        cam = ref.get_mainCamera()

        if not cam: # If we dont find a valid camera then we shouldnt toggle fly on
            return
        
        toggled = True


@hook(ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, unity_helper.structures.Vec3, ctypes.c_void_p), CharacterController.find_method('Move').address)
def HookedMove(this, pos, method):
    if toggled:
        pos = player.transform.localPosition # You can use both position and localPosition but in this instance im using localPosition
        forward = cam.transform.forward
        right = cam.transform.right

        isKeyDown_w =  GetKey(ctypes.c_int(0x77))
        isKeyDown_a =  GetKey(ctypes.c_int(0x61))
        isKeyDown_s =  GetKey(ctypes.c_int(0x73))
        isKeyDown_d =  GetKey(ctypes.c_int(0x64))

        isKeyDown_spacebar =  GetKey(ctypes.c_int(0x20))
        isKeyDown_leftShift =  GetKey(ctypes.c_int(0x132))

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

        
        if isKeyDown_spacebar:
            pos.y += VERTICAL_SPEED

        elif isKeyDown_leftShift:
            pos.y -= VERTICAL_SPEED

        player.transform.localPosition = pos # We must set our position from within this function ourselves or else we have collision and we cant disable colliders on our character in the game i tested in because it disables wasd then
        # Depending on the game you can use the normal HookedMove.original(this, pos, method) and just disable collision to achive noclip 
        return None
    
    return HookedMove.original(this, pos, method)


@hook(ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.POINTER(MSG)), ctypes.windll.user32.DispatchMessageA)
def HookedDispatchMessageA(lpMsg): # Useful for program specific hotkeys although you can still use unity's GetKeyDown and GetKey but then you'd have to have your own for loop which will most likely be more expensive than this
    normal = HookedDispatchMessageA.original(lpMsg)
    if lpMsg[0].message == WM_KEYDOWN:
        key_handler(lpMsg[0].wParam, lpMsg[0].lParam)
    return normal