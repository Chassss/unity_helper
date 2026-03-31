"""
Provides the main interface for interacting with the IL2CPP runtime.

This module exposes the Il2cpp class, which handles communication
with Unity-based applications, including memory access, and runtime interaction.
"""

import ctypes
from pylocalmem import Process
from contextlib import contextmanager
from .mono import MonoClass, MonoMethod
from .objects import Rigidbody, Camera, Object
from .bindings import Bindings
from .structures import Il2CppArray, Vec3, Il2CppAssembly, Quaternion


class Il2cpp(Bindings):
    inst = None
    def __init__(self, dll_name: str = "GameAssembly.dll"):
        self.game_asm = ctypes.WinDLL(dll_name)
        self.PROCESS = Process()
        
        Il2cpp.inst = self
        self._initialize()

    def _get_domain_raw(self) -> int|None:
        dom = self._il2cpp_domain_get()
        return int(dom) if dom else None
    
    
    @contextmanager
    def _attached_context(self):
        """
        Context manager that re-gets the domain, attaches a thread if the current thread is NOT already
        attached, yields, then detaches (only if we attached).
        This prevents detaching an already-attached (game) thread.
        """
        dom = self._get_domain_raw()
        if not dom:
            raise RuntimeError("il2cpp domain not available")

        
        current_thread = None
        if self._il2cpp_thread_current:
            try:
                current_thread = self._il2cpp_thread_current()
            except Exception:
                current_thread = None

        did_attach = False
        thread_ptr = None

        
        if current_thread:
            try:
                yield
            finally:
                pass
        else:
            
            thread_ptr = self._il2cpp_thread_attach(ctypes.c_void_p(dom))
            did_attach = True
            try:
                yield
            finally:
                if did_attach and self._il2cpp_thread_detach:
                    try:
                        self._il2cpp_thread_detach(thread_ptr)
                    except Exception:
                        
                        pass

    
    def __open_assembly(self, assembly_name:str) -> int|None:
        with self._attached_context():
            if assembly_name in self._assembly_cache:
                return self._assembly_cache[assembly_name]
            dom = self._get_domain_raw()
            asm = self._il2cpp_domain_assembly_open(ctypes.c_void_p(dom), assembly_name.encode())
            if not asm:
                return None
            self._assembly_cache[assembly_name] = int(asm)
            return int(asm)

    def __get_image_from_assembly(self, assembly_ptr: int) -> int|None:
        with self._attached_context():
            if assembly_ptr in self._image_cache:
                return self._image_cache[assembly_ptr]
            try:
                ptr = ctypes.cast(ctypes.c_void_p(assembly_ptr), ctypes.POINTER(ctypes.c_void_p))
                img = int(ptr[0])
            except Exception:
                return None
            self._image_cache[assembly_ptr] = img
            return img
        

    def _read_il2cpp_array(self, arr_ptr) -> int|None:
        header = ctypes.cast(arr_ptr, ctypes.POINTER(Il2CppArray)).contents
        length = header.max_length

        base_addr = arr_ptr + ctypes.sizeof(Il2CppArray)
        elements = ctypes.cast(base_addr, ctypes.POINTER(ctypes.c_void_p))

        return [elements[i] for i in range(length)]
    
    def _vec3_helper(self, data):
        if isinstance(data, (list, tuple)):
            x,y,z = data
            data = Vec3(x,y,z)
        elif isinstance(data, (Vec3)):
            return data
        else:
            return None
        return data
    
    def _quaternion_helper(self, data):
        if isinstance(data, (list, tuple)):
            x,y,z,w = data
            data = Quaternion(x,y,z,w)
        elif isinstance(data, (Quaternion)):
            return data
        else:
            return None
        return data
        
    def get_class_from_name(self, assembly_name:str, namespace:str, klass:str, cache:bool=True) -> MonoClass:
        """
        Retrieve a MonoClass object by its name.

        Args:
            assembly_name (str): Name of the assembly, e.g., 'UnityEngine.PhysicsModule.dll'.
            namespace (str): Namespace of the class, e.g., 'UnityEngine'.
            klass (str): Name of the class, e.g., 'Collider'.

        Returns:
            MonoClass: An object containing metadata about the class, including its methods, fields and properties.
        """
        if cache:
            if not self._class_cache:
                self.list_classes_in_image(assembly_name)
            name = ".".join(filter(None, [namespace, klass]))
            for i in self._class_cache:
                if i.name == name:
                    return i
        asm = self.__open_assembly(assembly_name)
        if not asm:
            return None
        img = self.__get_image_from_assembly(asm)
        if not img:
            return None

        with self._attached_context():
            cls = self._il2cpp_class_from_name(ctypes.c_void_p(img), namespace.encode(), klass.encode())
            if not cls:
                return None
            
            type_ = self._il2cpp_class_get_type(ctypes.c_void_p(cls))
            type_obj = self._il2cpp_type_get_object(type_)

            monoclass = MonoClass(self, int(cls), klass, type_obj, type_)
            if not any(i.name == monoclass.name and i.cls == monoclass.cls for i in self._class_cache):
                self._class_cache.append(monoclass)

            return monoclass

    def find_method(self, assembly_name:str, namespace:str, klass:str, method_name:str, param_count:int|None = None, cache:bool = True) -> MonoMethod:
        """
        Retrieve a MonoMethod object given its name.

        Args:
            assembly_name (str): Name of the assembly, e.g., 'UnityEngine.PhysicsModule.dll'.
            namespace (str): Namespace of the class, e.g., 'UnityEngine'.
            klass (str): Name of the class, e.g., 'Collider'.
            method_name (str): Name of the method, e.g., 'get_enabled'.
            param_count (Optional[int], optional): Param count of the function, e.g., 5. Defaults to None.
            cache (bool, optional): Whether to cache the MonoClass object for faster future lookups. Defaults to True.

        Returns:
            MonoMethod: An object containing metadata about the method.
        """
        param_range = [param_count] if param_count is not None else range(0, 11)
        
        if cache and self._class_cache:
            name = ".".join(filter(None, [namespace, klass]))
            for clazz in self._class_cache:
                if clazz.name == name:
                    for method in clazz.list_methods():
                        for count in param_range:
                            if method.name == method_name and method.param_count == count:
                                return method
                            

        cls = self.get_class_from_name(assembly_name, namespace, klass)
        methods = cls.list_methods()
        for method in methods:
            for count in param_range:
                if method.name == method_name and method.param_count == count:
                    return method 

    
    def get_RigidBody(self, this:int) -> Rigidbody:
        """
        Retreives a Rigidbody object given a valid object pointer.

        Args:
            this (int): Instance pointer e.g., 2155666249552

        Returns:
            Rigidbody: An object containing various methods of interacting with the rigidbody.
        """
        return Rigidbody(self._UnityEngine_Component__GetComponent(this, self._il2cpp_string_new(b"Rigidbody"), 0))


    def get_main_camera(self) -> Camera:
        """
        Retreives the main Camera object

        Returns:
            Camera: An object containing various methods and data for interacting with the camera
        """
        return Camera(self._UnityEngine_Camera_get_main(0))


    def find_object(self, object_str:str) -> Object:
        """
        Retreives a object based on the given name

        Args:
            object_str (str): Object name e.g., 'Player'

        Returns:
            Object: An object containing various methods and data for interacting with the object.
        """
        try:
            obj = self._UnityEngine_GameObject__Find(self._il2cpp_string_new(object_str.encode()), 0)
            if not obj:
                return None
            return Object(obj)
        except:
            return None
    
    def find_object_with_tag(self, tag_str:str) -> Object:
        """
        Retreives a object based on the given name

        Args:
            tag_str (str): Object name e.g., 'Player'

        Returns:
            Object: An object containing various methods and data for interacting with the object.
        """
        try:
            obj = self._UnityEngine_GameObject__FindGameObjectWithTag(self._il2cpp_string_new(tag_str.encode()), 0)
            if not obj:
                return None
            return Object(obj)
        except:
            return None
        
    def list_classes_in_image(self, assembly_name:str) -> list[MonoClass]:
        """
        Retrieves a List containing MonoClass objects of each class in an imagine

        Args:
            assembly_name (str): Name of the assembly, e.g., 'Assembly-CSharp.dll'.

        Returns:
            List[MonoClass]: A List containing MonoClass objects
        """
        asm_ptr = self.__open_assembly(assembly_name)
        if not asm_ptr:
            return []

        img_ptr = self.__get_image_from_assembly(asm_ptr)
        if not img_ptr:
            return []

        classes = []
        with self._attached_context():
            class_count = self._il2cpp_image_get_class_count(ctypes.c_void_p(img_ptr))
            for i in range(class_count):
                cls_ptr = self._il2cpp_image_get_class(ctypes.c_void_p(img_ptr), i)
                if not cls_ptr:
                    continue
                cls_namespace = self._il2cpp_class_get_namespace(ctypes.c_void_p(cls_ptr))
                cls_namespace = cls_namespace.decode() if cls_namespace else ""
                cls_name = self._il2cpp_class_get_name(ctypes.c_void_p(cls_ptr))
                cls_name = cls_name.decode() if cls_name else ""
                type_ = self._il2cpp_class_get_type(ctypes.c_void_p(cls_ptr))
                type_obj = self._il2cpp_type_get_object(type_)
                
                full_name = ".".join(filter(None, [cls_namespace, cls_name]))

                cls = MonoClass(self, cls_ptr, full_name, type_obj, type_)

                classes.append(cls)
                self._class_cache.append(cls)

        return classes
    
    def list_assemblies(self) -> list[str]:
        """
        Retrieves a list of assembly names.

        Returns:
            list[int]: List containing all the loaded assemblies names
        """
        assemblies = []

        with self._attached_context():
            domain = self._get_domain_raw()

            size = ctypes.c_size_t()
            assembly_array_ptr = self._il2cpp_domain_get_assemblies(
                ctypes.c_void_p(domain),
                ctypes.byref(size)
            )

            assembly_array = ctypes.cast(
                assembly_array_ptr,
                ctypes.POINTER(ctypes.POINTER(Il2CppAssembly))
            )

            for i in range(size.value):
                assembly_ptr = assembly_array[i]
                if not assembly_ptr:
                    continue

                assembly = assembly_ptr.contents
                if not assembly.image:
                    continue

                image = assembly.image.contents
                if not image.name:
                    continue

                name = image.name.decode("utf-8", errors="ignore")

                assemblies.append(name)

        return assemblies