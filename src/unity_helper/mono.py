"""
Reserved for internal use only.

"""


import ctypes, struct, re
from .objects import Object
from .memory import get_pages, read_bytes, is_64bit
from .constants import FieldAttribute, MethodAttribute, TypeAttribute, TYPE_CTYPE_MAP
from functools import cached_property


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
        self._il2cpp:int = il2cpp
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

    def find_method(self, method_name:str, param_count:int=None, cache:bool=True) -> MonoMethod|None:
        """
        Retrieve a MonoMethod object given its name.

        Args:
            method_name (str): Name of the method, e.g., 'set_timeScale'.
            param_count (Optional[int], optional): Param count of the function, e.g., 5. Defaults to None.
            cache (bool, optional): Whether to cache the MonoClass object for faster future lookups. Defaults to True.

        Returns:
            MonoMethod: An object containing metadata about the method.
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
        Retrieve a list of MonoMethod objects.

        Args:
            cache (bool, optional): Whether to cache the MonoClass object for faster future lookups. Defaults to True.

        Returns:
            list[MonoMethod]: A list containing MonoMethod objects.
        """   
        if cache and self._methods:
            return self._methods
        iterator = ctypes.c_void_p()
        with self._il2cpp._attached_context():
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
        Retrieve a MonoField object given its name.

        Args:
            field (str): Name of the method, e.g., 'set_timeScale'.
            
        Returns:
            MonoField: An object containing metadata about the method.
        """   
        for i in self.list_fields(cache):
            if i.name == field:
                return i

    def list_fields(self, cache=True) -> list[MonoField] | None:
        """
        Retrieve a list of MonoField objects, including inherited fields.
        """
        if cache and self._fields:
            return self._fields

        self._fields = []

        with self._il2cpp._attached_context():
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
    

    def findObject_of_type(self, includeInactive=False) -> Object|None:
        """
        Retreives a object baed on the current objects type.

        Args:
            includeInactive (bool): Whether to include incative objects.

        Returns:
            Object: An object containing various methods and data for interacting with the object.
        """
        try:
            return Object(self._il2cpp._UnityEngineObject__FindObjectOfType(self.object, includeInactive, self._il2cpp._methodInfoData['_UnityEngineObject__FindObjectOfType']))
        except:
            return None

    def findObjects_of_type(self, includeInactive=False) -> list[Object]|None:
        """
        Retreives a object baed on the current objects type.

        Args:
            includeInactive (bool): Whether to include incative objects.

        Returns:
            list[Object]: A list containing Object objects.
        """
        try:
            arr = self._il2cpp._UnityEngineObject__FindObjectsOfType(self.object, includeInactive, self._il2cpp._methodInfoData['_UnityEngineObject__FindObjectsOfType'])
            objects = [Object(i) for i in self._il2cpp._read_il2cpp_array(arr)]
            return objects
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
        self._il2cpp = il2cpp
        self.__owner = owner
        self._name = name
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
        Actual address of the method in memory.
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
        return self.__owner.instance
    
    @instance.setter
    def instance(self, value:int):
        if not isinstance(value, int):
            raise TypeError("instance must be an int")
        self.__owner.instance = value

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
        with self._il2cpp._attached_context():
            argc = len(args)

            c_args = (ctypes.c_void_p * max(1, argc))()
            for i, v in enumerate(args):
                if isinstance(v, ctypes.c_void_p):
                    c_args[i] = v
                else:
                    c_args[i] = ctypes.cast(ctypes.pointer(v), ctypes.c_void_p)

            instance = self.__owner.instance
            if instance:
                if isinstance(instance, ctypes.c_void_p):
                    instance_ptr = instance
                elif isinstance(instance, int):
                    instance_ptr = ctypes.c_void_p(instance)
                else:
                    instance_ptr = ctypes.cast(instance, ctypes.c_void_p)
            else:
                instance_ptr = None

            exc = ctypes.c_void_p()
            ret = self._il2cpp._il2cpp_runtime_invoke(
                ctypes.c_void_p(self.methodInfo),
                instance_ptr,
                c_args if argc else None,
                ctypes.byref(exc)
            )

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
                unboxed = self._il2cpp._il2cppObject_unbox(raw_ptr)
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
            code (str | bytes): Data to be written e.g., 'mov al,01;ret' or b'\xb0\x01\xc3' 
            offset (int, optional): Offset at which the code will be written to. Defaults to 0.

        Returns:
            If the function succeeds the value is True otherwise its None 
        """
        try:
            if isinstance(code, str):
                code = self._il2cpp.memory.assemble(code)
            return self._il2cpp.memory.write_bytes(self.address + offset, code)
        except:
            return None
        
class MonoField():
    def __init__(self, owner, il2cpp, name, ptr, type_name, is_static, flags):
        self.__owner = owner
        self._il2cpp = il2cpp
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
        Address of the field in memory.
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
        return self.__owner.instance
    
    @instance.setter
    def instance(self, value:int):
        if not isinstance(value, int):
            raise TypeError("instance must be an int")
        self.__owner.instance = value
    
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
    def value(self):
        """
        Current value of the field
        """
        if not self.instance and not self.is_static:
            raise RuntimeError("Non-static field access requires an instance")

        with self._il2cpp._attached_context():

            buf = (ctypes.c_byte * 8)()

            if self.is_static:
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

        with self._il2cpp._attached_context():
            type_ptr = self._il2cpp._il2cpp_field_get_type(ctypes.c_void_p(self.ptr))
            type_name = self._il2cpp._il2cpp_type_get_name(type_ptr).decode() if type_ptr else ""

            cval = self.__get_type(type_name)(value)
            if self.is_static:
                self._il2cpp._il2cpp_field_static_set_value(ctypes.c_void_p(self.ptr), ctypes.byref(cval))
            
            else:
                self._il2cpp._il2cpp_field_set_value(ctypes.c_void_p(self.instance), ctypes.c_void_p(self.ptr), ctypes.byref(cval))


    @cached_property
    def attributes(self) -> dict[str, bool]:
        """
        Field attribute information.
        """
        return {i.name: i in self.flags for i in FieldAttribute}
            
    def __get_type(self, type_name) -> ctypes._SimpleCData|None:
        try:
            ret = TYPE_CTYPE_MAP.get(type_name)
            if not ret:
                ret = ctypes.c_void_p

            return ret
        except:
            return ctypes.c_void_p # extra safety measures although it shouldnt error out either way