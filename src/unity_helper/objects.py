"""
Provides high-level wrappers for Unity objects, including
Component-based systems like Transform, Camera, and Scene, etc.

For information on any of the functions in this module refer too the official unity documentation https://docs.unity3d.com/ScriptReference/

"""

import ctypes as _ctypes
from . import structures as _struct

class _UnityObject():
    def __init__(self, ptr=None):
        from .main import Il2cpp
        self._il2cpp:Il2cpp = Il2cpp.inst
        self._instance:int = ptr

    @property
    def instance(self):
        return self._instance

class Physics(_UnityObject):
    """
    Represents a physics class object

    All methods in this class are static so you can just do some_variable = Physics() and then call any function within this class
    """

    @property
    def gravity(self) -> _struct.Vec3|None:
        try:
            gravity = _struct.Vec3()
            self._il2cpp._UnityEngine_Physics_get_gravity(_ctypes.byref(gravity), self._il2cpp._methodInfoData['_UnityEngine_Physics_get_gravity'])
            return gravity
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

    def Simulate(self, value:float) -> int|None:
        try:
            self._il2cpp._UnityEngine_Physics_Simulate(value, self._il2cpp._methodInfoData['_UnityEngine_Physics_Simulate'])
            return 1
        except:
            return None

    def Raycast(self, origin:list|tuple|_struct.Vec3, direction:list|tuple|_struct.Vec3, maxDistance:float, layerMask:int) -> bool|_struct.RaycastHit|None:
        try:
            origin = self._il2cpp._vec3_helper(origin)
            direction = self._il2cpp._vec3_helper(direction)
            hitInfo = _struct.RaycastHit()
            result = self._il2cpp._UnityEngine_Physics_Raycast(_ctypes.pointer(origin), _ctypes.pointer(direction), _ctypes.byref(hitInfo), maxDistance, layerMask, self._il2cpp._methodInfoData['_UnityEngine_Physics_Raycast'])
            if result:
                hitInfo.collider = self._il2cpp._UnityEngine_Object__FindObjectFromInstanceID(hitInfo.collider, self._il2cpp._methodInfoData['_UnityEngine_Object__FindObjectFromInstanceID'])
                return hitInfo
            return result
        except:
            return None
        
    def RaycastRay(self, ray:_struct.Ray, maxDistance:float, layerMask:int) -> bool|_struct.RaycastHit|None:
        try:
            hitInfo = _struct.RaycastHit()
            result = self._il2cpp._UnityEngine_Physics_RaycastRay(_ctypes.pointer(ray), _ctypes.byref(hitInfo), maxDistance, layerMask, self._il2cpp._methodInfoData['_UnityEngine_Physics_RaycastRay'])
            if result:
                hitInfo.collider = self._il2cpp._UnityEngine_Object__FindObjectFromInstanceID(hitInfo.collider, self._il2cpp._methodInfoData['_UnityEngine_Object__FindObjectFromInstanceID'])
                return hitInfo
            return result
        except:
            return None

