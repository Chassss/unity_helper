"""
Provides high-level wrappers for Unity objects, including
Component-based systems like Transform, Camera, and Scene, etc.

For information on any of the functions in this module refer too the official unity documentation https://docs.unity3d.com/ScriptReference/

"""

import ctypes
from .structures import Vec3, Quaternion, RaycastHit, Bounds, Ray, Matrix4x4, Color, Vec2, Rect

class UnityObject():
    def __init__(self, ptr=None):
        from .main import Il2cpp
        self._il2cpp:Il2cpp = Il2cpp.inst
        self.ptr:int = ptr

class Physics(UnityObject):
    """
    Represents a physics class object

    All methods in this class are static so you can just do some_variable = Physics() and then call any function within this class
    """

    @property
    def gravity(self) -> Vec3|None:
        try:
            gravity = Vec3()
            self._il2cpp._UnityEngine_Physics_get_gravity(ctypes.byref(gravity), self._il2cpp._methodInfoData['_UnityEngine_Physics_get_gravity'])
            return gravity
        except:
            return None

    @property
    def Simulate(self, value:float) -> int|None:
        try:
            self._il2cpp._UnityEngine_Physics_Simulate(value, self._il2cpp._methodInfoData['_UnityEngine_Physics_Simulate'])
            return 1
        except:
            return None
    

    @property
    def simulation(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Physics_get_autoSimulation(self._il2cpp._methodInfoData['_UnityEngine_Physics_get_autoSimulation'])
        except:
            return None


    @simulation.setter
    def simulation(self, value:bool):
        try:
            return self._il2cpp._UnityEngine_Physics_set_autoSimulation(value, self._il2cpp._methodInfoData['_UnityEngine_Physics_set_autoSimulation'])
        except:
            pass

    def Raycast(self, origin:list|tuple|Vec3, direction:list|tuple|Vec3, maxDistance:float, layerMask:int) -> bool|RaycastHit|None:
        try:
            origin = self._il2cpp._vec3_helper(origin)
            direction = self._il2cpp._vec3_helper(direction)
            hitInfo = RaycastHit()
            result = self._il2cpp._UnityEngine_Physics_Raycast(ctypes.pointer(origin), ctypes.pointer(direction), ctypes.byref(hitInfo), maxDistance, layerMask, self._il2cpp._methodInfoData['_UnityEngine_Physics_Raycast'])
            if result:
                hitInfo.collider = self._il2cpp._UnityEngine_Object__FindObjectFromInstanceID(hitInfo.collider, self._il2cpp._methodInfoData['_UnityEngine_Object__FindObjectFromInstanceID'])
                return hitInfo
            return result
        except:
            return None

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
            self._il2cpp._UnityEngine_Rigidbody_get_velocity(ctypes.byref(vel), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_velocity'])
            return vel
        except:
            return None
    
    @velocity.setter
    def velocity(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_velocity(self.ptr, ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_velocity'])
        except:
            pass

    @property
    def angularVelocity(self) -> Vec3|None:
        try:
            vel = Vec3()
            self._il2cpp._UnityEngine_Rigidbody_get_angularVelocity(ctypes.byref(vel), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_angularVelocity'])
            return vel
        except:
            return None
    
    @angularVelocity.setter
    def angularVelocity(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_angularVelocity(self.ptr, ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_angularVelocity'])
        except:
            pass

    @property
    def position(self) -> None:
        try:
            pos = Vec3()
            self._il2cpp._UnityEngine_Rigidbody_get_position(ctypes.byref(pos), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_position'])
            return pos
        except:
            return None
    
    @position.setter
    def position(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_position(self.ptr, ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_position'])
        except:
            pass
    
    @property
    def centerOfMass(self) -> Vec3|None:
        try:
            pos = Vec3()
            self._il2cpp._UnityEngine_Rigidbody_get_centerOfMass(ctypes.byref(pos), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_centerOfMass'])
            return pos
        except:
            return None
        
    @property
    def mass(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Rigidbody_get_mass(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_mass'])
        except:
            return None
        
    @mass.setter
    def mass(self):
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_mass(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_mass'])
        except:
            pass
    
    @property
    def isKinematic(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Rigidbody_get_isKinematic(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_isKinematic'])
        except:
            None
        
    @isKinematic.setter
    def isKinematic(self, value):
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_isKinematic(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_isKinematic'])
        except:
            pass

    @property
    def rotation(self) -> Quaternion|None:
        try:
            rot = Quaternion()
            self._il2cpp._UnityEngine_Rigidbody_get_rotation(ctypes.byref(rot), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_rotation'])
            return rot
        except:
            return None
        
    @rotation.setter
    def rotation(self, rot:list|tuple|Quaternion):
        try:
            rot = self._il2cpp._quaternion_helper(rot)
            if not rot:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_rotation(self.ptr, ctypes.pointer(rot), self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_rotation'])
        except:
            pass


    @property
    def constraints(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Rigidbody_get_constraints(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_constraints'])
        except:
            return None
        
    @constraints.setter
    def constraints(self, value:int):
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_constraints(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_constraints'])
        except:
            pass

    def set_detectCollisions(self, value:bool) -> int|None:
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_detectCollisions(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_detectCollisions'])
            return 1
        except:
            return None

    def set_useGravity(self, value:bool) -> int|None:
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_useGravity(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_useGravity'])
            return 1
        except:
            return
        
    def addForce(self, force:list|tuple|Vec3, mode:int) -> int|None:
        try:
            force = self._il2cpp._vec3_helper(force)
            if not force:
                return None
            
            self._il2cpp._UnityEngine_Rigidbody_AddForce(self.ptr, ctypes.pointer(force), mode, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_AddForce'])
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

    @property
    def enabled(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Behaviour__get_enabled(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Behaviour__get_enabled'])
        except:
            return None
        
    @enabled.setter
    def enabled(self, value) -> None:
        try:
            self._il2cpp._UnityEngine_Behaviour__set_enabled(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Behaviour__set_enabled'])
        except:
            pass
    
    @property
    def gameObject(self) -> Object|None:
        try:
            return Object(self._il2cpp._UnityEngine_Component__get_gameObject(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Component__get_gameObject']))
        except:
            return None
        
    @property
    def transform(self)-> Transform|None:
        try:
            addr = self._il2cpp._UnityEngine_Component__get_transform(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Component__get_transform'])
            if not addr:
                return None
            return Transform(addr)
        except:
            return None
    
    @property
    def tag(self) -> str|None:
        try:
            addr = self._il2cpp._UnityEngine_Component__get_tag(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Component__get_tag'])
            return self._il2cpp.PROCESS.read_unicode_string(addr + 0x14, self._il2cpp.PROCESS.read_int(addr + 0x10) * 2)
        except:
            return None
    
    @tag.setter
    def tag(self, value:str):
        try:
            self._il2cpp._UnityEngine_Component__set_tag(self.ptr, self._il2cpp._il2cpp_string_new(value.encode()), self._il2cpp._methodInfoData['_UnityEngine_Component__set_tag'])
        except:
            pass

    def destroy(self) -> None:
        try:
            self._il2cpp._UnityEngine_Object__Destroy(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Object__Destroy'])
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
            self._il2cpp._UnityEngine_Transform__get_position(ctypes.byref(pos), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_position'])
            return pos
        except:
            return None
    
    @position.setter
    def position(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform__set_position(self.ptr, ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Transform__set_position'])
        except:
            pass
    
    @property
    def rotation(self) -> Quaternion|None:
        try:
            rot = Quaternion()
            self._il2cpp._UnityEngine_Transform__get_rotation(ctypes.byref(rot), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_rotation'])
            return rot
        except:
            return None
    
    @rotation.setter
    def rotation(self, rot:list|tuple|Quaternion):
        try:
            rot = self._il2cpp._quaternion_helper(rot)
            if not rot:
                pass
            self._il2cpp._UnityEngine_Transform__set_rotation(self.ptr, ctypes.byref(rot), self._il2cpp._methodInfoData['_UnityEngine_Transform__set_rotation'])
        except:
            pass

    @property
    def parent(self)-> Transform|None:
        try:
            parent = self._il2cpp._UnityEngine_Transform__get_parent(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_parent'])
            if not parent:
                return None
            return Transform(parent)
        except:
            return None
    
    @parent.setter
    def parent(self, parent:Transform):
        try:
            self._il2cpp._UnityEngine_Transform__set_parent(self.ptr, parent.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__set_parent'])
        except:
            pass

    @property
    def root(self) -> Transform|None:
        try:
            parent = self._il2cpp._UnityEngine_Transform__get_root(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_root'])
            if not parent:
                return None
            return Transform(parent)
        except:
            return None

    @property
    def childcount(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Transform__get_childCount(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_childCount'])
        except:
            return None
    
    @property
    def forward(self)-> Vec3|None:
        try:
            forward = Vec3()
            self._il2cpp._UnityEngine_Transform__get_forward(ctypes.byref(forward), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_forward'])
            return forward
        except:
            return None
    
    @forward.setter
    def forward(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform__set_forward(self.ptr, ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Transform__set_forward'])
        except:
            pass

    @property
    def up(self)-> Vec3|None:
        try:
            up = Vec3()
            self._il2cpp._UnityEngine_Transform__get_up(ctypes.byref(up), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_up'])
            return up
        except:
            return None
        
    @property
    def right(self)-> Vec3|None:
        try:
            right = Vec3()
            self._il2cpp._UnityEngine_Transform__get_right(ctypes.byref(right), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_right'])
            return right
        except:
            return None

    @property
    def eulerAngles(self)-> Vec3|None:
        try:
            angles = Vec3()
            self._il2cpp._UnityEngine_Transform_get_eulerAngles(ctypes.byref(angles), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_eulerAngles'])
            return angles
        except:
            return None
    
    @eulerAngles.setter
    def eulerAngles(self, angles:list|tuple|Vec3):
        try:
            angles = self._il2cpp._vec3_helper(angles)
            if not angles:
                pass
            self._il2cpp._UnityEngine_Transform_set_eulerAngles(self.ptr, ctypes.pointer(angles), self._il2cpp._methodInfoData['_UnityEngine_Transform_set_eulerAngles'])
        except:
            pass

    @property
    def localPosition(self)-> Vec3|None:
        try:
            pos = Vec3()
            self._il2cpp._UnityEngine_Transform_get_localPosition(ctypes.byref(pos), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_localPosition'])
            return pos
        except:
            return None
    
    @localPosition.setter
    def localPosition(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform_set_localPosition(self.ptr, ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Transform_set_localPosition'])
        except:
            pass

    @property
    def hasChanged(self)-> bool|None:
        try:
            return self._il2cpp._UnityEngine_Transform_get_hasChanged(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_hasChanged'])
        except:
            return None
    
    @hasChanged.setter
    def hasChanged(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Transform_set_hasChanged(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Transform_set_hasChanged'])
        except:
            pass


    @property
    def localScale(self)-> Vec3|None:
        try:
            scale = Vec3()
            self._il2cpp._UnityEngine_Transform_get_localScale(ctypes.byref(scale), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_localScale'])
            return scale
        except:
            return None
    
    @localScale.setter
    def localScale(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform_set_localScale(self.ptr, ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Transform_set_localScale'])
        except:
            pass

    @property
    def localEulerAngles(self)-> Vec3|None:
        try:
            angles = Vec3()
            self._il2cpp._UnityEngine_Transform_get_localEulerAngles(ctypes.byref(angles), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_localEulerAngles'])
            return angles
        except:
            return None
    
    @localEulerAngles.setter
    def localEulerAngles(self, pos:list|tuple|Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform_set_localEulerAngles(self.ptr, ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Transform_set_localEulerAngles'])
        except:
            pass

    @property
    def worldToLocalMatrix(self)-> Matrix4x4|None:
        try:
            matrix = Matrix4x4()
            self._il2cpp._UnityEngine_Transform_get_worldToLocalMatrix(ctypes.byref(matrix), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_worldToLocalMatrix'])
            return matrix
        except:
            return None
        
    @property
    def localToWorldMatrix(self)-> Vec3|None:
        try:
            matrix = Matrix4x4()
            self._il2cpp._UnityEngine_Transform_get_localToWorldMatrix(ctypes.byref(matrix), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_localToWorldMatrix'])
            return matrix
        except:
            return None

    def IsChildOf(self, transform:Transform) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Transform__IsChildOf(self.ptr, transform.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__IsChildOf'])
        except:
            return None
        
    def find(self, transform_str:str)-> Transform|None:
        try:
            found = self._il2cpp._UnityEngine_Transform__Find(self.ptr, self._il2cpp._il2cpp_string_new(transform_str.encode()), self._il2cpp._methodInfoData['_UnityEngine_Transform__Find'])
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
            self._il2cpp._UnityEngine_Transform__LookAt_pos(self.ptr, ctypes.pointer(pos), ctypes.pointer(direction), self._il2cpp._methodInfoData['_UnityEngine_Transform__LookAt_pos'])
            return 1
        except:
            return None
        
    def LookAt_transform(self, transform:Transform) -> int|None:
        try:
            self._il2cpp._UnityEngine_Transform__LookAt_transform(self.ptr, transform.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__LookAt_transform'])
            return 1
        except:
            return None
        
    def translate(self, translation:list|tuple|Vec3, relativeTo:int) -> int|None:
        try:
            translation = self._il2cpp._vec3_helper(translation)
            if not translation:
                return None
            self._il2cpp._UnityEngine_Transform__translate(self.ptr, ctypes.pointer(translation), relativeTo, self._il2cpp._methodInfoData['_UnityEngine_Transform__translate'])
            return 1
        except:
            return None
        
    def GetChild(self, index:int) -> Transform|None:
        try:
            child = self._il2cpp._UnityEngine_Transform__GetChild(self.ptr, index, self._il2cpp._methodInfoData['_UnityEngine_Transform__GetChild'])
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
            name_addr = self._il2cpp._UnityEngine_Scene__get_name(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Scene__get_name'])
            return self._il2cpp.PROCESS.read_unicode_string(name_addr + 0x14, self._il2cpp.PROCESS.read_int(name_addr + 0x10) * 2)
        except:
            return None
    
    @property
    def path(self) -> str|None:
        try:
            name_addr = self._il2cpp._UnityEngine_Scene__get_path(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Scene__get_path'])
            return self._il2cpp.PROCESS.read_unicode_string(name_addr + 0x14, self._il2cpp.PROCESS.read_int(name_addr + 0x10) * 2)
        except:
            return None
    
    @property
    def rootCount(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_rootCount(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Scene__get_rootCount'])
        except:
            return None
        
    @property
    def loaded(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_isLoaded(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Scene__get_isLoaded'])
        except:
            return None
        
    def IsValid(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Scene__IsValid(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Scene__IsValid'])
        except:
            return None
    
    @property
    def guid(self) -> str|None:
        try:
            name_addr = self._il2cpp._UnityEngine_Scene__get_guid(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Scene__get_guid'])
            return self._il2cpp.PROCESS.read_unicode_string(name_addr + 0x14, self._il2cpp.PROCESS.read_int(name_addr + 0x10) * 2)
        except:
            return None
        
    @property
    def buildIndex(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_buildIndex(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Scene__get_buildIndex'])
        except:
            return None
        
    @property
    def handle(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_handle(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Scene__get_handle'])
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
            name_addr = self._il2cpp._UnityEngine_Object__get_name(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Object__get_name'])
            return self._il2cpp.PROCESS.read_unicode_string(name_addr + 0x14, self._il2cpp.PROCESS.read_int(name_addr + 0x10) * 2)
        except:
            return None
    
    @name.setter
    def name(self, value:str):
        try:
            self._il2cpp._UnityEngine_Object__set_name(self.ptr, self._il2cpp._il2cpp_string_new(value.encode()), self._il2cpp._methodInfoData['_UnityEngine_Object__set_name'])
        except:
            pass
    
    @property
    def isStatic(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_isStatic(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_isStatic'])
        except:
            return None
        
    @property
    def layer(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_layer(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_layer'])
        except:
            return None
        
    @layer.setter
    def layer(self, value:int):
        try:
            self._il2cpp._UnityEngine_GameObject__set_layer(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_GameObject__set_layer'])
        except:
            pass

    @property
    def transform(self)-> Transform|None:
        try:
            addr = self._il2cpp._UnityEngine_GameObject__get_transform(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_transform'])
            if not addr:
                return None
            return Transform(addr)
        except:
            return None

    @property
    def tag(self) -> str|None:
        try:
            addr = self._il2cpp._UnityEngine_GameObject__get_tag(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_tag'])
            return self._il2cpp.PROCESS.read_unicode_string(addr + 0x14, self._il2cpp.PROCESS.read_int(addr + 0x10) * 2)
        except:
            return None
    
    @tag.setter
    def tag(self, value:str):
        try:
            self._il2cpp._UnityEngine_GameObject__set_tag(self.ptr, self._il2cpp._il2cpp_string_new(value.encode()), self._il2cpp._methodInfoData['_UnityEngine_GameObject__set_tag'])
        except:
            pass

    @property
    def hideFlags(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Object__get_hideFlags(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Object__get_hideFlags'])
        except:
            return None
    
    @hideFlags.setter
    def hideFlags(self, value:int):
        try:
            self._il2cpp._UnityEngine_Object__set_hideFlags(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Object__get_hideFlags'])
        except:
            pass

    @property
    def scene(self) -> Scene|None:
        try:
            addr = self._il2cpp._UnityEngine_GameObject__get_scene(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_scene'])
            if not addr:
                return None
            return Scene(addr)
        except:
            return None
        
    @property
    def activeInHierarchy(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_activeInHierarchy(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_activeInHierarchy'])
        except:
            return None

    @property
    def activeSelf(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_activeSelf(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_activeSelf'])
        except:
            return None
        
    @property
    def sceneCullingMask(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_sceneCullingMask(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_sceneCullingMask'])
        except:
            return None
    
        
    def SetActive(self, value:bool) -> int|None:
        try:
            self._il2cpp._UnityEngine_GameObject__SetActive(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_GameObject__SetActive'])
            return 1
        except:
            return None

    def destroy(self) -> int|None:
        try:
            self._il2cpp._UnityEngine_Object__Destroy(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Object__Destroy'])
            return 1
        except:
            return None
    
    def GetComponent(self, type_object:int) -> Component|None:
        try:
            addr = self._il2cpp._UnityEngine_GameObject__GetComponent(self.ptr, type_object, self._il2cpp._methodInfoData['_UnityEngine_GameObject__GetComponent'])
            if not addr:
                return None
            return Component(addr)
        except:
            return None
        
    def GetComponents(self) -> list[Component]|None:
        try:
            arr = self._il2cpp._UnityEngine_GameObject__GetComponents(self.ptr, self._il2cpp._component.object, self._il2cpp._methodInfoData['_UnityEngine_GameObject__GetComponents'])
            components = [Component(i) for i in self._il2cpp._read_il2cpp_array(arr)]
            return components
        except:
            return None
        
    def AddComponent(self, type_object:int) -> int|None:
        try:
            self._il2cpp._UnityEngine_GameObject__AddComponent(self.ptr, type_object, self._il2cpp._methodInfoData['_UnityEngine_GameObject__AddComponent'])
            return 1
        except:
            return None
        
    def Instantiate(self) -> Object|None:
        try:
            new_obj = self._il2cpp._UnityEngine_Object__Instantiate(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Object__Instantiate'])
            if not new_obj:
                return None
            return Object(new_obj)
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
            return self._il2cpp._UnityEngine_Camera__get_fieldOfView(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_fieldOfView'])
        except:
            return None

    @fov.setter
    def fov(self, fov:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_fieldOfView(self.ptr, ctypes.c_float(fov), self._il2cpp._methodInfoData['_UnityEngine_Camera__set_fieldOfView'])
        except:
            pass
    
    @property
    def depth(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_depth(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_depth'])
        except:
            return None
    
    @depth.setter
    def depth(self, depth:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_depth(self.ptr, ctypes.c_float(depth), self._il2cpp._methodInfoData['_UnityEngine_Camera__set_depth'])
        except:
            pass

    @property
    def allowDynamicResolution(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_allowDynamicResolution(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_allowDynamicResolution'])
        except:
            return None
        

    @property
    def allowMSAA(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_allowMSAA(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_allowMSAA'])
        except:
            return None
    
    @allowMSAA.setter
    def allowMSAA(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Camera__set_allowMSAA(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_allowMSAA'])
        except:
            pass

    @property
    def allowHDR(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_allowHDR(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_allowHDR'])
        except:
            return None
    
    @allowHDR.setter
    def allowHDR(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Camera__set_allowHDR(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_allowHDR'])
        except:
            pass

    @property
    def aspect(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_aspect(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_aspect'])
        except:
            return None
    
    @aspect.setter
    def aspect(self, value:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_aspect(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_aspect'])
        except:
            pass

    @property
    def backgroundColor(self) -> Color|None:
        try:
            color = Color()
            self._il2cpp._UnityEngine_Camera__get_backgroundColor(ctypes.byref(color), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_backgroundColor'])
            return color
        except:
            return None
    
    @backgroundColor.setter
    def backgroundColor(self, color:Color):
        try:
            self._il2cpp._UnityEngine_Camera__set_backgroundColor(self.ptr, ctypes.pointer(color), self._il2cpp._methodInfoData['_UnityEngine_Camera__set_backgroundColor'])
        except:
            pass
    
    @property
    def cameraToWorldMatrix(self) -> Matrix4x4|None:
        try:
            matrix = Matrix4x4()
            self._il2cpp._UnityEngine_Camera__get_cameraToWorldMatrix(ctypes.byref(Matrix4x4), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_cameraToWorldMatrix'])
            return matrix
        except:
            return None

    @property
    def cameraType(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_cameraType(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_cameraType'])
        except:
            return None
    
    @cameraType.setter
    def cameraType(self, type_object:int):
        try:
            self._il2cpp._UnityEngine_Camera__set_cameraType(self.ptr, type_object, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_cameraType'])
        except:
            pass

    @property
    def clearFlags(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_clearFlags(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_clearFlags'])
        except:
            return None
    
    @clearFlags.setter
    def clearFlags(self, value:int):
        try:
            self._il2cpp._UnityEngine_Camera__set_clearFlags(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_clearFlags'])
        except:
            pass

    @property
    def cullingMask(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_cullingMask(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_cullingMask'])
        except:
            return None
    
    @cullingMask.setter
    def cullingMask(self, value:int):
        try:
            self._il2cpp._UnityEngine_Camera__set_cullingMask(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_cullingMask'])
        except:
            pass

    @property
    def eventMask(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_eventMask(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_eventMask'])
        except:
            return None

    
    @property
    def farClipPlane(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_farClipPlane(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_farClipPlane'])
        except:
            return None
    
    @farClipPlane.setter
    def farClipPlane(self, value:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_farClipPlane(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_farClipPlane'])
        except:
            pass

    @property
    def nearClipPlane(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_nearClipPlane(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_nearClipPlane'])
        except:
            return None
    
    @nearClipPlane.setter
    def nearClipPlane(self, value:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_nearClipPlane(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_nearClipPlane'])
        except:
            pass

    @property
    def focalLength(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_focalLength(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_focalLength'])
        except:
            return None

    @property
    def gateFit(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_gateFit(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_gateFit'])
        except:
            return None
    
    @gateFit.setter
    def gateFit(self, value:int):
        try:
            self._il2cpp._UnityEngine_Camera__set_gateFit(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_gateFit'])
        except:
            pass

    @property
    def lensShift(self) -> Vec2|None:
        try:
            lens = Vec2()
            self._il2cpp._UnityEngine_Camera__get_lensShift(ctypes.byref(lens), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_lensShift'])
            return lens
        except:
            return None
    
    @lensShift.setter
    def lensShift(self, value:list|tuple|Vec2):
        try:
            lens = self._il2cpp._vec2_helper(value)
            self._il2cpp._UnityEngine_Camera__set_lensShift(ctypes.pointer(lens), self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_lensShift'])
        except:
            pass

    @property
    def orthographicSize(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_orthographicSize(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_orthographicSize'])
        except:
            return None
    
    @orthographicSize.setter
    def orthographicSize(self, value:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_orthographicSize(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_orthographicSize'])
        except:
            pass

    @property
    def orthographic(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_orthographic(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_orthographic'])
        except:
            return None
    
    @orthographic.setter
    def orthographic(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Camera__set_orthographic(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_orthographic'])
        except:
            pass

    @property
    def pixelHeight(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_pixelHeight(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_pixelHeight'])
        except:
            return None
        
    @property
    def pixelWidth(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_pixelWidth(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_pixelWidth'])
        except:
            return None
        

    @property
    def pixelRect(self) -> Rect|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_pixelRect(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_pixelRect'])
        except:
            return None
    
    @pixelRect.setter
    def pixelRect(self, rect:list|tuple|Rect):
        try:
            rect = self._il2cpp._rect_helper(rect)
            self._il2cpp._UnityEngine_Camera__set_pixelRect(self.ptr, ctypes.pointer(rect), self._il2cpp._methodInfoData['_UnityEngine_Camera__set_pixelRect'])
        except:
            pass

    @property
    def targetDisplay(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_targetDisplay(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_targetDisplay'])
        except:
            return None
    
    @targetDisplay.setter
    def targetDisplay(self, value:int):
        try:
            self._il2cpp._UnityEngine_Camera__set_targetDisplay(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_targetDisplay'])
        except:
            pass

    @property
    def useOcclusionCulling(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_useOcclusionCulling(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_useOcclusionCulling'])
        except:
            return None
    
    @useOcclusionCulling.setter
    def useOcclusionCulling(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Camera__set_useOcclusionCulling(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_useOcclusionCulling'])
        except:
            pass

    @property
    def usePhysicalProperties(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_usePhysicalProperties(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_usePhysicalProperties'])
        except:
            return None
    
    @usePhysicalProperties.setter
    def usePhysicalProperties(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Camera__set_usePhysicalProperties(self.ptr, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_usePhysicalProperties'])
        except:
            pass


class Collider(Component):
    @property
    def attachedRigidbody(self) -> Rigidbody|None:
        try:
            body = self._il2cpp._UnityEngine_Collider_get_attachedRigidbody(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Collider_get_attachedRigidbody'])
            if not body:
                return None
            return Rigidbody(body)
        except:
            return None
        
    @property
    def bounds(self) -> Bounds|None:
        try:
            return self._il2cpp._UnityEngine_Collider_get_bounds(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Collider_get_bounds'])
        except:
            return None
        
    @property
    def enabled(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Collider_get_enabled(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Collider_get_enabled'])
        except:
            return None
        
    @enabled.setter
    def enabled(self):
        try:
            self._il2cpp._UnityEngine_Collider_set_enabled(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Collider_set_enabled'])
        except:
            pass
        
    @property
    def isTrigger(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Collider_get_isTrigger(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Collider_get_isTrigger'])
        except:
            return None
        
    @isTrigger.setter
    def isTrigger(self):
        try:
            self._il2cpp._UnityEngine_Collider_set_isTrigger(self.ptr, self._il2cpp._methodInfoData['_UnityEngine_Collider_set_isTrigger'])
        except:
            pass

    def Raycast(self, ray:Ray, maxDistance:float) -> bool|RaycastHit|None:
        try:
            hitInfo = RaycastHit()
            result = self._il2cpp._UnityEngine_Collider_Raycast(self.ptr, ctypes.pointer(ray), ctypes.byref(hitInfo), maxDistance, self._il2cpp._methodInfoData['_UnityEngine_Collider_Raycast'])
            if result:
                hitInfo.collider = self._il2cpp._UnityEngine_Object__FindObjectFromInstanceID(hitInfo.collider, self._il2cpp._methodInfoData['_UnityEngine_Object__FindObjectFromInstanceID'])
                return hitInfo
            return result
        except:
            return None