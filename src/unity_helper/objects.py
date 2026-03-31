"""
Provides high-level wrappers for Unity objects, including
Component-based systems like Transform, Camera, and Scene, etc.

"""

import ctypes
from .structures import Vec3, Quaternion, Rect

class UnityObject():
    def __init__(self, ptr):
        from .main import Il2cpp
        self._il2cpp:Il2cpp = Il2cpp.inst
        self.ptr:int = ptr


class Rigidbody(UnityObject):
    """
    Represents a physics body with mass, velocity, and forces.
    
    To create your own Rigidbody class simply get the address of the Rigidbody object
    and then do Rigidbody(address)
    """
    @property
    def velocity(self) -> Vec3|None:
        try:
            vel = Vec3()
            self._il2cpp._UnityEngine_Rigidbody_get_velocity(ctypes.byref(vel), self.ptr, 0)
            return vel
        except:
            return None
    
    @velocity.setter
    def velocity(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_velocity(self.ptr, ctypes.pointer(pos), 0)
        except:
            pass

    @property
    def position(self) -> None:
        try:
            pos = Vec3()
            self._il2cpp._UnityEngine_Rigidbody_get_position(ctypes.byref(pos), self.ptr, 0)
            return pos
        except:
            return None
    
    @position.setter
    def position(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_position(self.ptr, ctypes.pointer(pos), 0)
        except:
            pass
    
    @property
    def centerOfMass(self) -> Vec3|None:
        try:
            pos = Vec3()
            self._il2cpp._UnityEngine_Rigidbody_get_centerOfMass(ctypes.byref(pos), self.ptr, 0)
            return pos
        except:
            return None
        
    @property
    def mass(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Rigidbody_get_mass(self.ptr, 0)
        except:
            return None
        
    @mass.setter
    def mass(self):
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_mass(self.ptr, 0)
        except:
            pass
    
    @property
    def isKinematic(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Rigidbody_get_isKinematic(self.ptr, 0)
        except:
            None
        
    @isKinematic.setter
    def isKinematic(self, value):
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_isKinematic(self.ptr, value, 0)
        except:
            pass

    @property
    def rotation(self) -> Quaternion|None:
        try:
            rot = Quaternion()
            self._il2cpp._UnityEngine_Rigidbody_get_rotation(ctypes.byref(rot), self.ptr, 0)
            return rot
        except:
            return None
        
    @rotation.setter
    def rotation(self, rot:list|tuple|Quaternion):
        try:
            rot = self._il2cpp._quaternion_helper(rot)
            if not rot:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_rotation(self.ptr, ctypes.pointer(rot), 0)
        except:
            pass

    def set_detectCollisions(self, value:bool) -> int|None:
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_detectCollisions(self.ptr, value, 0)
            return 1
        except:
            return None

    def set_useGravity(self, value:bool) -> int|None:
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_useGravity(self.ptr, value, 0)
            return 1
        except:
            return
        
    def addForce(self, force:list|tuple|Vec3, mode:int) -> int|None:
        try:
            force = self._il2cpp._vec3_helper(force)
            if not force:
                return None
            
            self._il2cpp._UnityEngine_Rigidbody_AddForce(self.ptr, ctypes.pointer(force), mode, 0)
            return 1
        except:
            return None

class Component(UnityObject):
    """
    Base class for objects that can be attached to objects to define behavior.
    
    To create your own Component class simply get the address of the Component object
    and then do Component(address)
    """
    @property
    def name(self) -> str|None:
        try:
            klass = self._il2cpp._il2cpp_object_get_class(self.ptr)
            name_ptr = self._il2cpp._il2cpp_class_get_name(klass)
            return name_ptr.decode() if name_ptr else None
        except:
            return None
        # return self._il2cpp.PROCESS.read_unicode_string(name_ptr + 0x14, self._il2cpp.PROCESS.read_int(name_ptr + 0x10) * 2)

    @property
    def enabled(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Behaviour__get_enabled(self.ptr, 0)
        except:
            return None
        
    @enabled.setter
    def enabled(self, value) -> None:
        try:
            self._il2cpp._UnityEngine_Behaviour__set_enabled(self.ptr, value, 0)
        except:
            pass
    
    @property
    def gameObject(self) -> Object|None:
        try:
            return Object(self._il2cpp._UnityEngine_Component__get_gameObject(self.ptr, 0))
        except:
            return None
        
    @property
    def transform(self)-> Transform|None:
        try:
            return Transform(self._il2cpp._UnityEngine_Component__get_transform(self.ptr, 0))
        except:
            return None
    
    @property
    def tag(self) -> str|None:
        try:
            addr = self._il2cpp._UnityEngine_Component__get_tag(self.ptr, 0)
            return self._il2cpp.PROCESS.read_unicode_string(addr + 0x14, self._il2cpp.PROCESS.read_int(addr + 0x10) * 2)
        except:
            return None
    
    @tag.setter
    def tag(self, value:str):
        try:
            self._il2cpp._UnityEngine_Component__set_tag(self.ptr, self._il2cpp._il2cpp_string_new(value.encode()), 0)
        except:
            pass

    def destroy(self) -> None:
        try:
            self._il2cpp._UnityEngine_Object__Destroy(self.ptr, 0, 0)
            return 1
        except:
            return None


class Transform(Component):
    """
    Represents the position, rotation, and scale of an entity.
    
    To create your own Transform class simply get the address of the Transform object
    and then do Transform(address)
    """

    @property
    def position(self) -> Vec3|None:
        try:
            pos = Vec3()
            self._il2cpp._UnityEngine_Transform__get_position(ctypes.byref(pos), self.ptr, 0)
            return pos
        except:
            return None
    
    @position.setter
    def position(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform__set_position(self.ptr, ctypes.pointer(pos), 0)
        except:
            pass
    
    @property
    def rotation(self) -> Quaternion|None:
        try:
            rot = Quaternion()
            self._il2cpp._UnityEngine_Transform__get_rotation(ctypes.byref(rot), self.ptr, 0)
            return rot
        except:
            return None
    
    @rotation.setter
    def rotation(self, rot:list|tuple|Quaternion):
        try:
            rot = self._il2cpp._quaternion_helper(rot)
            if not rot:
                pass
            self._il2cpp._UnityEngine_Transform__set_rotation(self.ptr, ctypes.byref(rot), 0)
        except:
            pass
    
    @property
    def rect(self) -> Rect|None:
        try:
            rect = Rect()
            self._il2cpp._UnityEngine_Transform__get_rect(ctypes.byref(rect), self.ptr, 0)
            return rect
        except:
            return None

    @property
    def parent(self)-> Transform|None:
        try:
            parent = self._il2cpp._UnityEngine_Transform__get_parent(self.ptr, 0)
            if not parent:
                return None
            return Transform(parent)
        except:
            return None
    
    @parent.setter
    def parent(self, parent:Transform):
        try:
            self._il2cpp._UnityEngine_Transform__set_parent(self.ptr, parent.ptr, 0)
        except:
            pass

    @property
    def root(self) -> Transform|None:
        try:
            parent = self._il2cpp._UnityEngine_Transform__get_root(self.ptr, 0)
            if not parent:
                return None
            return Transform(parent)
        except:
            return None

    @property
    def childcount(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Transform__get_childCount(self.ptr, 0)
        except:
            return None
    
    @property
    def forward(self)-> Vec3|None:
        try:
            return self._il2cpp._UnityEngine_Transform__get_forward(self.ptr, 0)
        except:
            return None
    
    @forward.setter
    def forward(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform__set_forward(self.ptr, ctypes.pointer(pos), 0)
        except:
            pass

    @property
    def up(self)-> Vec3|None:
        try:
            return self._il2cpp._UnityEngine_Transform__get_up(self.ptr, 0)
        except:
            return None
        
    @property
    def right(self)-> Vec3|None:
        try:
            return self._il2cpp._UnityEngine_Transform__get_right(self.ptr, 0)
        except:
            return None

    def IsChildOf(self, transform:Transform) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Transform__IsChildOf(self.ptr, transform.ptr, 0)
        except:
            return None
        
    def find(self, transform_str:str)-> Transform|None:
        try:
            found = self._il2cpp._UnityEngine_Transform__Find(self.ptr, self._il2cpp._il2cpp_string_new(transform_str.encode()), 0)
            if not found:
                return None
            return Transform(self, found)
        except:
            return None
        
    def LookAt_pos(self, pos:list|tuple|Vec3, direction:list|tuple|Vec3) -> int|None:
        try:
            pos = self._il2cpp._vec3_helper(pos)
            direction = self._il2cpp._vec3_helper(direction)
            if not pos or not direction:
                return None
            self._il2cpp._UnityEngine_Transform__LookAt_pos(self.ptr, ctypes.pointer(pos), ctypes.pointer(direction), 0)
            return 1
        except:
            return None
        
    def LookAt_transform(self, transform:Transform) -> int|None:
        try:
            self._il2cpp._UnityEngine_Transform__LookAt_transform(self.ptr, transform.ptr, 0)
            return 1
        except:
            return None
        
    def translate(self, translation:list|tuple|Vec3, relativeTo:int) -> int|None:
        try:
            translation = self._il2cpp._vec3_helper(translation)
            if not translation:
                return None
            self._il2cpp._UnityEngine_Transform__translate(self.ptr, ctypes.pointer(translation), relativeTo, 0)
            return 1
        except:
            return None
        
    def GetChild(self, index:int) -> Transform|None:
        try:
            child = self._il2cpp._UnityEngine_Transform__GetChild(self.ptr, index, 0)
            if not child:
                return None
            return Transform(child)
        except:
            return None

class Scene(UnityObject):
    """
    Represents a collection of entities and components.
    
    To create your own Scene class simply get the address of the Scene object
    and then do Scene(address)
    """
    @property
    def name(self) -> str|None:
        try:
            name_addr = self._il2cpp._UnityEngine_Scene__get_name(self.ptr, 0)
            return self._il2cpp.PROCESS.read_unicode_string(name_addr + 0x14, self._il2cpp.PROCESS.read_int(name_addr + 0x10) * 2)
        except:
            return None
    
    @property
    def path(self) -> str|None:
        try:
            name_addr = self._il2cpp._UnityEngine_Scene__get_path(self.ptr, 0)
            return self._il2cpp.PROCESS.read_unicode_string(name_addr + 0x14, self._il2cpp.PROCESS.read_int(name_addr + 0x10) * 2)
        except:
            return None
    
    @property
    def rootCount(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_rootCount(self.ptr, 0)
        except:
            return None
        
    @property
    def loaded(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_isLoaded(self.ptr, 0)
        except:
            return None
        
    def IsValid(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Scene__IsValid(self.ptr, 0)
        except:
            return None
    
    @property
    def guid(self) -> str|None:
        try:
            name_addr = self._il2cpp._UnityEngine_Scene__get_guid(self.ptr, 0)
            return self._il2cpp.PROCESS.read_unicode_string(name_addr + 0x14, self._il2cpp.PROCESS.read_int(name_addr + 0x10) * 2)
        except:
            return None
        
    @property
    def buildIndex(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_buildIndex(self.ptr, 0)
        except:
            return None
        
    @property
    def handle(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_handle(self.ptr, 0)
        except:
            return None
        
    

class Object(UnityObject):
    """
    Base class for all engine objects.
    
    To create your own Object class simply get the address of the Object object
    and then do Object(address)

    Not all functions will work as expected because all GameObjects are objects but not all Objects are GameObjects
    """
    @property
    def name(self) -> str|None:
        try:
            name_addr = self._il2cpp._UnityEngine_Object__get_name(self.ptr, 0)
            return self._il2cpp.PROCESS.read_unicode_string(name_addr + 0x14, self._il2cpp.PROCESS.read_int(name_addr + 0x10) * 2)
        except:
            return None
    
    @name.setter
    def name(self, value:str):
        try:
            self._il2cpp._UnityEngine_Object__set_name(self.ptr, self._il2cpp._il2cpp_string_new(value.encode()), 0)
        except:
            pass
    
    @property
    def isStatic(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_isStatic(self.ptr, 0)
        except:
            return None
        
    @property
    def layer(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_layer(self.ptr, 0)
        except:
            return None
        
    @name.setter
    def layer(self, value:int):
        try:
            self._il2cpp._UnityEngine_Object__set_layer(self.ptr, value, 0)
        except:
            pass
    
    def SetActive(self, value:bool) -> int|None:
        try:
            self._il2cpp._UnityEngine_GameObject__SetActive(self.ptr, value, 0)
            return 1
        except:
            return None

    def destroy(self) -> int|None:
        try:
            self._il2cpp._UnityEngine_Object__Destroy(self.ptr, 0)
            return 1
        except:
            return None
        
    def GetComponents(self) -> list[Component]|None:
        try:
            arr = self._il2cpp._UnityEngine_GameObject__GetComponents(self.ptr, self._il2cpp._component.object, 0)
            components = [Component(i) for i in self._il2cpp._read_il2cpp_array(arr)]
            return components
        except:
            return None

    @property
    def transform(self)-> Transform|None:
        try:
            return Transform(self._il2cpp._UnityEngine_GameObject__get_transform(self.ptr, 0))
        except:
            return None

    def AddComponent(self, type_:int) -> int|None:
        try:
            self._il2cpp._UnityEngine_GameObject__AddComponent(self.ptr, type_, 0)
            return 1
        except:
            return None

    @property
    def tag(self) -> str|None:
        try:
            addr = self._il2cpp._UnityEngine_GameObject__get_tag(self.ptr, 0)
            return self._il2cpp.PROCESS.read_unicode_string(addr + 0x14, self._il2cpp.PROCESS.read_int(addr + 0x10) * 2)
        except:
            return None
    
    @tag.setter
    def tag(self, value:str):
        try:
            self._il2cpp._UnityEngine_GameObject__set_tag(self.ptr, self._il2cpp._il2cpp_string_new(value.encode()), 0)
        except:
            pass

    @property
    def scene(self) -> Scene|None:
        try:
            addr = self._il2cpp._UnityEngine_GameObject__get_scene(self.ptr, 0)
            if not addr:
                return None
            return Scene(addr)
        except:
            return None


class Camera(Component):
    """
    Defines a viewpoint into the scene.
    
    To create your own Camera class simply get the address of the Camera object
    and then do Camera(address)
    """
    @property
    def fov(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_fieldOfView(self.ptr, 0)
        except:
            return None

    @fov.setter
    def fov(self, fov:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_fieldOfView(self.ptr, ctypes.c_float(fov), 0)
        except:
            pass
    
    @property
    def depth(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_depth(self.ptr, 0)
        except:
            return None
    
    @depth.setter
    def depth(self, depth:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_depth(self.ptr, ctypes.c_float(depth), 0)
        except:
            pass