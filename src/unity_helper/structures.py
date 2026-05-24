"""
Defines low-level data structures used for game and engine interaction.

"""

import ctypes as _ctypes

class _UnpackableStructure(_ctypes.Structure):
    def __iter__(self):
        for field_name, _ in self._fields_:
            yield getattr(self, field_name)


class Vec2(_UnpackableStructure):
    _fields_ = [
        ("x", _ctypes.c_float),
        ("y", _ctypes.c_float),
    ]

class Vec3(_UnpackableStructure):
    _fields_ = [
        ("x", _ctypes.c_float),
        ("y", _ctypes.c_float),
        ("z", _ctypes.c_float)
    ]

class Vec4(_UnpackableStructure):
    _fields_ = [
        ("x", _ctypes.c_float),
        ("y", _ctypes.c_float),
        ("z", _ctypes.c_float),
        ("w", _ctypes.c_float)
    ]

class Quaternion(_UnpackableStructure):
    _fields_ = [
        ("x", _ctypes.c_float),
        ("y", _ctypes.c_float),
        ("z", _ctypes.c_float),
        ("w", _ctypes.c_float)
    ]

class Color(_UnpackableStructure):
    _fields_ = [
        ("r", _ctypes.c_float),
        ("g", _ctypes.c_float),
        ("b", _ctypes.c_float),
        ("a", _ctypes.c_float)
    ]

class Rect(_UnpackableStructure):
    _fields_ = [
        ("x", _ctypes.c_float),
        ("y", _ctypes.c_float),
        ("width", _ctypes.c_float),
        ("height", _ctypes.c_float)
    ]

class Matrix4x4(_UnpackableStructure):
    _fields_ = [("m00", _ctypes.c_float), ("m01", _ctypes.c_float), ("m02", _ctypes.c_float), ("m03", _ctypes.c_float),
                ("m10", _ctypes.c_float), ("m11", _ctypes.c_float), ("m12", _ctypes.c_float), ("m13", _ctypes.c_float),
                ("m20", _ctypes.c_float), ("m21", _ctypes.c_float), ("m22", _ctypes.c_float), ("m23", _ctypes.c_float),
                ("m30", _ctypes.c_float), ("m31", _ctypes.c_float), ("m32", _ctypes.c_float), ("m33", _ctypes.c_float)]
    
class Il2CppArray(_ctypes.Structure):
    _fields_ = [
        ("klass", _ctypes.c_void_p),
        ("monitor", _ctypes.c_void_p),
        ("bounds", _ctypes.c_void_p),
        ("max_length", _ctypes.c_int),
    ]

class Il2CppString(_ctypes.Structure):
    _fields_ = [
        ("klass", _ctypes.c_void_p),
        ("monitor", _ctypes.c_void_p),
        ("length", _ctypes.c_int),
        ("_padding", _ctypes.c_int),
    ]

class Il2CppImage(_ctypes.Structure):
    _pack_ = _ctypes.sizeof(_ctypes.c_void_p)
    pass


class Il2CppAssembly(_ctypes.Structure):
    _pack_ = _ctypes.sizeof(_ctypes.c_void_p)
    pass

class Il2CppAssemblyName(_ctypes.Structure):
    _pack_ = _ctypes.sizeof(_ctypes.c_void_p)
    _fields_ = [
        ("name", _ctypes.c_char_p),
        ("culture", _ctypes.c_char_p),
        ("hash_value", _ctypes.c_char_p),
        ("public_key", _ctypes.c_char_p),
        ("hash_alg", _ctypes.c_uint32),
        ("hash_len", _ctypes.c_int32),
        ("flags", _ctypes.c_uint32),
        ("major", _ctypes.c_int32),
        ("minor", _ctypes.c_int32),
        ("build", _ctypes.c_int32),
        ("revision", _ctypes.c_int32),
        ("public_key_token", _ctypes.c_uint8 * 8)
    ]

Il2CppImage._fields_ = [
    ("name", _ctypes.c_char_p),
    ("nameNoExt", _ctypes.c_char_p),
    ("assembly", _ctypes.POINTER(Il2CppAssembly)),
    ("typeStart", _ctypes.c_int32),
    ("typeCount", _ctypes.c_uint32),
    ("exportedTypeStart", _ctypes.c_int32),
    ("exportedTypeCount", _ctypes.c_uint32),
    ("customAttributeStart", _ctypes.c_int32),
    ("customAttributeCount", _ctypes.c_uint32),
    ("entryPointIndex", _ctypes.c_int32),
    ("nameToClassHashTable", _ctypes.c_void_p),
    ("token", _ctypes.c_uint32),
    ("dynamic", _ctypes.c_uint8),
]

Il2CppAssembly._fields_ = [
    ("image", _ctypes.POINTER(Il2CppImage)),
    ("token", _ctypes.c_uint32),
    ("referencedAssemblyStart", _ctypes.c_int32),
    ("referencedAssemblyCount", _ctypes.c_int32),
    ("aname", Il2CppAssemblyName)
]

class Bounds(_UnpackableStructure):
    _fields_ = [
        ("center", Vec3),
        ("size", Vec3)
    ]

class RaycastHit(_UnpackableStructure):
    _fields_ = [
        ("point", Vec3),
        ("normal", Vec3),
        ("faceID", _ctypes.c_uint),
        ("distance", _ctypes.c_float),
        ("uv", Vec2),
        ("collider", _ctypes.c_void_p)
    ]

class Ray(_UnpackableStructure):
    _fields_ = [
        ("m_Direction", Vec3),
        ("m_Origin", Vec3)
    ]

class Scene(_ctypes.Structure):
    _fields_ = [
        ("m_Handle", _ctypes.c_int)
    ]

class Plane(_UnpackableStructure):
    _fields_ = [
        ("normal", Vec3),
        ("distance", _ctypes.c_float)
    ]

class Keyframe(_UnpackableStructure):
    _fields_ = [
        ("time", _ctypes.c_float),
        ("value", _ctypes.c_float),
        ("inTangent", _ctypes.c_float),
        ("outTangent", _ctypes.c_float),
        ("weightedMode", _ctypes.c_int),
        ("inWeight", _ctypes.c_float),
        ("outWeight", _ctypes.c_float),
    ]