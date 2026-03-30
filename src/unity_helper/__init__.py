"""
Public API for unity_helper.

Il2cpp:
    Main interface for interacting with IL2CPP.

structures:
    Contains useful structures such as Vec3, Vec2, Quaternion, etc.

objects:
    Provides high-level wrappers for Unity objects, including
    Component-based systems like Transform, Camera, and Scene, etc.
"""


from .main import Il2cpp
from . import structures
from . import mono
from . import bindings
from . import objects

__all__ = ["Il2cpp", "structures", "objects"]