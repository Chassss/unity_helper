"""
Provides the main interface for interacting with the IL2CPP runtime.

This module exposes the Il2cpp class, which handles communication
with Unity-based applications, including memory access, and runtime interaction.
"""

import ctypes
from . import memory
from .mono import MonoClass, MonoMethod, MonoImage
from .objects import Camera, GameObject
from .bindings import Bindings
from .structures import Il2CppArray, Vec3, Il2CppAssembly, Quaternion, Color, Vec2, Rect
import threading

class Il2cpp(Bindings):
    """
    High-level wrapper for unity IL2CPP based games to be able to interact with its information.

    Args:
        warn_on_missing (bool): If True, emits a warning when a built in requested method is not found; if False, missing methods fail silently. Defaults to `True`.
        init_il2cpp (bool): If True, manually calls il2cpp_init to prevent crashing when attemping to call functions that rely on il2cpp to be initialized first (may break some games). Defaults to `True`.
        init_helpers (bool): If True, initializes helper functions like UnityEngine_Component__GetComponent which are used within ``objects.py`` module. Defaults to ``True``.
        game_assembly (str): Full path or name of the GameAssembly library to load. Defaults to ``'GameAssembly.dll'``.
    """
    inst = None
    def __init__(self, warn_on_missing:bool=True, init_il2cpp:bool=True, init_helpers:bool=True, game_assembly:str='GameAssembly.dll'):
        self.game_asm = ctypes.WinDLL(game_assembly)

        self.memory = memory
        self.warn_on_missing:bool = warn_on_missing
        self.init_il2cpp:bool = init_il2cpp
        self._tls = threading.local()
        self._tls.attached = None
        self._tls.thread_ptr = None
        self._tls.external_attach = None

        self._assembly_cache: dict[str, int] = {}
        self._methodInfoData: dict[str, int] = {}

        Il2cpp.inst = self
        self._initialize_internals()
        
        if init_helpers:
            self._initialize_class_bindings()

    def _get_domain_raw(self) -> int|None:
        dom = self._il2cpp_domain_get()
        return int(dom) if dom else None
        
    def _ensure_attached(self):
        """
        Attach current thread once.
        Safe to call repeatedly.
        """

        # already attached by us
        if getattr(self._tls, "attached", False):
            return self._tls.thread_ptr

        # already attached externally (Unity/game thread)
        current_thread = None

        if self._il2cpp_thread_current:
            try:
                current_thread = self._il2cpp_thread_current()
            except Exception:
                current_thread = None

        if current_thread:
            self._tls.attached = True
            self._tls.thread_ptr = current_thread
            self._tls.external_attach = True
            return current_thread

        # attach ourselves
        dom = self._get_domain_raw()
        if not dom:
            raise RuntimeError("il2cpp domain not available")

        thread_ptr = self._il2cpp_thread_attach(ctypes.c_void_p(dom))

        self._tls.attached = True
        self._tls.thread_ptr = thread_ptr
        self._tls.external_attach = False

        return thread_ptr
    
    def _detach_current_thread(self):
        """
        Detach only if WE attached it.
        """

        if not getattr(self._tls, "attached", False):
            return

        if getattr(self._tls, "external_attach", False):
            return

        try:
            if self._il2cpp_thread_detach:
                self._il2cpp_thread_detach(self._tls.thread_ptr)
        except Exception:
            pass

        self._tls.attached = False
        self._tls.thread_ptr = None

    def _read_il2cpp_array(self, arr_ptr) -> int|None:
        """
        Reserved for internal use by other classes
        """
        header = ctypes.cast(arr_ptr, ctypes.POINTER(Il2CppArray)).contents
        length = header.max_length

        base_addr = arr_ptr + ctypes.sizeof(Il2CppArray)
        elements = ctypes.cast(base_addr, ctypes.POINTER(ctypes.c_void_p))

        return [elements[i] for i in range(length)]
    
    def _vec3_helper(self, data):
        """
        Reserved for internal use by other classes
        """
        if isinstance(data, (list, tuple)):
            x,y,z = data
            data = Vec3(x,y,z)
        elif isinstance(data, (Vec3)):
            return data
        else:
            return None
        return data
    
    def _vec2_helper(self, data):
        """
        Reserved for internal use by other classes
        """
        if isinstance(data, (list, tuple)):
            x,y = data
            data = Vec2(x,y)
        elif isinstance(data, (Vec2)):
            return data
        else:
            return None
        return data
    
    def _quaternion_helper(self, data):
        """
        Reserved for internal use by other classes
        """
        if isinstance(data, (list, tuple)):
            x,y,z,w = data
            data = Quaternion(x,y,z,w)
        elif isinstance(data, (Quaternion)):
            return data
        else:
            return None
        return data
    
    def _color_helper(self, data):
        """
        Reserved for internal use by other classes
        """
        if isinstance(data, (list, tuple)):
            r,g,b,a = data
            data = Color(r,g,b,a)
        elif isinstance(data, (Color)):
            return data
        else:
            return None
        return data
    
    def _rect_helper(self, data):
        """
        Reserved for internal use by other classes
        """
        if isinstance(data, (list, tuple)):
            x,y,wdith,height = data
            data = Rect(x,y,wdith,height)
        elif isinstance(data, (Rect)):
            return data
        else:
            return None
        return data
    
    def get_assembly_from_name(self, assembly_name:str) -> MonoImage|None:
        """
        Retrieve a ``MonoImage`` object by its name.

        Args:
            assembly_name (str): Name of the assembly, e.g., ``'Assembly-CSharp.dll'``.

        Returns:
            MonoImage | None: The matching ``MonoImage`` if found, else ``None``.
        """
        if not assembly_name in self._assembly_cache:
            self.list_assemblies()
        
        return self._assembly_cache.get(assembly_name)
        
    def get_class_from_name(self, assembly_name:str, klass:str, cache:bool=True) -> MonoClass|None:
        """
        Retrieve a ``MonoClass`` object by its name.

        Args:
            assembly_name (str): Name of the assembly, e.g., ``'UnityEngine.PhysicsModule.dll'``.
            klass (str): Fully qualified type name, e.g. ``'UnityEngine.Collider'``.

        Returns:
            MonoClass | None: An object containing metadata about the class, including its methods, fields and properties if found else ``None``.
        """
        
        asm = self.get_assembly_from_name(assembly_name)
        
        if not asm:
            return None
        
        return asm.find_class(klass, cache)

    def find_method(self, assembly_name:str, klass:str, method_name:str, param_count:int|None = None, cache:bool = True) -> MonoMethod|None:
        """
        Retrieve a ``MonoMethod`` object given its name.

        Args:
            assembly_name (str): Name of the assembly, e.g., ``'UnityEngine.PhysicsModule.dll'``.
            klass (str): Fully qualified type name, e.g. ``'UnityEngine.Collider'``.
            method_name (str): Name of the method, e.g., ``'get_enabled'``.
            param_count (Optional[int], optional): Param count of the function, e.g., 5. Defaults to ``None``.
            cache (bool, optional): Whether to cache the ``MonoClass`` object for faster future lookups. Defaults to `True`.

        Returns:
            MonoMethod | None: An object representing the method and its metadata.
        """
        param_range = [param_count] if param_count is not None else range(0, 11)             

        cls = self.get_class_from_name(assembly_name, klass, cache)
        methods = cls.list_methods(cache)

        for method in methods:
            if method.name == method_name and method.param_count in param_range:
                return method

    def get_mainCamera(self) -> Camera|None:
        """
        Retreives the main Camera object.

        Returns:
            Camera | None: Main camera if available, otherwise ``None``.
        """
        try:
            addr = self._UnityEngine_Camera_get_main(self._methodInfoData['_UnityEngine_Camera_get_main'])
            if not addr:
                return None
            return Camera(addr)
        except:
            return None
    
    def get_currentCamera(self) -> Camera|None:
        """
        Retrieve the current camera object.

        Returns:
            Camera | None: Current camera if available, otherwise ``None``.
        """
        try:
            addr = self._UnityEngine_Camera_get_current(self._methodInfoData['_UnityEngine_Camera_get_current'])
            if not addr:
                return None
            return Camera(addr)
        except:
            return None
    
    def get_allCameras(self) -> list[Camera]|None:
        """
        Retrieve all active camera objects.

        Returns:
            list[Camera] | None: List of active cameras if found, otherwise ``None``.
        """
        try:
            arr = self._UnityEngine_Camera_get_allCameras(self._methodInfoData['_UnityEngine_Camera_get_allCameras'])
            cameras = [Camera(i) for i in self._read_il2cpp_array(arr) if i]
            return cameras
        except:
            return None
    
    def get_all_camerasCount(self) -> int|None:
        """
        Retrieve the number of active cameras.

        Returns:
            int | None: Number of active cameras, otherwise ``None``.
        """
        try:
            return self._UnityEngine_Camera_get_allCamerasCount(0, self._methodInfoData['_UnityEngine_Camera_get_allCamerasCount'])
        except:
            return None

    def find_object(self, object_str:str) -> GameObject|None:
        """
        Retrieve an game object by name.

        Args:
            object_str (str): GameObject name e.g., ``'Player'``.

        Returns:
            GameObject | None: Matching game object if found, otherwise ``None``.
        """
        try:
            obj = self._UnityEngine_GameObject__Find(self._il2cpp_string_new(object_str.encode()), self._methodInfoData['_UnityEngine_GameObject__Find'])
            if not obj:
                return None
            return GameObject(obj)
        except:
            return None
    
    def find_object_with_tag(self, tag_str:str) -> GameObject|None:
        """
        Retreives a object by tag

        Args:
            tag_str (str): GameObject name e.g., ``'Player'``.

        Returns:
            GameObject | None: Matching object if found, otherwise ``None``.
        """
        try:
            obj = self._UnityEngine_GameObject__FindGameObjectWithTag(self._il2cpp_string_new(tag_str.encode()), self._methodInfoData['_UnityEngine_GameObject__FindGameObjectWithTag'])
            if not obj:
                return None
            return GameObject(obj)
        except:
            return None
        
    def find_objects_with_tag(self, tag_str:str) -> list[GameObject]:
        """
        Retreives a list of objects based on the given name

        Args:
            tag_str (str): GameObject name e.g., 'Player'

        Returns:
            List[Ga,eObject]: A list containing object objects if found otherwise ``None``.
        """
        try:
            arr = self._UnityEngine_GameObject__FindGameObjectsWithTag(self._il2cpp_string_new(tag_str.encode()), self._methodInfoData['_UnityEngine_GameObject__FindGameObjectsWithTag'])
            objs = [GameObject(i) for i in self._read_il2cpp_array(arr) if i]
            return objs
        except:
            return None
        
    def list_classes_in_image(self, assembly_name:str, cache:bool=True) -> list[MonoClass]:
        """
        Retrieve all classes in an assembly image.

        Args:
            assembly_name (str): Assembly name e.g., ``'Assembly-CSharp.dll'``.
            cache (bool, optional): Whether to cache the ``MonoClass`` object for faster future lookups. Defaults to `True`.

        Returns:
            list[MonoClass]: List of ``MonoClass`` objects.
        """
        
        assembly = self.get_assembly_from_name(assembly_name)
        if not assembly:
            return []
        
        return assembly.list_classes(cache)
        
    def list_assemblies(self) -> list[MonoImage]:
        """
        Retrieves a list of assembly names.

        Returns:
            list[MonoImage]: List of ``MonoImage`` objects.
        """
        assemblies = []

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
            
            img = self._il2cpp_assembly_get_image(assembly).contents
            name = image.name.decode("utf-8", errors="ignore")
            file_name = self._il2cpp_image_get_filename(image)
            file_name = file_name.decode() if file_name else ""

            monoimage = MonoImage(self, assembly, img, name, file_name)

            if not name in self._assembly_cache:
                self._assembly_cache[name] = monoimage

            assemblies.append(monoimage)

        return assemblies
    
    def dump_methods(self, image:str) -> dict|None:
        """
        Dumps all methods in an image in the ``Il2cppDumper`` format

        Args:
            image (str): Name of the assembly, e.g., ``'UnityEngine.PhysicsModule.dll'``.

        Returns:
            dict[str, list] | None: Structured Il2cppDumper-style output or ``None`` if unavailable.
        """
        classes = self.list_classes_in_image(image)

        base_dict = {"ScriptMethod": [], "Addresses": []}

        if not classes:
            return None
        
        base = self.game_asm._handle

        if not base:
            return None

        for i in classes:
            methods = i.list_methods()
            for method in methods:
                base_dict['ScriptMethod'].append({"Address": method.address - base, "Name": f'{i.name.replace('.', '_')}$${method.name}', "Signature": method.signature})
                base_dict['Addresses'].append(method.address - base)

        return base_dict