class Rigidbody(_UnityObject):
    """
    Represents a physics body with mass, velocity, and forces.
    
    To create your own Rigidbody class simply get the address of the Rigidbody object\n
    and then do Rigidbody(address)
    """
    @property
    def velocity(self) -> _struct.Vec3|None:
        try:
            vel = _struct.Vec3()
            self._il2cpp._UnityEngine_Rigidbody_get_velocity(_ctypes.byref(vel), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_velocity'])
            return vel
        except:
            return None
    
    @velocity.setter
    def velocity(self, pos:list|tuple|_struct.Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_velocity(self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_velocity'])
        except:
            pass

    @property
    def angularVelocity(self) -> _struct.Vec3|None:
        try:
            vel = _struct.Vec3()
            self._il2cpp._UnityEngine_Rigidbody_get_angularVelocity(_ctypes.byref(vel), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_angularVelocity'])
            return vel
        except:
            return None
    
    @angularVelocity.setter
    def angularVelocity(self, pos:list|tuple|_struct.Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_angularVelocity(self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_angularVelocity'])
        except:
            pass

    @property
    def position(self) -> None:
        try:
            pos = _struct.Vec3()
            self._il2cpp._UnityEngine_Rigidbody_get_position(_ctypes.byref(pos), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_position'])
            return pos
        except:
            return None
    
    @position.setter
    def position(self, pos:list|tuple|_struct.Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_position(self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_position'])
        except:
            pass
    
    @property
    def centerOfMass(self) -> _struct.Vec3|None:
        try:
            pos = _struct.Vec3()
            self._il2cpp._UnityEngine_Rigidbody_get_centerOfMass(_ctypes.byref(pos), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_centerOfMass'])
            return pos
        except:
            return None
        
    @property
    def mass(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Rigidbody_get_mass(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_mass'])
        except:
            return None
        
    @mass.setter
    def mass(self):
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_mass(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_mass'])
        except:
            pass
    
    @property
    def isKinematic(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Rigidbody_get_isKinematic(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_isKinematic'])
        except:
            None
        
    @isKinematic.setter
    def isKinematic(self, value):
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_isKinematic(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_isKinematic'])
        except:
            pass

    @property
    def rotation(self) -> _struct.Quaternion|None:
        try:
            rot = _struct.Quaternion()
            self._il2cpp._UnityEngine_Rigidbody_get_rotation(_ctypes.byref(rot), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_rotation'])
            return rot
        except:
            return None
        
    @rotation.setter
    def rotation(self, rot:list|tuple|_struct.Quaternion):
        try:
            rot = self._il2cpp._quaternion_helper(rot)
            if not rot:
                pass
            self._il2cpp._UnityEngine_Rigidbody_set_rotation(self.instance, _ctypes.pointer(rot), self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_rotation'])
        except:
            pass


    @property
    def constraints(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Rigidbody_get_constraints(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_get_constraints'])
        except:
            return None
        
    @constraints.setter
    def constraints(self, value:int):
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_constraints(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_constraints'])
        except:
            pass

    def set_detectCollisions(self, value:bool) -> int|None:
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_detectCollisions(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_detectCollisions'])
            return 1
        except:
            return None

    def set_useGravity(self, value:bool) -> int|None:
        try:
            self._il2cpp._UnityEngine_Rigidbody_set_useGravity(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_set_useGravity'])
            return 1
        except:
            return
        
    def addForce(self, force:list|tuple|_struct.Vec3, mode:int) -> int|None:
        try:
            force = self._il2cpp._vec3_helper(force)
            if not force:
                return None
            
            self._il2cpp._UnityEngine_Rigidbody_AddForce(self.instance, _ctypes.pointer(force), mode, self._il2cpp._methodInfoData['_UnityEngine_Rigidbody_AddForce'])
            return 1
        except:
            return None

class Component(_UnityObject):
    """
    Base class for objects that can be attached to objects to define behavior.
    
    To create your own Component class simply get the address of the Component object\n
    and then do Component(address)
    """
    @property
    def name(self) -> str|None:
        try:
            klass = self._il2cpp._il2cpp_object_get_class(self.instance)
            name_ptr = self._il2cpp._il2cpp_class_get_name(klass)
            return name_ptr.decode() if name_ptr else None
        except:
            return None

    @property
    def enabled(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Behaviour__get_enabled(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Behaviour__get_enabled'])
        except:
            return None
        
    @enabled.setter
    def enabled(self, value) -> None:
        try:
            self._il2cpp._UnityEngine_Behaviour__set_enabled(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Behaviour__set_enabled'])
        except:
            pass
    
    @property
    def gameObject(self) -> Object|None:
        try:
            return Object(self._il2cpp._UnityEngine_Component__get_gameObject(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Component__get_gameObject']))
        except:
            return None
        
    @property
    def transform(self)-> Transform|None:
        try:
            addr = self._il2cpp._UnityEngine_Component__get_transform(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Component__get_transform'])
            if not addr:
                return None
            return Transform(addr)
        except:
            return None
    
    @property
    def tag(self) -> str|None:
        try:
            addr = self._il2cpp._UnityEngine_Component__get_tag(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Component__get_tag'])
            return self._il2cpp.memory.read_unicode_string(addr + 0x14, self._il2cpp.memory.read_int(addr + 0x10) * 2)
        except:
            return None
    
    @tag.setter
    def tag(self, value:str):
        try:
            self._il2cpp._UnityEngine_Component__set_tag(self.instance, self._il2cpp._il2cpp_string_new(value.encode()), self._il2cpp._methodInfoData['_UnityEngine_Component__set_tag'])
        except:
            pass

    def destroy(self) -> None:
        try:
            self._il2cpp._UnityEngine_Object__Destroy(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Object__Destroy'])
            return 1
        except:
            return None

class Transform(Component):
    """
    Represents a Transform class object with position, mass, scale, rotation. 
    
    To create your own Transform class simply get the address of the Transform object\n
    and then do Transform(address)
    """

    @property
    def position(self) -> _struct.Vec3|None:
        try:
            pos = _struct.Vec3()
            self._il2cpp._UnityEngine_Transform__get_position(_ctypes.byref(pos), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_position'])
            return pos
        except:
            return None
    
    @position.setter
    def position(self, pos:list|tuple|_struct.Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform__set_position(self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Transform__set_position'])
        except:
            pass
    
    @property
    def rotation(self) -> _struct.Quaternion|None:
        try:
            rot = _struct.Quaternion()
            self._il2cpp._UnityEngine_Transform__get_rotation(_ctypes.byref(rot), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_rotation'])
            return rot
        except:
            return None
    
    @rotation.setter
    def rotation(self, rot:list|tuple|_struct.Quaternion):
        try:
            rot = self._il2cpp._quaternion_helper(rot)
            if not rot:
                pass
            self._il2cpp._UnityEngine_Transform__set_rotation(self.instance, _ctypes.byref(rot), self._il2cpp._methodInfoData['_UnityEngine_Transform__set_rotation'])
        except:
            pass

    @property
    def parent(self)-> Transform|None:
        try:
            parent = self._il2cpp._UnityEngine_Transform__get_parent(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_parent'])
            if not parent:
                return None
            return Transform(parent)
        except:
            return None
    
    @parent.setter
    def parent(self, parent:Transform):
        try:
            self._il2cpp._UnityEngine_Transform__set_parent(self.instance, parent.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__set_parent'])
        except:
            pass

    @property
    def root(self) -> Transform|None:
        try:
            parent = self._il2cpp._UnityEngine_Transform__get_root(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_root'])
            if not parent:
                return None
            return Transform(parent)
        except:
            return None

    @property
    def childcount(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Transform__get_childCount(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_childCount'])
        except:
            return None
    
    @property
    def forward(self)-> _struct.Vec3|None:
        try:
            forward = _struct.Vec3()
            self._il2cpp._UnityEngine_Transform__get_forward(_ctypes.byref(forward), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_forward'])
            return forward
        except:
            return None
    
    @forward.setter
    def forward(self, pos:list|tuple|_struct.Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform__set_forward(self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Transform__set_forward'])
        except:
            pass

    @property
    def up(self)-> _struct.Vec3|None:
        try:
            up = _struct.Vec3()
            self._il2cpp._UnityEngine_Transform__get_up(_ctypes.byref(up), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_up'])
            return up
        except:
            return None
        
    @property
    def right(self)-> _struct.Vec3|None:
        try:
            right = _struct.Vec3()
            self._il2cpp._UnityEngine_Transform__get_right(_ctypes.byref(right), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform__get_right'])
            return right
        except:
            return None

    @property
    def eulerAngles(self)-> _struct.Vec3|None:
        try:
            angles = _struct.Vec3()
            self._il2cpp._UnityEngine_Transform_get_eulerAngles(_ctypes.byref(angles), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_eulerAngles'])
            return angles
        except:
            return None
    
    @eulerAngles.setter
    def eulerAngles(self, angles:list|tuple|_struct.Vec3):
        try:
            angles = self._il2cpp._vec3_helper(angles)
            if not angles:
                pass
            self._il2cpp._UnityEngine_Transform_set_eulerAngles(self.instance, _ctypes.pointer(angles), self._il2cpp._methodInfoData['_UnityEngine_Transform_set_eulerAngles'])
        except:
            pass

    @property
    def localPosition(self)-> _struct.Vec3|None:
        try:
            pos = _struct.Vec3()
            self._il2cpp._UnityEngine_Transform_get_localPosition(_ctypes.byref(pos), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_localPosition'])
            return pos
        except:
            return None
    
    @localPosition.setter
    def localPosition(self, pos:list|tuple|_struct.Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform_set_localPosition(self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Transform_set_localPosition'])
        except:
            pass

    @property
    def hasChanged(self)-> bool|None:
        try:
            return self._il2cpp._UnityEngine_Transform_get_hasChanged(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_hasChanged'])
        except:
            return None
    
    @hasChanged.setter
    def hasChanged(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Transform_set_hasChanged(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Transform_set_hasChanged'])
        except:
            pass


    @property
    def localScale(self)-> _struct.Vec3|None:
        try:
            scale = _struct.Vec3()
            self._il2cpp._UnityEngine_Transform_get_localScale(_ctypes.byref(scale), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_localScale'])
            return scale
        except:
            return None
    
    @localScale.setter
    def localScale(self, pos:list|tuple|_struct.Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform_set_localScale(self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Transform_set_localScale'])
        except:
            pass

    @property
    def localEulerAngles(self)-> _struct.Vec3|None:
        try:
            angles = _struct.Vec3()
            self._il2cpp._UnityEngine_Transform_get_localEulerAngles(_ctypes.byref(angles), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_localEulerAngles'])
            return angles
        except:
            return None
    
    @localEulerAngles.setter
    def localEulerAngles(self, pos:list|tuple|_struct.Vec3):
        try:
            pos = self._il2cpp._vec3_helper(pos)
            if not pos:
                pass
            self._il2cpp._UnityEngine_Transform_set_localEulerAngles(self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Transform_set_localEulerAngles'])
        except:
            pass

    @property
    def worldToLocalMatrix(self)-> _struct.Matrix4x4|None:
        try:
            matrix = _struct.Matrix4x4()
            self._il2cpp._UnityEngine_Transform_get_worldToLocalMatrix(_ctypes.byref(matrix), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_worldToLocalMatrix'])
            return matrix
        except:
            return None
        
    @property
    def localToWorldMatrix(self)-> _struct.Vec3|None:
        try:
            matrix = _struct.Matrix4x4()
            self._il2cpp._UnityEngine_Transform_get_localToWorldMatrix(_ctypes.byref(matrix), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Transform_get_localToWorldMatrix'])
            return matrix
        except:
            return None

    def IsChildOf(self, transform:Transform) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Transform__IsChildOf(self.instance, transform.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__IsChildOf'])
        except:
            return None
        
    def find(self, transform_str:str)-> Transform|None:
        try:
            found = self._il2cpp._UnityEngine_Transform__Find(self.instance, self._il2cpp._il2cpp_string_new(transform_str.encode()), self._il2cpp._methodInfoData['_UnityEngine_Transform__Find'])
            if not found:
                return None
            return Transform(self, found)
        except:
            return None
        
    def LookAt_pos(self, pos:list|tuple|_struct.Vec3, direction:list|tuple|_struct.Vec3) -> int|None:
        try:
            pos = self._il2cpp._vec3_helper(pos)
            direction = self._il2cpp._vec3_helper(direction)
            if not pos or not direction:
                return None
            self._il2cpp._UnityEngine_Transform__LookAt_pos(self.instance, _ctypes.pointer(pos), _ctypes.pointer(direction), self._il2cpp._methodInfoData['_UnityEngine_Transform__LookAt_pos'])
            return 1
        except:
            return None
        
    def LookAt_transform(self, transform:Transform) -> int|None:
        try:
            self._il2cpp._UnityEngine_Transform__LookAt_transform(self.instance, transform.ptr, self._il2cpp._methodInfoData['_UnityEngine_Transform__LookAt_transform'])
            return 1
        except:
            return None
        
    def translate(self, translation:list|tuple|_struct.Vec3, relativeTo:int) -> int|None:
        try:
            translation = self._il2cpp._vec3_helper(translation)
            if not translation:
                return None
            self._il2cpp._UnityEngine_Transform__translate(self.instance, _ctypes.pointer(translation), relativeTo, self._il2cpp._methodInfoData['_UnityEngine_Transform__translate'])
            return 1
        except:
            return None
        
    def GetChild(self, index:int) -> Transform|None:
        try:
            child = self._il2cpp._UnityEngine_Transform__GetChild(self.instance, index, self._il2cpp._methodInfoData['_UnityEngine_Transform__GetChild'])
            if not child:
                return None
            return Transform(child)
        except:
            return None
        
class Scene(_UnityObject):
    """
    Represents a collection of entities and components.
    
    To create your own Scene class simply get the address of the Scene object\n
    and then do Scene(address)
    """
    @property
    def name(self) -> str|None:
        try:
            name_addr = self._il2cpp._UnityEngine_Scene__get_name(_ctypes.byref(self.instance), self._il2cpp._methodInfoData['_UnityEngine_Scene__get_name'])
            return self._il2cpp.memory.read_unicode_string(name_addr + 0x14, self._il2cpp.memory.read_int(name_addr + 0x10) * 2)
        except:
            return None
    
    @property
    def path(self) -> str|None:
        try:
            name_addr = self._il2cpp._UnityEngine_Scene__get_path(_ctypes.byref(self.instance), self._il2cpp._methodInfoData['_UnityEngine_Scene__get_path'])
            return self._il2cpp.memory.read_unicode_string(name_addr + 0x14, self._il2cpp.memory.read_int(name_addr + 0x10) * 2)
        except:
            return None
    
    @property
    def rootCount(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_rootCount(_ctypes.byref(self.instance), self._il2cpp._methodInfoData['_UnityEngine_Scene__get_rootCount'])
        except:
            return None
        
    @property
    def loaded(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_isLoaded(_ctypes.byref(self.instance), self._il2cpp._methodInfoData['_UnityEngine_Scene__get_isLoaded'])
        except:
            return None
        
    def IsValid(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Scene__IsValid(_ctypes.byref(self.instance), self._il2cpp._methodInfoData['_UnityEngine_Scene__IsValid'])
        except:
            return None
    
    @property
    def guid(self) -> str|None:
        try:
            name_addr = self._il2cpp._UnityEngine_Scene__get_guid(_ctypes.byref(self.instance), self._il2cpp._methodInfoData['_UnityEngine_Scene__get_guid'])
            return self._il2cpp.memory.read_unicode_string(name_addr + 0x14, self._il2cpp.memory.read_int(name_addr + 0x10) * 2)
        except:
            return None
        
    @property
    def buildIndex(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_buildIndex(_ctypes.byref(self.instance), self._il2cpp._methodInfoData['_UnityEngine_Scene__get_buildIndex'])
        except:
            return None
        
    @property
    def handle(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Scene__get_handle(_ctypes.byref(self.instance), self._il2cpp._methodInfoData['_UnityEngine_Scene__get_handle'])
        except:
            return None
        
    

class Object(_UnityObject):
    """
    Base class for all engine objects.
    
    To create your own Object class simply get the address of the Object object\n
    and then do Object(address)

    Not all functions will work as expected because all GameObjects are objects but not all Objects are GameObjects
    """
    @property
    def name(self) -> str|None:
        try:
            name_addr = self._il2cpp._UnityEngine_Object__get_name(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Object__get_name'])
            return self._il2cpp.memory.read_unicode_string(name_addr + 0x14, self._il2cpp.memory.read_int(name_addr + 0x10) * 2)
        except:
            return None
    
    @name.setter
    def name(self, value:str):
        try:
            self._il2cpp._UnityEngine_Object__set_name(self.instance, self._il2cpp._il2cpp_string_new(value.encode()), self._il2cpp._methodInfoData['_UnityEngine_Object__set_name'])
        except:
            pass
    
    @property
    def isStatic(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_isStatic(self.instance, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_isStatic'])
        except:
            return None
        
    @property
    def layer(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_layer(self.instance, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_layer'])
        except:
            return None
        
    @layer.setter
    def layer(self, value:int):
        try:
            self._il2cpp._UnityEngine_GameObject__set_layer(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_GameObject__set_layer'])
        except:
            pass

    @property
    def transform(self)-> Transform|None:
        try:
            addr = self._il2cpp._UnityEngine_GameObject__get_transform(self.instance, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_transform'])
            if not addr:
                return None
            return Transform(addr)
        except:
            return None

    @property
    def tag(self) -> str|None:
        try:
            addr = self._il2cpp._UnityEngine_GameObject__get_tag(self.instance, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_tag'])
            return self._il2cpp.memory.read_unicode_string(addr + 0x14, self._il2cpp.memory.read_int(addr + 0x10) * 2)
        except:
            return None
    
    @tag.setter
    def tag(self, value:str):
        try:
            self._il2cpp._UnityEngine_GameObject__set_tag(self.instance, self._il2cpp._il2cpp_string_new(value.encode()), self._il2cpp._methodInfoData['_UnityEngine_GameObject__set_tag'])
        except:
            pass

    @property
    def hideFlags(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Object__get_hideFlags(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Object__get_hideFlags'])
        except:
            return None
    
    @hideFlags.setter
    def hideFlags(self, value:int):
        try:
            self._il2cpp._UnityEngine_Object__set_hideFlags(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Object__get_hideFlags'])
        except:
            pass

    @property
    def scene(self) -> Scene|None:
        try:
            addr = self._il2cpp._UnityEngine_GameObject__get_scene(self.instance, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_scene'])
            if not addr:
                return None
            return Scene(addr)
        except:
            return None
        
    @property
    def activeInHierarchy(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_activeInHierarchy(self.instance, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_activeInHierarchy'])
        except:
            return None

    @property
    def activeSelf(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_activeSelf(self.instance, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_activeSelf'])
        except:
            return None
        
    @property
    def sceneCullingMask(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_sceneCullingMask(self.instance, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_sceneCullingMask'])
        except:
            return None
        
    @property
    def active(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_GameObject__get_active(self.instance, self._il2cpp._methodInfoData['_UnityEngine_GameObject__get_active'])
        except:
            return None
    
    @active.setter
    def active(self, value:bool):
        try:
            self._il2cpp._UnityEngine_GameObject__set_active(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_GameObject__set_active'])
        except:
            pass
        
    def SetActive(self, value:bool) -> int|None:
        try:
            self._il2cpp._UnityEngine_GameObject__SetActive(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_GameObject__SetActive'])
            return 1
        except:
            return None

    def destroy(self) -> int|None:
        try:
            self._il2cpp._UnityEngine_Object__Destroy(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Object__Destroy'])
            return 1
        except:
            return None
    
    def GetComponent(self, type_object:int) -> Component|None:
        try:
            addr = self._il2cpp._UnityEngine_GameObject__GetComponent(self.instance, type_object, self._il2cpp._methodInfoData['_UnityEngine_GameObject__GetComponent'])
            if not addr:
                return None
            return Component(addr)
        except:
            return None
        
    def GetComponents(self) -> list[Component]|None:
        try:
            arr = self._il2cpp._UnityEngine_GameObject__GetComponents(self.instance, self._il2cpp._component.object, self._il2cpp._methodInfoData['_UnityEngine_GameObject__GetComponents'])
            components = [Component(i) for i in self._il2cpp._read_il2cpp_array(arr)]
            return components
        except:
            return None
        
    def AddComponent(self, type_object:int) -> int|None:
        try:
            self._il2cpp._UnityEngine_GameObject__AddComponent(self.instance, type_object, self._il2cpp._methodInfoData['_UnityEngine_GameObject__AddComponent'])
            return 1
        except:
            return None
        
    def Instantiate(self) -> Object|None:
        try:
            new_obj = self._il2cpp._UnityEngine_Object__Instantiate(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Object__Instantiate'])
            if not new_obj:
                return None
            return Object(new_obj)
        except:
            return None
        
    def MoveGameObjectToScene(self, scene:Scene) -> int|None:
        try:
            self._il2cpp._UnityEngine_SceneManager__MoveGameObjectToScene(self.instance, scene.handle, self._il2cpp._methodInfoData['_UnityEngine_SceneManager__MoveGameObjectToScene'])
            return 1
        except:
            return None
        
    def DontDestroyOnLoad(self) -> int|None:
        try:
            self._il2cpp._UnityEngine_Object__DontDestroyOnLoad(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Object__DontDestroyOnLoad'])
            return 1
        except:
            return None


class Camera(Component):
    """
    Defines a viewpoint into the scene.
    
    To create your own Camera class simply get the address of the Camera object\n
    and then do Camera(address)
    """
    @property
    def fov(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_fieldOfView(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_fieldOfView'])
        except:
            return None

    @fov.setter
    def fov(self, fov:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_fieldOfView(self.instance, _ctypes.c_float(fov), self._il2cpp._methodInfoData['_UnityEngine_Camera__set_fieldOfView'])
        except:
            pass
    
    @property
    def depth(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_depth(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_depth'])
        except:
            return None
    
    @depth.setter
    def depth(self, depth:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_depth(self.instance, _ctypes.c_float(depth), self._il2cpp._methodInfoData['_UnityEngine_Camera__set_depth'])
        except:
            pass

    @property
    def allowDynamicResolution(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_allowDynamicResolution(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_allowDynamicResolution'])
        except:
            return None
        

    @property
    def allowMSAA(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_allowMSAA(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_allowMSAA'])
        except:
            return None
    
    @allowMSAA.setter
    def allowMSAA(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Camera__set_allowMSAA(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_allowMSAA'])
        except:
            pass

    @property
    def allowHDR(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_allowHDR(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_allowHDR'])
        except:
            return None
    
    @allowHDR.setter
    def allowHDR(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Camera__set_allowHDR(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_allowHDR'])
        except:
            pass

    @property
    def aspect(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_aspect(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_aspect'])
        except:
            return None
    
    @aspect.setter
    def aspect(self, value:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_aspect(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_aspect'])
        except:
            pass

    @property
    def backgroundColor(self) -> _struct.Color|None:
        try:
            color = _struct.Color()
            self._il2cpp._UnityEngine_Camera__get_backgroundColor(_ctypes.byref(color), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_backgroundColor'])
            return color
        except:
            return None
    
    @backgroundColor.setter
    def backgroundColor(self, color:_struct.Color):
        try:
            self._il2cpp._UnityEngine_Camera__set_backgroundColor(self.instance, _ctypes.pointer(color), self._il2cpp._methodInfoData['_UnityEngine_Camera__set_backgroundColor'])
        except:
            pass
    
    @property
    def cameraToWorldMatrix(self) -> _struct.Matrix4x4|None:
        try:
            matrix = _struct.Matrix4x4()
            self._il2cpp._UnityEngine_Camera__get_cameraToWorldMatrix(_ctypes.byref(_struct.Matrix4x4), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_cameraToWorldMatrix'])
            return matrix
        except:
            return None

    @property
    def cameraType(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_cameraType(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_cameraType'])
        except:
            return None
    
    @cameraType.setter
    def cameraType(self, type_object:int):
        try:
            self._il2cpp._UnityEngine_Camera__set_cameraType(self.instance, type_object, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_cameraType'])
        except:
            pass

    @property
    def clearFlags(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_clearFlags(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_clearFlags'])
        except:
            return None
    
    @clearFlags.setter
    def clearFlags(self, value:int):
        try:
            self._il2cpp._UnityEngine_Camera__set_clearFlags(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_clearFlags'])
        except:
            pass

    @property
    def cullingMask(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_cullingMask(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_cullingMask'])
        except:
            return None
    
    @cullingMask.setter
    def cullingMask(self, value:int):
        try:
            self._il2cpp._UnityEngine_Camera__set_cullingMask(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_cullingMask'])
        except:
            pass

    @property
    def eventMask(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_eventMask(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_eventMask'])
        except:
            return None

    
    @property
    def farClipPlane(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_farClipPlane(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_farClipPlane'])
        except:
            return None
    
    @farClipPlane.setter
    def farClipPlane(self, value:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_farClipPlane(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_farClipPlane'])
        except:
            pass

    @property
    def nearClipPlane(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_nearClipPlane(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_nearClipPlane'])
        except:
            return None
    
    @nearClipPlane.setter
    def nearClipPlane(self, value:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_nearClipPlane(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_nearClipPlane'])
        except:
            pass

    @property
    def focalLength(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_focalLength(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_focalLength'])
        except:
            return None

    @property
    def gateFit(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_gateFit(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_gateFit'])
        except:
            return None
    
    @gateFit.setter
    def gateFit(self, value:int):
        try:
            self._il2cpp._UnityEngine_Camera__set_gateFit(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_gateFit'])
        except:
            pass

    @property
    def lensShift(self) -> _struct.Vec2|None:
        try:
            lens = _struct.Vec2()
            self._il2cpp._UnityEngine_Camera__get_lensShift(_ctypes.byref(lens), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_lensShift'])
            return lens
        except:
            return None
    
    @lensShift.setter
    def lensShift(self, value:list|tuple|_struct.Vec2):
        try:
            lens = self._il2cpp._vec2_helper(value)
            self._il2cpp._UnityEngine_Camera__set_lensShift(_ctypes.pointer(lens), self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_lensShift'])
        except:
            pass

    @property
    def orthographicSize(self) -> float|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_orthographicSize(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_orthographicSize'])
        except:
            return None
    
    @orthographicSize.setter
    def orthographicSize(self, value:float):
        try:
            self._il2cpp._UnityEngine_Camera__set_orthographicSize(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_orthographicSize'])
        except:
            pass

    @property
    def orthographic(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_orthographic(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_orthographic'])
        except:
            return None
    
    @orthographic.setter
    def orthographic(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Camera__set_orthographic(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_orthographic'])
        except:
            pass

    @property
    def pixelHeight(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_pixelHeight(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_pixelHeight'])
        except:
            return None
        
    @property
    def pixelWidth(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_pixelWidth(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_pixelWidth'])
        except:
            return None
        

    @property
    def pixelRect(self) -> _struct.Rect|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_pixelRect(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_pixelRect'])
        except:
            return None
    
    @pixelRect.setter
    def pixelRect(self, rect:list|tuple|_struct.Rect):
        try:
            rect = self._il2cpp._rect_helper(rect)
            self._il2cpp._UnityEngine_Camera__set_pixelRect(self.instance, _ctypes.pointer(rect), self._il2cpp._methodInfoData['_UnityEngine_Camera__set_pixelRect'])
        except:
            pass

    @property
    def targetDisplay(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_targetDisplay(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_targetDisplay'])
        except:
            return None
    
    @targetDisplay.setter
    def targetDisplay(self, value:int):
        try:
            self._il2cpp._UnityEngine_Camera__set_targetDisplay(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_targetDisplay'])
        except:
            pass

    @property
    def useOcclusionCulling(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_useOcclusionCulling(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_useOcclusionCulling'])
        except:
            return None
    
    @useOcclusionCulling.setter
    def useOcclusionCulling(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Camera__set_useOcclusionCulling(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_useOcclusionCulling'])
        except:
            pass

    @property
    def usePhysicalProperties(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Camera__get_usePhysicalProperties(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Camera__get_usePhysicalProperties'])
        except:
            return None
    
    @usePhysicalProperties.setter
    def usePhysicalProperties(self, value:bool):
        try:
            self._il2cpp._UnityEngine_Camera__set_usePhysicalProperties(self.instance, value, self._il2cpp._methodInfoData['_UnityEngine_Camera__set_usePhysicalProperties'])
        except:
            pass

    def ScreenPointToRay(self) -> _struct.Ray|None:
        try:
            ray = _struct.Ray()
            pos = _struct.Vec3()
            self._il2cpp._UnityEngine_Input__get_mousePosition(_ctypes.byref(pos), self._il2cpp._methodInfoData['_UnityEngine_Input__get_mousePosition'])
            self._il2cpp._UnityEngine_Camera__ScreenPointToRay(_ctypes.byref(ray), self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Camera__ScreenPointToRay'])
            return ray
        except:
            return None
        
    def ScreenToWorldPoint(self) -> _struct.Vec3|None:
        try:
            mouse_pos = _struct.Vec3()
            pos = _struct.Vec3()
            self._il2cpp._UnityEngine_Input__get_mousePosition(_ctypes.byref(mouse_pos), self._il2cpp._methodInfoData['_UnityEngine_Input__get_mousePosition'])
            self._il2cpp._UnityEngine_Camera__ScreenToWorldPoint(_ctypes.byref(pos), self.instance, _ctypes.pointer(mouse_pos), self._il2cpp._methodInfoData['_UnityEngine_Camera__ScreenToWorldPoint'])
            return pos
        except:
            return None
        
    def WorldToScreenPoint(self, pos:list|tuple|_struct.Vec3) -> _struct.Vec3|None:
        try:
            pos = self._il2cpp._vec3_helper(pos)
            screen_pos = _struct.Vec3()
            self._il2cpp._UnityEngine_Camera__WorldToScreenPoint(_ctypes.byref(screen_pos), self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Camera__WorldToScreenPoint'])
            return screen_pos
        except:
            return None


    def ScreenToViewportPoint(self, pos:list|tuple|_struct.Vec3) -> _struct.Vec3|None:
        try:
            pos = self._il2cpp._vec3_helper(pos)
            viewport_pos = _struct.Vec3()
            self._il2cpp._UnityEngine_Camera__ScreenToViewportPoint(_ctypes.byref(viewport_pos), self.instance, _ctypes.pointer(pos), self._il2cpp._methodInfoData['_UnityEngine_Camera__ScreenToViewportPoint'])
            return viewport_pos
        except:
            return None

class Collider(Component):
    """
    Represents a Collider class object.
    
    To create your own Collider class simply get the address of the Collider object\n
    and then do Collider(address)
    """
    @property
    def attachedRigidbody(self) -> Rigidbody|None:
        try:
            body = self._il2cpp._UnityEngine_Collider_get_attachedRigidbody(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Collider_get_attachedRigidbody'])
            if not body:
                return None
            return Rigidbody(body)
        except:
            return None
        
    @property
    def bounds(self) -> _struct.Bounds|None:
        try:
            return self._il2cpp._UnityEngine_Collider_get_bounds(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Collider_get_bounds'])
        except:
            return None
        
    @property
    def enabled(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Collider_get_enabled(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Collider_get_enabled'])
        except:
            return None
        
    @enabled.setter
    def enabled(self):
        try:
            self._il2cpp._UnityEngine_Collider_set_enabled(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Collider_set_enabled'])
        except:
            pass
        
    @property
    def isTrigger(self) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_Collider_get_isTrigger(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Collider_get_isTrigger'])
        except:
            return None
        
    @isTrigger.setter
    def isTrigger(self):
        try:
            self._il2cpp._UnityEngine_Collider_set_isTrigger(self.instance, self._il2cpp._methodInfoData['_UnityEngine_Collider_set_isTrigger'])
        except:
            pass

    def Raycast(self, ray:_struct.Ray, maxDistance:float) -> bool|_struct.RaycastHit|None:
        try:
            hitInfo = _struct.RaycastHit()
            result = self._il2cpp._UnityEngine_Collider_Raycast(self.instance, _ctypes.pointer(ray), _ctypes.byref(hitInfo), maxDistance, self._il2cpp._methodInfoData['_UnityEngine_Collider_Raycast'])
            if result:
                hitInfo.collider = self._il2cpp._UnityEngine_Object__FindObjectFromInstanceID(hitInfo.collider, self._il2cpp._methodInfoData['_UnityEngine_Object__FindObjectFromInstanceID'])
                return hitInfo
            return result
        except:
            return None
        

class SceneManager(_UnityObject):
    """
    Represents a SceneManager class object.
    
    All methods in this class are static so you can just do some_variable = SceneManager() and then call any function within this class
    """
    @property
    def sceneCount(self) -> int|None:
        try:
            return self._il2cpp._UnityEngine_SceneManager__get_sceneCount(self._il2cpp._methodInfoData['_UnityEngine_SceneManager__get_sceneCount'])
        except:
            return None

    def CreateScene(self, name:str) -> Scene|None:
        try:
            scene = self._il2cpp._UnityEngine_SceneManager__CreateScene(self._il2cpp._il2cpp_string_new(name.encode()), self._il2cpp._methodInfoData['_UnityEngine_SceneManager__CreateScene'])
            if scene:
                return Scene(scene)
            return None
        except:
            return None
        
    def GetActiveScene(self) -> Scene|None:
        try:
            scene = self._il2cpp._UnityEngine_SceneManager__GetActiveScene(self._il2cpp._methodInfoData['_UnityEngine_SceneManager__GetActiveScene'])
            if scene:
                return Scene(scene)
            return None
        except:
            return None
        
    def GetSceneAt(self, index:int) -> Scene|None:
        try:
            scene = self._il2cpp._UnityEngine_SceneManager__GetSceneAt(index, self._il2cpp._methodInfoData['_UnityEngine_SceneManager__GetSceneAt'])
            if scene:
                return Scene(scene)
            return None
        except:
            return None
        
    def GetSceneByName(self, name:str) -> Scene|None:
        try:
            scene = self._il2cpp._UnityEngine_SceneManager__GetSceneByName(self._il2cpp._il2cpp_string_new(name.encode()), self._il2cpp._methodInfoData['_UnityEngine_SceneManager__GetSceneByName'])
            if scene:
                return Scene(scene)
            return None
        except:
            return None
        
    def LoadScene(self, name:str) -> int|None:
        try:
            self._il2cpp._UnityEngine_SceneManager__LoadScene(self._il2cpp._il2cpp_string_new(name.encode()), self._il2cpp._methodInfoData['_UnityEngine_SceneManager__LoadScene'])
            return 1
        except:
            return None
        
    def SetActiveScene(self, scene:_struct.Scene) -> bool|None:
        try:
            return self._il2cpp._UnityEngine_SceneManager__SetActiveScene(_ctypes.byref(scene), self._il2cpp._methodInfoData['_UnityEngine_SceneManager__SetActiveScene'])
        except:
            return None