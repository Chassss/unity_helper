"""
Reserved for internal use only.

"""

import ctypes
from .structures import Vec3, Quaternion, Il2CppAssembly
from.mono import MonoClass


class Bindings():
    def __DO_API(self, api, argtypes, restype):
        try:
            new_api = api
            new_api.argtypes = argtypes
            new_api.restype = restype
            return new_api
        except:
            return None
        
    def __find_method(self, unity_obj, method):
        try:
            return unity_obj.find_method(method).address
        except Exception as e:
            print(f"Failed to find: {method} some built in features wont work")

    def _initialize(self):
        self._il2cpp_domain_get = self.__DO_API(self.game_asm.il2cpp_domain_get, [], ctypes.c_void_p)
        self._il2cpp_thread_attach = self.__DO_API(self.game_asm.il2cpp_thread_attach, [ctypes.c_void_p], ctypes.c_void_p)
        self._il2cpp_thread_current = self.__DO_API(self.game_asm.il2cpp_thread_current, [], ctypes.c_void_p)
        self._il2cpp_thread_detach = self.__DO_API(self.game_asm.il2cpp_thread_detach, [ctypes.c_void_p], None)
        self._il2cpp_domain_assembly_open = self.__DO_API(self.game_asm.il2cpp_domain_assembly_open, [ctypes.c_void_p, ctypes.c_char_p], ctypes.c_void_p)
        self._il2cpp_class_from_name = self.__DO_API(self.game_asm.il2cpp_class_from_name, [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p], ctypes.c_void_p)
        self._il2cpp_class_get_methods = self.__DO_API(self.game_asm.il2cpp_class_get_methods, [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)], ctypes.c_void_p)
        self._il2cpp_class_get_method_from_name = self.__DO_API(self.game_asm.il2cpp_class_get_method_from_name, [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int], ctypes.c_void_p)
        self._il2cpp_method_get_name = self.__DO_API(self.game_asm.il2cpp_method_get_name, [ctypes.c_void_p], ctypes.c_char_p)
        self._il2cpp_method_get_param_count = self.__DO_API(self.game_asm.il2cpp_method_get_param_count, [ctypes.c_void_p], ctypes.c_int)
        self._il2cpp_method_get_param = self.__DO_API(self.game_asm.il2cpp_method_get_param, [ctypes.c_void_p, ctypes.c_void_p], ctypes.c_void_p)
        self._il2cpp_runtime_invoke = self.__DO_API(self.game_asm.il2cpp_runtime_invoke, [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p)], ctypes.c_void_p)
        self._il2cpp_class_get_fields = self.__DO_API(self.game_asm.il2cpp_class_get_fields, [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)], ctypes.c_void_p)
        self._il2cpp_field_get_name = self.__DO_API(self.game_asm.il2cpp_field_get_name, [ctypes.c_void_p], ctypes.c_char_p)
        self._il2cpp_field_get_type = self.__DO_API(self.game_asm.il2cpp_field_get_type, [ctypes.c_void_p], ctypes.c_void_p)
        self._il2cpp_type_get_name = self.__DO_API(self.game_asm.il2cpp_type_get_name, [ctypes.c_void_p], ctypes.c_char_p)
        self._il2cpp_field_get_offset = self.__DO_API(self.game_asm.il2cpp_field_get_offset, [ctypes.c_void_p], ctypes.c_int)
        self._il2cpp_field_get_value = self.__DO_API(self.game_asm.il2cpp_field_get_value, [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p], None)
        self._il2cpp_image_get_class = self.__DO_API(self.game_asm.il2cpp_image_get_class, [ctypes.c_void_p, ctypes.c_int], ctypes.c_void_p)
        self._il2cpp_image_get_class_count = self.__DO_API(self.game_asm.il2cpp_image_get_class_count, [ctypes.c_void_p], ctypes.c_int)
        self._il2cpp_class_get_namespace = self.__DO_API(self.game_asm.il2cpp_class_get_namespace, [ctypes.c_void_p], ctypes.c_char_p)
        self._il2cpp_class_get_name = self.__DO_API(self.game_asm.il2cpp_class_get_name, [ctypes.c_void_p], ctypes.c_char_p)
        self._il2cpp_field_static_get_value = self.__DO_API(self.game_asm.il2cpp_field_static_get_value, [ctypes.c_void_p, ctypes.c_void_p], None)
        self._il2cpp_field_get_flags = self.__DO_API(self.game_asm.il2cpp_field_get_flags, [ctypes.c_void_p], ctypes.c_int)
        self._il2cpp_field_set_value = self.__DO_API(self.game_asm.il2cpp_field_set_value, [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p], None)
        self._il2cpp_object_unbox = self.__DO_API(self.game_asm.il2cpp_object_unbox, [ctypes.c_void_p], ctypes.c_void_p)
        self._il2cpp_type_get_object = self.__DO_API(self.game_asm.il2cpp_type_get_object, [ctypes.c_void_p], ctypes.c_void_p)
        self._il2cpp_class_get_type = self.__DO_API(self.game_asm.il2cpp_class_get_type, [ctypes.c_void_p], ctypes.c_void_p)
        self._il2cpp_object_get_class = self.__DO_API(self.game_asm.il2cpp_object_get_class, [ctypes.c_void_p], ctypes.c_void_p)
        self._il2cpp_string_new = self.__DO_API(self.game_asm.il2cpp_string_new, [ctypes.c_char_p], ctypes.c_void_p)
        self._il2cpp_method_get_return_type = self.__DO_API(self.game_asm.il2cpp_method_get_return_type, [ctypes.c_void_p], ctypes.c_void_p)
        self._il2cpp_method_get_flags = self.__DO_API(self.game_asm.il2cpp_method_get_flags, [ctypes.c_void_p, ctypes.c_int32], ctypes.c_int32)
        self._il2cpp_class_get_field_from_name = self.__DO_API(self.game_asm.il2cpp_class_get_field_from_name, [ctypes.c_void_p, ctypes.c_char_p], ctypes.c_void_p)
        self._il2cpp_domain_get_assemblies = self.__DO_API(self.game_asm.il2cpp_domain_get_assemblies, [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)], ctypes.POINTER(Il2CppAssembly))


        self._domain: int|None = None
        self._attached = False
        self._assembly_cache: dict[str, int] = {}
        self._image_cache: dict[int, int] = {}
        self._class_cache: list[MonoClass] = []


        # Maybe in the future we can get rid of WINFUNCTYPES and just use calling like GetComponent((_il2cpp_string_new(b'Player'))), etc

        # Get methods based off of signature because they have numerous duplicate names
        self._component = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Component')
        for i in self._component.list_methods():
            if i.name == 'GetComponent' and i.param_count == 1 and i.param_info[0] == 'Parameter 0 type: System.String':
                self._UnityEngine_Component__GetComponent = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(i.address)

        self._UnityEngine_Component__get_transform = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._component, 'get_transform'))
        self._UnityEngine_Component__get_gameObject = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._component, 'get_gameObject'))
        self._UnityEngine_Component__get_tag = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._component, 'get_tag'))
        self._UnityEngine_Component__set_tag = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._component, 'set_tag'))


        self._gameobject = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'GameObject')
        for i in self._gameobject.list_methods():
            if i.name == 'GetComponents' and i.param_count == 1 and i.param_info[0] == 'Parameter 0 type: System.Type':
                self._UnityEngine_GameObject__GetComponents = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(i.address)
            elif i.name == 'AddComponent' and i.param_count == 1 and i.param_info[0] == 'Parameter 0 type: System.Type':
                self._UnityEngine_GameObject__AddComponent = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(i.address)       

        self._UnityEngine_GameObject__Find = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._gameobject, 'Find'))
        self._UnityEngine_GameObject__FindGameObjectWithTag = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._gameobject, 'FindGameObjectWithTag'))
        self._UnityEngine_GameObject__SetActive = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method(self._gameobject, 'SetActive'))
        self._UnityEngine_GameObject__get_transform = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._gameobject.find_method('get_transform', param_count=0).address)
        self._UnityEngine_GameObject__get_tag = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._gameobject, 'get_tag'))
        self._UnityEngine_GameObject__set_tag = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._gameobject, 'set_tag'))
        self._UnityEngine_GameObject__get_isStatic = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._gameobject, 'get_isStatic'))
        self._UnityEngine_GameObject__get_scene = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._gameobject, 'get_tag'))
        self._UnityEngine_GameObject__get_layer = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._gameobject, 'get_layer'))
        self._UnityEngine_GameObject__set_layer = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self.__find_method(self._gameobject, 'set_layer'))

        self._behaviour = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Behaviour')
        self._UnityEngine_Behaviour__get_enabled = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._behaviour, 'get_enabled'))
        self._UnityEngine_Behaviour__set_enabled = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method(self._behaviour, 'set_enabled'))

        self._camera = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Camera')
        
        self._UnityEngine_Camera_get_current = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._camera, 'get_current'))
        self._UnityEngine_Camera_get_main = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._camera, 'get_main'))
        self._UnityEngine_Camera_get_allCamerasCount = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._camera, 'get_allCamerasCount'))
        self._UnityEngine_Camera_get_allCameras = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._camera, 'get_allCameras'))
        self._UnityEngine_Camera__get_depth = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._camera, 'get_depth'))
        self._UnityEngine_Camera__set_depth = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method(self._camera, 'set_depth'))
        self._UnityEngine_Camera__get_fieldOfView = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._camera, 'get_fieldOfView'))
        self._UnityEngine_Camera__set_fieldOfView = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method(self._camera, 'set_fieldOfView'))
        

        self._object = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Object')

        self._UnityEngine_Object__FindObjectOfType = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self._object.find_method('FindObjectOfType', param_count=2).address)
        self._UnityEngine_Object__FindObjectsOfType = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self._object.find_method('FindObjectsOfType', param_count=2).address)
        self._UnityEngine_Object__get_name = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._object, 'get_name'))
        self._UnityEngine_Object__set_name = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._object, 'set_name'))
        self._UnityEngine_Object__Destroy = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self._object.find_method('Destroy', param_count=1).address)
        

        self._transform = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Transform')
        
        self._UnityEngine_Transform__IsChildOf = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'IsChildOf'))
        self._UnityEngine_Transform__get_childCount = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'get_childCount'))
        self._UnityEngine_Transform__GetChild = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self.__find_method(self._transform, 'GetChild'))
        self._UnityEngine_Transform__LookAt_transform = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('LookAt', param_count=1).address)
        self._UnityEngine_Transform__LookAt_pos = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.POINTER(Vec3), ctypes.c_void_p)(self._transform.find_method('LookAt', param_count=2).address)
        self._UnityEngine_Transform__Find = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'Find'))
        self._UnityEngine_Transform__translate = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_int32, ctypes.c_void_p)(self.__find_method(self._transform, 'Translate'))
        self._UnityEngine_Transform__set_position = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method(self._transform, 'set_position'))
        self._UnityEngine_Transform__get_position = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'get_position'))
        self._UnityEngine_Transform__set_rotation = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Quaternion), ctypes.c_void_p)(self.__find_method(self._transform, 'set_rotation'))
        self._UnityEngine_Transform__get_rotation = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Quaternion), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'get_rotation'))
        self._UnityEngine_Transform__get_parent = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'get_parent'))
        self._UnityEngine_Transform__set_parent = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'set_parent'))
        self._UnityEngine_Transform__get_root = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'get_parent'))
        self._UnityEngine_Transform__get_forward = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'get_forward'))
        self._UnityEngine_Transform__set_forward = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'set_forward'))
        self._UnityEngine_Transform__get_up = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'get_up'))
        self._UnityEngine_Transform__get_right = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._transform, 'get_right'))
    

        self._rigidbody = self.get_class_from_name('UnityEngine.PhysicsModule.dll', 'UnityEngine', 'Rigidbody')

        self._UnityEngine_Rigidbody_set_velocity = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method(self._rigidbody, 'set_velocity'))
        self._UnityEngine_Rigidbody_get_velocity = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'get_velocity'))
        self._UnityEngine_Rigidbody_AddForce = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_int32, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'AddForce'))
        self._UnityEngine_Rigidbody_get_centerOfMass = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'get_centerOfMass'))
        self._UnityEngine_Rigidbody_set_detectCollisions = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'set_detectCollisions'))
        self._UnityEngine_Rigidbody_get_position = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'get_position'))
        self._UnityEngine_Rigidbody_set_position = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method(self._rigidbody, 'set_position'))
        self._UnityEngine_Rigidbody_set_useGravity = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'set_useGravity'))
        self._UnityEngine_Rigidbody_get_mass = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'get_mass'))
        self._UnityEngine_Rigidbody_set_mass = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'set_mass'))
        self._UnityEngine_Rigidbody_get_isKinematic = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'get_isKinematic'))
        self._UnityEngine_Rigidbody_set_isKinematic = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'set_isKinematic'))
        self._UnityEngine_Rigidbody_get_rotation = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Quaternion), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._rigidbody, 'get_rotation'))
        self._UnityEngine_Rigidbody_set_rotation = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Quaternion), ctypes.c_void_p)(self.__find_method(self._rigidbody, 'set_rotation'))

        self._scene = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine.SceneManagement', 'Scene')

        self._UnityEngine_Scene__get_name = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._scene, 'get_name'))
        self._UnityEngine_Scene__get_path = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._scene, 'get_path'))
        self._UnityEngine_Scene__get_rootCount = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._scene, 'get_rootCount'))
        self._UnityEngine_Scene__get_isLoaded = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._scene, 'get_isLoaded'))
        self._UnityEngine_Scene__get_guid = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._scene, 'get_guid'))
        self._UnityEngine_Scene__get_buildIndex = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._scene, 'get_buildIndex'))
        self._UnityEngine_Scene__get_handle = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._scene, 'get_handle'))
        self._UnityEngine_Scene__IsValid = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method(self._scene, 'IsValid'))
