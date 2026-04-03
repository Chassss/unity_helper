"""
Defines low-level data structures used for game and engine interaction.

"""

import ctypes

class Vec2(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
    ]

class Vec3(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float)
    ]

class Vec4(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
        ("w", ctypes.c_float)
    ]


class Quaternion(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
        ("w", ctypes.c_float)
    ]

class Color(ctypes.Structure):
    _fields_ = [
        ("r", ctypes.c_float),
        ("g", ctypes.c_float),
        ("b", ctypes.c_float),
        ("a", ctypes.c_float)
    ]

class Rect(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("width", ctypes.c_float),
        ("height", ctypes.c_float)
    ]

class Matrix4x4(ctypes.Structure):
    _fields_ = [("m00", ctypes.c_float), ("m01", ctypes.c_float), ("m02", ctypes.c_float), ("m03", ctypes.c_float),
                ("m10", ctypes.c_float), ("m11", ctypes.c_float), ("m12", ctypes.c_float), ("m13", ctypes.c_float),
                ("m20", ctypes.c_float), ("m21", ctypes.c_float), ("m22", ctypes.c_float), ("m23", ctypes.c_float),
                ("m30", ctypes.c_float), ("m31", ctypes.c_float), ("m32", ctypes.c_float), ("m33", ctypes.c_float)]
    

class Il2CppArray(ctypes.Structure):
    _fields_ = [
        ("klass", ctypes.c_void_p),
        ("monitor", ctypes.c_void_p),
        ("bounds", ctypes.c_void_p),
        ("max_length", ctypes.c_int),
    ]


class Il2CppString(ctypes.Structure):
    _fields_ = [
        ("klass", ctypes.c_void_p),
        ("monitor", ctypes.c_void_p),
        ("length", ctypes.c_int),
        ("_padding", ctypes.c_int),
    ]

class Il2CppImage(ctypes.Structure):
    _pack_ = ctypes.sizeof(ctypes.c_void_p)
    pass


class Il2CppAssembly(ctypes.Structure):
    _pack_ = ctypes.sizeof(ctypes.c_void_p)
    pass


class Il2CppAssemblyName(ctypes.Structure):
    _pack_ = ctypes.sizeof(ctypes.c_void_p)
    _fields_ = [
        ("name", ctypes.c_char_p),
        ("culture", ctypes.c_char_p),
        ("hash_value", ctypes.c_char_p),
        ("public_key", ctypes.c_char_p),
        ("hash_alg", ctypes.c_uint32),
        ("hash_len", ctypes.c_int32),
        ("flags", ctypes.c_uint32),
        ("major", ctypes.c_int32),
        ("minor", ctypes.c_int32),
        ("build", ctypes.c_int32),
        ("revision", ctypes.c_int32),
        ("public_key_token", ctypes.c_uint8 * 8)
    ]


Il2CppImage._fields_ = [
    ("name", ctypes.c_char_p),
    ("nameNoExt", ctypes.c_char_p),
    ("assembly", ctypes.POINTER(Il2CppAssembly)),
    ("typeStart", ctypes.c_int32),
    ("typeCount", ctypes.c_uint32),
    ("exportedTypeStart", ctypes.c_int32),
    ("exportedTypeCount", ctypes.c_uint32),
    ("customAttributeStart", ctypes.c_int32),
    ("customAttributeCount", ctypes.c_uint32),
    ("entryPointIndex", ctypes.c_int32),
    ("nameToClassHashTable", ctypes.c_void_p),
    ("token", ctypes.c_uint32),
    ("dynamic", ctypes.c_uint8),
]


Il2CppAssembly._fields_ = [
    ("image", ctypes.POINTER(Il2CppImage)),
    ("token", ctypes.c_uint32),
    ("referencedAssemblyStart", ctypes.c_int32),
    ("referencedAssemblyCount", ctypes.c_int32),
    ("aname", Il2CppAssemblyName)
]

class Bounds(ctypes.Structure):
    _fields_ = [
        ("center", Vec3),
        ("size", Vec3)
    ]


class RaycastHit(ctypes.Structure):
    _fields_ = [
        ("point", Vec3),
        ("normal", Vec3),
        ("faceID", ctypes.c_uint),
        ("distance", ctypes.c_float),
        ("uv", Vec2),
        ("collider", ctypes.c_void_p)
    ]


class Ray(ctypes.Structure):
    _fields_ = [
        ("m_Direction", Vec3),
        ("m_Origin", Vec3)
    ]