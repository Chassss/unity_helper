"""
Public API for unity_helper.

Il2cpp:
    Main interface for interacting with IL2CPP.

structures:
    Contains useful structures such as Vec3, Vec2, Quaternion, etc.

objects:
    Provides high-level wrappers for Unity objects, including
    Component-based systems like Transform, Camera, and Scene, etc.

memory:
    Provides high-level wrappers around windows api to be able to access and manipulate memory.

constants:
    Shared constant values used across the project.
"""


from .main import Il2cpp
from . import structures
from . import mono
from . import bindings
from . import objects
from . import memory
from . import constants

__all__ = ["Il2cpp", "structures", "objects", "constants", "memory"]