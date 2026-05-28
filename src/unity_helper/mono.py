"""
Reserved for internal use only.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main import Il2cpp

import ctypes, struct, re
from .objects import Object, Component, GameObject, Transform
from .memory import get_pages, read_bytes, is_64bit
from .constants import FieldAttribute, MethodAttribute, TypeAttribute, TYPE_CTYPE_MAP, PYTHON_TO_CTYPES
from functools import cached_property


class AbstractClassInstantiationError(Exception):
    pass

class FieldReadonlyError(Exception):
    pass

class FieldConstError(Exception):
    pass

class _FieldAccessor:
    def __init__(self, mono_class):
        self._mono_class = mono_class

    def __getattr__(self, name) -> MonoField:
        field = self._mono_class.find_field(name)

        if field is None:
            raise AttributeError(name)

        return field


class _MethodAccessor:
    def __init__(self, mono_class):
        self._mono_class = mono_class

    def __getattr__(self, name) -> MonoMethod:
        method = self._mono_class.find_method(name)

        if method is None:
            raise AttributeError(name)

        return method


class MonoClass():
    def __init__(self, il2cpp, cls, name, flags, object, _type, is_static):
        self._il2cpp:Il2cpp = il2cpp
        self._cls:int = cls
        self._name:str = name
        self._flags:int = flags
        self._object:int = object
        self._type:int = _type
        self._is_static:bool = is_static
        self._methods:list[MonoMethod] = []
        self._fields:list[MonoField] = []
        self._instance:int = None

    @property
    def name(self) -> str:
        """
        Full name of the monoclass.
        """
        return self._name
    
    @property
    def object(self) -> int:
        """
        Class type object address in memory.
        """
        return self._object
    @property
    def type(self) -> int:
        """
        Class type address in memory.
        """
        return self._type
    
    @property
    def instance(self) -> int:
        """
        Class instance address.
        """
        return self._instance

    @instance.setter
    def instance(self, value:int):
        if not isinstance(value, int):
            raise TypeError("Instance must be an int")
        self._instance = value

    @property
    def cls(self):
        """
        Class metadata pointer.

        """
        return self._cls
    
    @property
    def field(self):
        """
        Provides attribute-style access to class fields.
        """

        return _FieldAccessor(self)
    
    @property
    def method(self):
        """
        Provides attribute-style access to class fields.
        """

        return _MethodAccessor(self)
    
    @property
    def is_static(self) -> bool:
        """
        If the class is a static class or a instance class.
        """
        return self._is_static
    
    @property
    def flags(self) -> int:
        """
        Bitmask of class attribute flags.
        """
        return self._flags
    
    @cached_property
    def traits(self) -> dict[str, bool]:
        """
        Class trait information.
        """
        def get(call, default=None):
            try:
                return call(self.cls)
            except Exception:
                return default

        return {
            "Enum": get(self._il2cpp._il2cpp_class_is_enum, False),
            "Interface": get(self._il2cpp._il2cpp_class_is_interface, False),
            "Abstract": get(self._il2cpp._il2cpp_class_is_abstract, False),
            "ValueType": get(self._il2cpp._il2cpp_class_is_valuetype, False),

            "Generic": get(self._il2cpp._il2cpp_class_is_generic, False),
            "Inflated": get(self._il2cpp._il2cpp_class_is_inflated, False),

            "DeclaringType": get(self._il2cpp._il2cpp_class_get_declaring_type, None),
        }
    
    @cached_property
    def attributes(self) -> dict[str, bool]:
        """
        Class attribute information.
        """
        return {i.name: i in self.flags for i in TypeAttribute}
    
    @property
    def parent(self) -> MonoClass:
        try:
            cls = self._il2cpp._il2cpp_class_get_parent(ctypes.c_void_p(self.cls))
            
            klass = self._il2cpp._il2cpp_class_get_name(ctypes.c_void_p(cls)).decode()
            type_ = self._il2cpp._il2cpp_class_get_type(ctypes.c_void_p(cls))
            type_obj = self._il2cpp._il2cpp_type_get_object(type_)
            flags = TypeAttribute(self._il2cpp._il2cpp_class_get_flags(cls))
            is_static = (TypeAttribute.ABSTRACT in flags) and (TypeAttribute.SEALED in flags)

            monoclass = MonoClass(self._il2cpp, int(cls), klass, flags, type_obj, type_, is_static)
        except:
            return None
        return monoclass

    def find_method(self, method_name:str, param_count:int=None, cache:bool=True) -> MonoMethod|None:
        """
        Retrieve a ``MonoMethod`` object given its name.

        Args:
            method_name (str): Name of the method, e.g., `'set_timeScale'`.
            param_count (Optional[int], optional): Param count of the function, e.g., ``5``. Defaults to ``None``.
            cache (bool, optional): Whether to cache the ``MonoClass`` object for faster future lookups. Defaults to ``True``.

        Returns:
            MonoMethod | None: An object representing the method and its metadata if found otherwise ``None``.
        """   
        methods = self.list_methods(cache)
        if methods:
            param_range = [param_count] if param_count is not None else range(0, 11)
            for count in param_range:
                for method in methods:
                    if method.name != method_name:
                        continue

                    if method.param_count == count:
                        return method

    def list_methods(self, cache=True) -> list[MonoMethod]|None:
        """
        Retrieve a list of ``MonoMethod`` objects.

        Args:
            cache (bool, optional): Whether to cache the ``MonoClass`` object for faster future lookups. Defaults to ``True``.

        Returns:
            list[MonoMethod]: A list containing ``MonoMethod`` objects.
        """   
        if cache and self._methods:
            return self._methods
        iterator = ctypes.c_void_p()
        while True:
            method = self._il2cpp._il2cpp_class_get_methods(ctypes.c_void_p(self.cls), ctypes.byref(iterator))
            if not method:
                break
            name_ptr = self._il2cpp._il2cpp_method_get_name(method)
            name = name_ptr.decode() if name_ptr else ""
            param_count = self._il2cpp._il2cpp_method_get_param_count(method)
            param_info = ' '.join([f'{self._il2cpp._il2cpp_type_get_name(self._il2cpp._il2cpp_method_get_param(method, i)).decode()} {self._il2cpp._il2cpp_method_get_param_name(method, i).decode()}' for i in range(param_count)]).replace('&', '*')

            return_value = self._il2cpp._il2cpp_type_get_name(self._il2cpp._il2cpp_method_get_return_type(method)).decode()
            signature = f'{return_value} {self.name.replace('.', '_')}__{name} ({self.name.replace('.', '_')}_o* __this {param_info} const MethoInfo* method);'
            flags = MethodAttribute(self._il2cpp._il2cpp_method_get_flags(method, 0))
            is_static = MethodAttribute.STATIC in flags
            
            method = MonoMethod(self, self._il2cpp, name, self._il2cpp.memory.read_longlong(method), int(method), param_count, param_info, signature, return_value, is_static, flags)
            if not any(i.name == method.name and i.address == method.address for i in self._methods):
                self._methods.append(method)


        return self._methods

    def find_field(self, field:str, cache=True) -> MonoField|None:
        """
        Retrieve a ``MonoField`` object given its name.

        Args:
            field (str): Name of the method, e.g., `'set_timeScale'`.
            
        Returns:
            MonoField | None: An object containing metadata about the method if found otherwise ``None``.
        """   
        for i in self.list_fields(cache):
            if i.name == field:
                return i

    def list_fields(self, cache=True) -> list[MonoField] | None:
        """
        Retrieve a list of ``MonoField`` objects, including inherited fields.

        Args:
            cache (bool, optional): Whether to cache the ``MonoClass`` object for faster future lookups. Defaults to ``True``.

        Returns:
            list[MonoField] | None: A list containing ``MonoField`` objects if found otherwise ``None``.
        """
        if cache and self._fields:
            return self._fields

        self._fields = []

        klass = ctypes.c_void_p(self.cls)

        while klass:
            iterator = ctypes.c_void_p()

            while True:
                field = self._il2cpp._il2cpp_class_get_fields(klass, ctypes.byref(iterator))
                if not field:
                    break

                name_ptr = self._il2cpp._il2cpp_field_get_name(field)
                name = name_ptr.decode() if name_ptr else ""
                type_ptr = self._il2cpp._il2cpp_field_get_type(field)
                type_name = (self._il2cpp._il2cpp_type_get_name(type_ptr).decode() if type_ptr else "")
                flags = FieldAttribute(self._il2cpp._il2cpp_field_get_flags(field))
                is_static = FieldAttribute.STATIC in flags
                monofield = MonoField(self, self._il2cpp, name, int(field), type_name, is_static, flags)

                if not any(i.name == monofield.name for i in self._fields):
                    self._fields.append(monofield)

            # move to parent class because classes can inherit fields from parents
            klass = self._il2cpp._il2cpp_class_get_parent(klass)

        return self._fields
    

    def find_object_of_type(self, includeInactive=False) -> Object|GameObject|Component|Transform|None:
        """
        Retreives a object baed on the current objects type.

        Args:
            includeInactive (bool): Whether to include incative objects.

        Returns:
            Object | GameObject| Component| None: A class object containing various methods and data for interacting with the object if found otherwise ``None``.
        """
        try:
            obj = self._il2cpp._UnityEngine_Object__FindObjectOfType(self.object, includeInactive, self._il2cpp._methodInfoData['_UnityEngine_Object__FindObjectOfType'])
            klass = self
            while klass:
                if klass.name == 'Component':
                    return Component(obj)
                elif klass.name == 'Object':
                    return Object(obj)
                elif klass.name == 'GameObject':
                    return GameObject(obj)
                elif klass.name == 'Transform':
                    return Transform(obj)

                klass = klass.parent
        except:
            return None

    def find_objects_of_type(self, includeInactive=False) -> list[Object|GameObject|Component|Transform]:
        """
        Retrieves all objects matching the current object's type.

        Args:
            includeInactive (bool): Whether to include incative objects.

        Returns:
            list[Object | GameObject| Component]  | None: A list containing class objects.
        """
        try:
            arr = self._il2cpp._UnityEngine_Object__FindObjectsOfType(self.object, includeInactive, self._il2cpp._methodInfoData['_UnityEngine_Object__FindObjectsOfType'])
            
            objects = [i for i in self._il2cpp._read_il2cpp_array(arr)]
            klass = self
            while klass:
                if klass.name == 'Component':
                    return [Component(i) for i in objects]
                elif klass.name == 'Object':
                    return [Object(i) for i in objects]
                elif klass.name == 'GameObject':
                    return [GameObject(i) for i in objects]
                elif klass.name == 'Transform':
                    return [Transform(i) for i in objects]

                klass = klass.parent
                
            return objects
        except:
            return objects
        
    
    def Instantiate(self) -> GameObject|None:
        """
        Creates a new instance of the specified class.

        Raises:
            AbstractClassInstantiationError:
                If the class is abstract.

        Returns:
            GameObject|None: The created object if successful, otherwise ``None``.
        """
        if self.attributes.get("ABSTRACT"):
            raise AbstractClassInstantiationError(f"Cannot instantiate abstract class '{self.name}'")
        try:
        
            obj = self._il2cpp._il2cpp_object_new(self.cls)
            
            ctor = self._il2cpp._il2cpp_class_get_method_from_name(self.cls, b'.ctor', 0)

            if not ctor:
                return None
            
            exc = ctypes.c_void_p()
            self._il2cpp._il2cpp_runtime_invoke(ctor, obj, None, ctypes.byref(exc))
            
            if obj:
                return GameObject(obj)
            
            return None
        except:
            return None

    def get_instance_addresses(self) -> list[int]:
        """
        Retrieves instance addresses by scanning allocated memory.

        Returns:
            list[int]: A list of instance addresses.
        """
        fmt = "<Q" if is_64bit() else "<I"
        target_bytes = struct.pack(fmt, self.cls)
        pattern = re.compile(re.escape(target_bytes))

        found = []
        pages = get_pages()

        for base, size in pages:
            if size < len(target_bytes):
                continue

            data = read_bytes(base, size)
            if not data:
                continue
            
            for match in pattern.finditer(data):
                found.append(base + match.start())

        return found


class MonoMethod():
    def __init__(self, owner, il2cpp, name, address, methodInfo, param_count, param_info, signature, return_value, is_static, flags):
        self._il2cpp:Il2cpp = il2cpp
        self._klass:MonoClass = owner
        self._name:str = name
        self._address:int = address
        self._methodInfo:int = methodInfo
        self._param_count:int = param_count
        self._param_info:list = param_info
        self._signature:str = signature
        self._return_value:str = return_value
        self._is_static:bool = is_static
        self._flags:int = flags

    @property
    def name(self) -> str:
        """
        Name of the method.
        """
        return self._name
    @property
    def address(self) -> int:
        """
        Address of the method in memory.
        """
        return self._address
    @property
    def methodInfo(self) -> int:
        """
        Address of the methodInfo object in memory.
        """
        return self._methodInfo
    @property
    def param_count(self) -> int:
        """
        Amount of parameters passed into the method.
        """
        return self._param_count
    @property
    def param_info(self) -> str:
        """
        Information about the passed in parameters if any.
        """
        return self._param_info
    @property
    def signature(self) -> str:
        """
        Full signature of the function.
        """
        return self._signature
    @property
    def return_value(self) -> str:
        """
        Information about the return value of the method.
        """
        return self._return_value
    @property
    def is_static(self) -> bool:
        """
        If the method is a static method or a instance method.
        """
        return self._is_static
    
    @property
    def flags(self) -> int:
        """
        Bitmask of method attribute flags.
        """
        return self._flags
    
    @property
    def instance(self) -> int:
        """
        Parent class instance address.
        """
        return self.klass.instance
    
    @instance.setter
    def instance(self, value:int):
        if not isinstance(value, int):
            raise TypeError("instance must be an int")
        self.klass.instance = value

    @property
    def klass(self) -> MonoClass:
        """
        Method parent class.
        """
        return self._klass

    @cached_property
    def traits(self) -> dict[str, bool]:
        """
        Method trait information.
        """
        def get(call, default=None):
            try:
                return call(self.methodInfo)
            except Exception:
                return default
            
        return {
            "Instance": get(self._il2cpp._il2cpp_method_is_instance, False),
            "Generic": get(self._il2cpp._il2cpp_method_is_generic, False),
            "Inflated": get(self._il2cpp._il2cpp_method_is_inflated, False),
        }

    @cached_property
    def attributes(self) -> dict[str, bool]:
        """
        Method attribute information.
        """
        return {i.name: i in self.flags for i in MethodAttribute}

    def __call__(self, *args) -> int|ctypes._SimpleCData|None:
        argc = len(args)
        
        c_args = (ctypes.c_void_p * max(1, argc))()
        for i, v in enumerate(args):
            if not isinstance(v, ctypes.c_void_p):
                if isinstance(v, str):
                    v = self._il2cpp._il2cpp_string_new(v.encode())
                    c_args[i] = ctypes.cast(v, ctypes.c_void_p)
                else:
                    v = PYTHON_TO_CTYPES.get(type(v), lambda x: x)(v)
                    c_args[i] = ctypes.cast(ctypes.pointer(v), ctypes.c_void_p)
            else:
                c_args[i] = v
            

        exc = ctypes.c_void_p()
        ret = self._il2cpp._il2cpp_runtime_invoke(ctypes.c_void_p(self.methodInfo), ctypes.c_void_p(self.instance), c_args if argc else None, ctypes.byref(exc))

        if not ret:
            return None

        if isinstance(ret, ctypes.c_void_p):
            raw_ptr = ret
        elif hasattr(ret, "value"):
            raw_ptr = ctypes.c_void_p(ret.value)
        elif isinstance(ret, int):
            raw_ptr = ctypes.c_void_p(ret)
        else:
            raw_ptr = ctypes.cast(ret, ctypes.c_void_p)

        type_ = TYPE_CTYPE_MAP.get(self.return_value)

        if type_ is None:
            return raw_ptr

        unboxed = None
        try:
            unboxed = self._il2cpp._il2cpp_object_unbox(raw_ptr)
        except:
            unboxed = None

        if unboxed:
            val = ctypes.cast(unboxed, ctypes.POINTER(type_)).contents
            if hasattr(val, "value"):
                return val.value
            return val

        try:
            val = ctypes.cast(raw_ptr, ctypes.POINTER(type_)).contents
            if hasattr(val, "value"):
                return val.value
            return val
        except:
            pass

        return raw_ptr
        

    def native_patch(self, code:str|bytes, offset:int=0) -> bool|None:
        """
        Writes bytes at the function and given offset

        Args:
            code (str | bytes): Data to be written e.g., ``'mov al,01;ret'`` or ``b'\\xb0\\x01\\xc3'``.
            offset (int, optional): Offset at which the code will be written to. Defaults to ``0``.

        Returns:
            If the function succeeds the value is ``True`` otherwise ``None`` 
        """
        try:
            if isinstance(code, str):
                code = self._il2cpp.memory.assemble(code)
            return self._il2cpp.memory.write_bytes(self.address + offset, code)
        except:
            return None
        
class MonoField():
    def __init__(self, owner, il2cpp, name, ptr, type_name, is_static, flags):
        self._klass:MonoClass = owner
        self._il2cpp:Il2cpp = il2cpp
        self._name:str = name
        self._ptr:int = ptr
        self._type:str = type_name
        self._is_static:bool = is_static
        self._flags:int = flags

    @property
    def name(self) -> str:
        """
        Name of the field.
        """
        return self._name
    @property
    def ptr(self) -> int:
        """
        Pointer to the IL2CPP field metadata.
        """
        return self._ptr
    @property
    def type(self) -> str:
        """
        Unity type of the field.
        """
        return self._type
    @property
    def is_static(self) -> bool:
        """
        If the field is a static field or a instance field.
        """
        return self._is_static
    
    @property
    def instance(self) -> int:
        """
        Parent class instance address.
        """
        return self.klass.instance

    @instance.setter
    def instance(self, value:int):
        if not isinstance(value, int):
            raise TypeError("instance must be an int")
        self.klass.instance = value
    
    @property
    def flags(self) -> int:
        """
        Bitmask of field attribute flags.
        """
        return self._flags
    
    @cached_property
    def attributes(self) -> dict[str, bool]:
        """
        Field attribute information.
        """
        return {i.name: i in self.flags for i in FieldAttribute}
        
    @property
    def offset(self) -> int:
        """
        Field offset in the class.
        """
        return self._il2cpp._il2cpp_field_get_offset(self.ptr)
    
    @property
    def klass(self) -> MonoClass:
        """
        Field parent class.
        """
        return self._klass
    
    @property
    def address(self) -> int:
        """
        Field address in memory.
        """
        if self.is_static:
            if self.offset:
                return self._il2cpp.memory.read_longlong(self.klass.cls + 0xB8) + self.offset
            else:
                addr = self._il2cpp.memory.read_longlong(self.klass.cls + 0xB8)
                value = self._il2cpp.memory.read_ctype(addr, self.__get_type(self.type)())
                if value == self.value:
                    return addr

                return None

        if not self.instance:
            raise RuntimeError("Non-static field access requires an instance")

        return self.instance + self.offset
    
    @property
    def value(self):
        """
        Current value of the field.
        """
        if not self.instance and not self.is_static:
            raise RuntimeError("Non-static field access requires an instance")

        buf = (ctypes.c_byte * 8)()

        if self.is_static:
            if self.name.startswith('<>'):
                return None
            self._il2cpp._il2cpp_field_static_get_value(ctypes.c_void_p(self.ptr), ctypes.byref(buf))
        else:
            self._il2cpp._il2cpp_field_get_value(ctypes.c_void_p(self.instance), ctypes.c_void_p(self.ptr), ctypes.byref(buf))

        type_ptr = self._il2cpp._il2cpp_field_get_type(ctypes.c_void_p(self.ptr))
        type_name = self._il2cpp._il2cpp_type_get_name(type_ptr).decode() if type_ptr else ""

        raw = ctypes.addressof(buf)

        return ctypes.cast(raw, ctypes.POINTER(self.__get_type(type_name)))[0]

    @value.setter
    def value(self, value):
        if not self.instance and not self.is_static:
            raise RuntimeError("Non-static field access requires an instance")

        type_ptr = self._il2cpp._il2cpp_field_get_type(ctypes.c_void_p(self.ptr))
        type_name = self._il2cpp._il2cpp_type_get_name(type_ptr).decode() if type_ptr else ""

        if self.attributes.get('LITERAL'):
            raise FieldConstError("Unable to set a const fields value.")

        elif self.attributes.get('INIT_ONLY'):
            raise FieldReadonlyError("Unable to set a readonly fields value.")
        
        if not isinstance(value, ctypes._SimpleCData):
            value = self.__get_type(type_name)(value)
        
        if self.is_static:
            self._il2cpp._il2cpp_field_static_set_value(ctypes.c_void_p(self.ptr), value)
        
        else:
            self._il2cpp._il2cpp_field_set_value(ctypes.c_void_p(self.instance), ctypes.c_void_p(self.ptr), ctypes.byref(value))
            
    def __get_type(self, type_name) -> ctypes._SimpleCData|None:
        try:
            ret = TYPE_CTYPE_MAP.get(type_name)
            if not ret:
                ret = ctypes.c_void_p

            return ret
        except:
            return ctypes.c_void_p # extra safety measures although it shouldnt error out either way