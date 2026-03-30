"""
Reserved for internal use only.

"""

import ctypes
from .structures import Vec3, Quaternion, Rect, Il2CppAssembly
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

        self._UnityEngine_Component__get_transform = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._component.find_method('get_transform').address)
        self._UnityEngine_Component__get_gameObject = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._component.find_method('get_gameObject').address)
        self._UnityEngine_Component__get_tag = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._component.find_method('get_tag').address)
        self._UnityEngine_Component__set_tag = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)(self._component.find_method('set_tag').address)


        self._gameobject = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'GameObject')
        for i in self._gameobject.list_methods():
            if i.name == 'GetComponents' and i.param_count == 1 and i.param_info[0] == 'Parameter 0 type: System.Type':
                self._UnityEngine_GameObject__GetComponents = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(i.address)
            elif i.name == 'AddComponent' and i.param_count == 1 and i.param_info[0] == 'Parameter 0 type: System.Type':
                self._UnityEngine_GameObject__AddComponent = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(i.address)       

        self._UnityEngine_GameObject__Find = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._gameobject.find_method('Find').address)
        self._UnityEngine_GameObject__FindGameObjectWithTag = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._gameobject.find_method('FindGameObjectWithTag').address)
        self._UnityEngine_GameObject__SetActive = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self._gameobject.find_method('SetActive').address)
        self._UnityEngine_GameObject__get_transform = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._gameobject.find_method('get_transform', param_count=0).address)
        self._UnityEngine_GameObject__get_tag = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._gameobject.find_method('get_tag').address)
        self._UnityEngine_GameObject__set_tag = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._gameobject.find_method('set_tag').address)
        self._UnityEngine_GameObject__get_isStatic = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self._gameobject.find_method('get_isStatic').address)
        self._UnityEngine_GameObject__get_scene = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._gameobject.find_method('get_tag').address)

        self._behaviour = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Behaviour')
        self._UnityEngine_Behaviour__get_enabled = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self._behaviour.find_method('get_enabled').address)
        self._UnityEngine_Behaviour__set_enabled = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self._behaviour.find_method('set_enabled').address)

        self._camera = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Camera')
        
        self._UnityEngine_Camera_get_current = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self._camera.find_method('get_current').address)
        self._UnityEngine_Camera_get_main = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self._camera.find_method('get_main').address)
        self._UnityEngine_Camera_get_allCamerasCount = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self._camera.find_method('get_allCamerasCount').address)
        self._UnityEngine_Camera_get_allCameras = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self._camera.find_method('get_allCameras').address)
        self._UnityEngine_Camera__get_depth = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self._camera.find_method('get_depth').address)
        self._UnityEngine_Camera__set_depth = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self._camera.find_method('set_depth').address)
        self._UnityEngine_Camera__get_fieldOfView = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self._camera.find_method('get_fieldOfView').address)
        self._UnityEngine_Camera__set_fieldOfView = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self._camera.find_method('set_fieldOfView').address)
        

        self._object = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Object')

        self._UnityEngine_Object__FindObjectOfType = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self._object.find_method('FindObjectOfType', param_count=2).address)
        self._UnityEngine_Object__FindObjectsOfType = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self._object.find_method('FindObjectsOfType', param_count=2).address)
        self._UnityEngine_Object__get_name = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._object.find_method('get_name').address)
        self._UnityEngine_Object__set_name = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._object.find_method('set_name').address)
        self._UnityEngine_Object__Destroy = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self._object.find_method('Destroy', param_count=1).address)
        

        self._transform = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Transform')
        
        self._UnityEngine_Transform__IsChildOf = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('IsChildOf').address)
        self._UnityEngine_Transform__get_childCount = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('get_childCount').address)
        self._UnityEngine_Transform__GetChild = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self._transform.find_method('GetChild').address)
        self._UnityEngine_Transform__LookAt_transform = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('LookAt', param_count=1).address)
        self._UnityEngine_Transform__LookAt_pos = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.POINTER(Vec3), ctypes.c_void_p)(self._transform.find_method('LookAt', param_count=2).address)
        self._UnityEngine_Transform__Find = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('Find').address)
        self._UnityEngine_Transform__translate = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_int32, ctypes.c_void_p)(self._transform.find_method('Translate').address)
        self._UnityEngine_Transform__set_position = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self._transform.find_method('set_position').address)
        self._UnityEngine_Transform__get_position = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('get_position').address)
        self._UnityEngine_Transform__set_rotation = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Quaternion), ctypes.c_void_p)(self._transform.find_method('set_rotation').address)
        self._UnityEngine_Transform__get_rotation = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Quaternion), ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('get_rotation').address)
        self._UnityEngine_Transform__get_rect = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Rect), ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('get_rotation').address)
        self._UnityEngine_Transform__get_parent = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('get_parent').address)
        self._UnityEngine_Transform__set_parent = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('set_parent').address)
        self._UnityEngine_Transform__get_root = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._transform.find_method('get_parent').address)

        self._rigidbody = self.get_class_from_name('UnityEngine.PhysicsModule.dll', 'UnityEngine', 'Rigidbody')

        self._UnityEngine_Rigidbody_set_velocity = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self._rigidbody.find_method('set_velocity').address)
        self._UnityEngine_Rigidbody_get_velocity = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self._rigidbody.find_method('get_velocity').address)
        self._UnityEngine_Rigidbody_AddForce = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_int32, ctypes.c_void_p)(self._rigidbody.find_method('AddForce').address)
        self._UnityEngine_Rigidbody_get_centerOfMass = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self._rigidbody.find_method('get_centerOfMass').address)
        self._UnityEngine_Rigidbody_set_detectCollisions = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self._rigidbody.find_method('set_detectCollisions').address)
        self._UnityEngine_Rigidbody_get_position = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self._rigidbody.find_method('get_position').address)
        self._UnityEngine_Rigidbody_set_position = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self._rigidbody.find_method('set_position').address)
        self._UnityEngine_Rigidbody_set_useGravity = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self._rigidbody.find_method('set_useGravity').address)
        

        self._scene = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine.SceneManagement', 'Scene')

        self._UnityEngine_Scene__get_name = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._scene.find_method('get_name').address)
        self._UnityEngine_Scene__get_path = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._scene.find_method('get_path').address)
        self._UnityEngine_Scene__get_rootCount = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self._scene.find_method('get_rootCount').address)
        self._UnityEngine_Scene__get_isLoaded = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self._scene.find_method('get_isLoaded').address)
        self._UnityEngine_Scene__get_guid = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self._scene.find_method('get_guid').address)
        self._UnityEngine_Scene__get_buildIndex = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self._scene.find_method('get_buildIndex').address)
        self._UnityEngine_Scene__get_handle = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self._scene.find_method('get_handle').address)
        self._UnityEngine_Scene__IsValid = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self._scene.find_method('IsValid').address)

        # self._gizmos = self.get_class_by_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Gizmos')
        
        # self._UnityEngine_Gizmos__DrawCube = ctypes.WINFUNCTYPE(None, Vec3, Vec3, ctypes.c_void_p)(self._gizmos.find_method('DrawCube').address)
        # self._UnityEngine_Gizmos__DrawLine = ctypes.WINFUNCTYPE(None, Vec3, Vec3, ctypes.c_void_p)(self._gizmos.find_method('DrawLine').address)
        # self._UnityEngine_Gizmos__DrawRay = ctypes.WINFUNCTYPE(None, Vec3, Vec3, ctypes.c_void_p)(self._gizmos.find_method('DrawRay').address)
        # self._UnityEngine_Gizmos__DrawSphere = ctypes.WINFUNCTYPE(None, Vec3, ctypes.c_float, ctypes.c_void_p)(self._gizmos.find_method('DrawSphere').address)
        # self._UnityEngine_Gizmos__DrawWireCube = ctypes.WINFUNCTYPE(None, Vec3, Vec3, ctypes.c_void_p)(self._gizmos.find_method('DrawWireCube').address)
        # self._UnityEngine_Gizmos__DrawWireSphere = ctypes.WINFUNCTYPE(None, Vec3, ctypes.c_float, ctypes.c_void_p)(self._gizmos.find_method('DrawWireSphere').address)
        
        
        # self._debug = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Debug')

        # self._UnityEngine_Debug__DrawLine = ctypes.WINFUNCTYPE(None, Vec3, Vec3, Color, ctypes.c_void_p)(self._debug.find_method('DrawLine', param_count=3).address)


        # self._gl = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'GL')

        # self._UnityEngine_GL__Begin = ctypes.WINFUNCTYPE(None, ctypes.c_int32, ctypes.c_void_p)(self._gl.find_method('Begin').address)        
        # self._UnityEngine_GL__End = ctypes.WINFUNCTYPE(None, ctypes.c_void_p)(self._gl.find_method('End').address)
        # self._UnityEngine_GL__Vertex3 = ctypes.WINFUNCTYPE(None, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_void_p)(self._gl.find_method('Vertex3').address)
        # self._UnityEngine_GL__Color = ctypes.WINFUNCTYPE(None, Color, ctypes.c_void_p)(self._gl.find_method('Color').address)
