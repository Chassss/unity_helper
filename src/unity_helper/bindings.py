"""
Reserved for internal use only.

"""

import ctypes
from .structures import Vec3, Quaternion, Il2CppAssembly, Bounds, RaycastHit, Ray, Matrix4x4, Color, Vec2, Rect
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
    
    # Helper functions for getting a method to clean up code and automatically append its methodInfo to a dict for later use
    def __find_method(self, name, unity_obj, method, param_count=None):
        try:
            found_method = unity_obj.find_method(method, param_count=param_count)

            # store methodInfo in dict for later use
            self._methodInfoData[name] = found_method.methodInfo
            if not found_method.address:
                return 0

            return found_method.address
        except Exception as e:
            print(f"Failed to find: {method} some built in features wont work")
            return 0

    def __find_method_by_criteria(self, name, unity_obj, method_name=None, param_count=None, param_types=None):
        try:
            for m in unity_obj.list_methods():

                if method_name is not None and m.name != method_name:
                    continue

                if param_count is not None and m.param_count != param_count:
                    continue

                if param_types is not None:
                    if any(m.param_info[i] != v for i, v in enumerate(param_types)):
                        continue
                
                # store methodInfo in dict for later use
                self._methodInfoData[name] = m.methodInfo
                return m.address

        except Exception as e:
            print(f"Failed to find: {method_name} some built in features wont work")
            return 0

        return 0

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
        self._methodInfoData: dict[str, int] = {}
        self._class_cache: list[MonoClass] = []
    

        self._component = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Component')

        self._UnityEngine_Component__GetComponent = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method_by_criteria('_UnityEngine_Component__GetComponent', self._component, 'GetComponent', 1, ['Parameter 0 type: System.String']))
        self._UnityEngine_Component__get_transform = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Component__get_transform', self._component, 'get_transform'))
        self._UnityEngine_Component__get_gameObject = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Component__get_gameObject', self._component, 'get_gameObject'))
        self._UnityEngine_Component__get_tag = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Component__get_tag', self._component, 'get_tag'))
        self._UnityEngine_Component__set_tag = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Component__set_tag', self._component, 'set_tag'))


        self._gameobject = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'GameObject')

        self._UnityEngine_GameObject__GetComponents = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method_by_criteria('_UnityEngine_GameObject__GetComponents', self._gameobject, 'GetComponents', 1, ['Parameter 0 type: System.Type']))
        self._UnityEngine_GameObject__AddComponent = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method_by_criteria('_UnityEngine_GameObject__AddComponent', self._gameobject, 'AddComponent', 1, ['Parameter 0 type: System.Type']))
        self._UnityEngine_GameObject__Find = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__Find', self._gameobject, 'Find'))
        self._UnityEngine_GameObject__FindGameObjectWithTag = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__FindGameObjectWithTag', self._gameobject, 'FindGameObjectWithTag'))
        self._UnityEngine_GameObject__SetActive = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__SetActive', self._gameobject, 'SetActive'))
        self._UnityEngine_GameObject__get_transform = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__get_transform', self._gameobject, 'get_transform', param_count=0))
        self._UnityEngine_GameObject__get_tag = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__get_tag', self._gameobject, 'get_tag'))
        self._UnityEngine_GameObject__set_tag = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__set_tag', self._gameobject, 'set_tag'))
        self._UnityEngine_GameObject__get_isStatic = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__get_isStatic', self._gameobject, 'get_isStatic'))
        self._UnityEngine_GameObject__get_scene = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__get_scene', self._gameobject, 'get_scene'))
        self._UnityEngine_GameObject__get_layer = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__get_layer', self._gameobject, 'get_layer'))
        self._UnityEngine_GameObject__set_layer = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__set_layer', self._gameobject, 'set_layer'))
        self._UnityEngine_GameObject__get_activeInHierarchy = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__get_activeInHierarchy', self._gameobject, 'get_activeInHierarchy'))
        self._UnityEngine_GameObject__get_activeSelf = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__get_activeSelf', self._gameobject, 'get_activeSelf'))
        self._UnityEngine_GameObject__get_sceneCullingMask = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_GameObject__get_sceneCullingMask', self._gameobject, 'get_sceneCullingMask'))
        self._UnityEngine_GameObject__GetComponent = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method_by_criteria('_UnityEngine_GameObject__GetComponent', self._gameobject, 'GetComponent', 1, ['Parameter 0 type: System.Type']))

        self._behaviour = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Behaviour')

        self._UnityEngine_Behaviour__get_enabled = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Behaviour__get_enabled', self._behaviour, 'get_enabled'))
        self._UnityEngine_Behaviour__set_enabled = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Behaviour__set_enabled', self._behaviour, 'set_enabled'))


        self._camera = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Camera')
        
        self._UnityEngine_Camera_get_current = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera_get_current', self._camera, 'get_current'))
        self._UnityEngine_Camera_get_main = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera_get_main', self._camera, 'get_main'))
        self._UnityEngine_Camera_get_allCamerasCount = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera_get_allCamerasCount', self._camera, 'get_allCamerasCount'))
        self._UnityEngine_Camera_get_allCameras = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera_get_allCameras', self._camera, 'get_allCameras'))
        self._UnityEngine_Camera__get_depth = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_depth', self._camera, 'get_depth'))
        self._UnityEngine_Camera__set_depth = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_depth', self._camera, 'set_depth'))
        self._UnityEngine_Camera__get_fieldOfView = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_fieldOfView', self._camera, 'get_fieldOfView'))
        self._UnityEngine_Camera__set_fieldOfView = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_fieldOfView', self._camera, 'set_fieldOfView'))
        
        self._UnityEngine_Camera__get_allowDynamicResolution = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_allowDynamicResolution', self._camera, 'get_allowDynamicResolution'))
        self._UnityEngine_Camera__get_allowMSAA = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_allowMSAA', self._camera, 'get_allowMSAA'))
        self._UnityEngine_Camera__set_allowMSAA = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_allowMSAA', self._camera, 'set_allowMSAA'))
        self._UnityEngine_Camera__get_allowHDR = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_allowMSAA', self._camera, 'get_allowHDR'))
        self._UnityEngine_Camera__set_allowHDR = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_allowMSAA', self._camera, 'set_allowHDR'))
        self._UnityEngine_Camera__get_aspect = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_aspect', self._camera, 'get_aspect'))
        self._UnityEngine_Camera__set_aspect = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_aspect', self._camera, 'set_aspect'))
        self._UnityEngine_Camera__get_backgroundColor = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Color), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_backgroundColor', self._camera, 'get_backgroundColor'))
        self._UnityEngine_Camera__set_backgroundColor = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Color), ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_backgroundColor', self._camera, 'set_backgroundColor'))
        self._UnityEngine_Camera__get_cameraToWorldMatrix = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Matrix4x4), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_cameraToWorldMatrix', self._camera, 'get_cameraToWorldMatrix'))
        self._UnityEngine_Camera__get_cameraType = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_cameraType', self._camera, 'get_cameraType'))
        self._UnityEngine_Camera__set_cameraType = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_cameraType', self._camera, 'set_cameraType'))
        self._UnityEngine_Camera__get_clearFlags = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_clearFlags', self._camera, 'get_clearFlags'))
        self._UnityEngine_Camera__set_clearFlags = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_clearFlags', self._camera, 'set_clearFlags'))
        self._UnityEngine_Camera__get_cullingMask = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_cullingMask', self._camera, 'get_cullingMask'))
        self._UnityEngine_Camera__set_cullingMask = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_cullingMask', self._camera, 'set_cullingMask'))
        self._UnityEngine_Camera__get_eventMask = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_eventMask', self._camera, 'get_eventMask'))
        self._UnityEngine_Camera__get_farClipPlane = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_farClipPlane', self._camera, 'get_farClipPlane'))
        self._UnityEngine_Camera__set_farClipPlane = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_farClipPlane', self._camera, 'set_farClipPlane'))
        self._UnityEngine_Camera__get_nearClipPlane = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_nearClipPlane', self._camera, 'get_nearClipPlane'))
        self._UnityEngine_Camera__set_nearClipPlane = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_nearClipPlane', self._camera, 'set_nearClipPlane'))
        self._UnityEngine_Camera__get_focalLength = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_focalLength', self._camera, 'get_focalLength'))
        self._UnityEngine_Camera__get_gateFit = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_gateFit', self._camera, 'get_gateFit'))
        self._UnityEngine_Camera__set_gateFit = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_gateFit', self._camera, 'set_gateFit'))
        self._UnityEngine_Camera__get_lensShift = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec2), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_lensShift', self._camera, 'get_lensShift'))
        self._UnityEngine_Camera__set_lensShift = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec2), ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_lensShift', self._camera, 'set_lensShift'))
        self._UnityEngine_Camera__get_orthographicSize = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_orthographicSize', self._camera, 'get_orthographicSize'))
        self._UnityEngine_Camera__set_orthographicSize = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_orthographicSize', self._camera, 'set_orthographicSize'))
        self._UnityEngine_Camera__get_orthographic = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_orthographic', self._camera, 'get_orthographic'))
        self._UnityEngine_Camera__set_orthographic = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_orthographic', self._camera, 'set_orthographic'))
        self._UnityEngine_Camera__get_pixelHeight = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_pixelHeight', self._camera, 'get_pixelHeight'))
        self._UnityEngine_Camera__get_pixelWidth = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_pixelWidth', self._camera, 'get_pixelWidth'))
        self._UnityEngine_Camera__get_pixelRect = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Rect), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_pixelRect', self._camera, 'get_pixelRect'))
        self._UnityEngine_Camera__set_pixelRect = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Rect), ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_pixelRect', self._camera, 'set_pixelRect'))
        self._UnityEngine_Camera__get_targetDisplay = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_targetDisplay', self._camera, 'get_targetDisplay'))
        self._UnityEngine_Camera__set_targetDisplay = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_targetDisplay', self._camera, 'set_targetDisplay'))
        self._UnityEngine_Camera__get_useOcclusionCulling = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p )(self.__find_method('_UnityEngine_Camera__get_useOcclusionCulling', self._camera, 'get_useOcclusionCulling'))
        self._UnityEngine_Camera__set_useOcclusionCulling = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_useOcclusionCulling', self._camera, 'set_useOcclusionCulling'))
        self._UnityEngine_Camera__get_usePhysicalProperties = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__get_orthographic', self._camera, 'get_orthographic'))
        self._UnityEngine_Camera__set_usePhysicalProperties = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Camera__set_usePhysicalProperties', self._camera, 'set_usePhysicalProperties'))


        self._object = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Object')

        self._UnityEngine_Object__Instantiate = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)()
        self._UnityEngine_Object__FindObjectOfType = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Object__FindObjectOfType', self._object, 'FindObjectOfType', param_count=2))
        self._UnityEngine_Object__FindObjectsOfType = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Object__FindObjectsOfType', self._object, 'FindObjectsOfType', param_count=2))
        self._UnityEngine_Object__get_name = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Object__get_name', self._object, 'get_name'))
        self._UnityEngine_Object__set_name = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Object__set_name', self._object, 'set_name'))
        self._UnityEngine_Object__Destroy = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method('_UnityEngine_Object__Destroy', self._object, 'Destroy', param_count=1))
        self._UnityEngine_Object__get_hideFlags = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Object__get_hideFlags', self._object, 'get_hideFlags'))
        self._UnityEngine_Object__set_hideFlags = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self.__find_method('_UnityEngine_Object__set_hideFlags', self._object, 'set_hideFlags'))
        

        self._transform = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Transform')
        
        self._UnityEngine_Transform__IsChildOf = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__IsChildOf', self._transform, 'IsChildOf'))
        self._UnityEngine_Transform__get_childCount = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__get_childCount', self._transform, 'get_childCount'))
        self._UnityEngine_Transform__GetChild = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__GetChild', self._transform, 'GetChild'))
        self._UnityEngine_Transform__LookAt_transform = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__LookAt_transform', self._transform, 'LookAt', param_count=1))
        self._UnityEngine_Transform__LookAt_pos = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__LookAt_pos', self._transform, 'LookAt', param_count=2))
        self._UnityEngine_Transform__Find = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__Find', self._transform, 'Find'))
        self._UnityEngine_Transform__translate = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_int32, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__translate', self._transform, 'Translate'))
        self._UnityEngine_Transform__set_position = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__set_position', self._transform, 'set_position'))
        self._UnityEngine_Transform__get_position = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__get_position', self._transform, 'get_position'))
        self._UnityEngine_Transform__set_rotation = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Quaternion), ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__set_rotation', self._transform, 'set_rotation'))
        self._UnityEngine_Transform__get_rotation = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Quaternion), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__get_rotation', self._transform, 'get_rotation'))
        self._UnityEngine_Transform__get_parent = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__get_parent', self._transform, 'get_parent'))
        self._UnityEngine_Transform__set_parent = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__set_parent', self._transform, 'set_parent'))
        self._UnityEngine_Transform__get_root = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__get_root', self._transform, 'get_parent'))
        self._UnityEngine_Transform__get_forward = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__get_forward', self._transform, 'get_forward'))
        self._UnityEngine_Transform__set_forward = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__set_forward', self._transform, 'set_forward'))
        self._UnityEngine_Transform__get_up = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__get_up', self._transform, 'get_up'))
        self._UnityEngine_Transform__get_right = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform__get_right', self._transform, 'get_right'))
        self._UnityEngine_Transform_get_eulerAngles = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_get_eulerAngles', self._transform, 'get_eulerAngles'))
        self._UnityEngine_Transform_set_eulerAngles = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_set_eulerAngles', self._transform, 'set_eulerAngles'))
        self._UnityEngine_Transform_get_localPosition = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_get_localPosition', self._transform, 'get_localPosition'))
        self._UnityEngine_Transform_set_localPosition = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_set_localPosition', self._transform, 'set_localPosition'))
        self._UnityEngine_Transform_get_hasChanged = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_get_hasChanged', self._transform, 'get_hasChanged'))
        self._UnityEngine_Transform_set_hasChanged = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_set_hasChanged', self._transform, 'set_hasChanged'))
        self._UnityEngine_Transform_get_localRotation = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_get_localRotation', self._transform, 'get_localRotation'))
        self._UnityEngine_Transform_set_localRotation = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_set_localRotation', self._transform, 'set_localRotation'))
        self._UnityEngine_Transform_get_localScale = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_get_localScale', self._transform, 'get_localScale'))
        self._UnityEngine_Transform_set_localScale = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_set_localScale', self._transform, 'set_localScale'))
        self._UnityEngine_Transform_get_localEulerAngles = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_get_localEulerAngles', self._transform, 'get_localEulerAngles'))
        self._UnityEngine_Transform_set_localEulerAngles = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_set_localEulerAngles', self._transform, 'set_localEulerAngles'))
        self._UnityEngine_Transform_get_localToWorldMatrix = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Matrix4x4), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_get_localToWorldMatrix', self._transform, 'get_localToWorldMatrix'))
        self._UnityEngine_Transform_get_worldToLocalMatrix = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Matrix4x4), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Transform_get_worldToLocalMatrix', self._transform, 'get_worldToLocalMatrix'))



        self._rigidbody = self.get_class_from_name('UnityEngine.PhysicsModule.dll', 'UnityEngine', 'Rigidbody')

        self._UnityEngine_Rigidbody_set_angularVelocity = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_set_angularVelocity', self._rigidbody, 'set_angularVelocity'))
        self._UnityEngine_Rigidbody_get_angularVelocity = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_get_angularVelocity', self._rigidbody, 'get_angularVelocity'))
        self._UnityEngine_Rigidbody_set_velocity = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_set_velocity', self._rigidbody, 'set_velocity'))
        self._UnityEngine_Rigidbody_get_velocity = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_get_velocity', self._rigidbody, 'get_velocity'))
        self._UnityEngine_Rigidbody_AddForce = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_int32, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_AddForce', self._rigidbody, 'AddForce'))
        self._UnityEngine_Rigidbody_get_centerOfMass = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_get_centerOfMass', self._rigidbody, 'get_centerOfMass'))
        self._UnityEngine_Rigidbody_set_detectCollisions = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_set_detectCollisions', self._rigidbody, 'set_detectCollisions'))
        self._UnityEngine_Rigidbody_get_position = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Vec3), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_get_position', self._rigidbody, 'get_position'))
        self._UnityEngine_Rigidbody_set_position = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_set_position', self._rigidbody, 'set_position'))
        self._UnityEngine_Rigidbody_set_useGravity = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_set_useGravity', self._rigidbody, 'set_useGravity'))
        self._UnityEngine_Rigidbody_get_mass = ctypes.WINFUNCTYPE(ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_get_mass', self._rigidbody, 'get_mass'))
        self._UnityEngine_Rigidbody_set_mass = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_set_mass', self._rigidbody, 'set_mass'))
        self._UnityEngine_Rigidbody_get_isKinematic = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_get_isKinematic', self._rigidbody, 'get_isKinematic'))
        self._UnityEngine_Rigidbody_set_isKinematic = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_set_isKinematic', self._rigidbody, 'set_isKinematic'))
        self._UnityEngine_Rigidbody_get_rotation = ctypes.WINFUNCTYPE(None, ctypes.POINTER(Quaternion), ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_get_rotation', self._rigidbody, 'get_rotation'))
        self._UnityEngine_Rigidbody_set_rotation = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Quaternion), ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_set_rotation', self._rigidbody, 'set_rotation'))
        self._UnityEngine_Rigidbody_get_constraints = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_get_constraints', self._rigidbody, 'get_constraints'))
        self._UnityEngine_Rigidbody_set_constraints = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)(self.__find_method('_UnityEngine_Rigidbody_set_constraints', self._rigidbody, 'set_constraints'))

        self._scene = self.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine.SceneManagement', 'Scene')

        self._UnityEngine_Scene__get_name = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Scene__get_name', self._scene, 'get_name'))
        self._UnityEngine_Scene__get_path = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Scene__get_path', self._scene, 'get_path'))
        self._UnityEngine_Scene__get_rootCount = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Scene__get_rootCount', self._scene, 'get_rootCount'))
        self._UnityEngine_Scene__get_isLoaded = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Scene__get_isLoaded', self._scene, 'get_isLoaded'))
        self._UnityEngine_Scene__get_guid = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Scene__get_guid', self._scene, 'get_guid'))
        self._UnityEngine_Scene__get_buildIndex = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Scene__get_buildIndex', self._scene, 'get_buildIndex'))
        self._UnityEngine_Scene__get_handle = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Scene__get_handle', self._scene, 'get_handle'))
        self._UnityEngine_Scene__IsValid = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Scene__IsValid', self._scene, 'IsValid'))


        self._physics = self.get_class_from_name('UnityEngine.PhysicsModule.dll', 'UnityEngine', 'Physics')

        self._UnityEngine_Physics_get_gravity = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(Vec3), ctypes.c_void_p)(self.__find_method('_UnityEngine_Physics_get_gravity', self._physics, 'get_gravity'))
        self._UnityEngine_Physics_Simulate = ctypes.WINFUNCTYPE(None, ctypes.c_float, ctypes.c_void_p)(self.__find_method('_UnityEngine_Physics_Simulate', self._physics, 'Simulate'))
        self._UnityEngine_Physics_get_autoSimulation = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('_UnityEngine_Physics_get_autoSimulation', self._physics, 'get_autoSimulation'))
        self._UnityEngine_Physics_set_autoSimulation = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('_UnityEngine_Physics_set_autoSimulation', self._physics, 'set_autoSimulation'))
        self._UnityEngine_Physics_Raycast = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(Vec3), ctypes.POINTER(Vec3), ctypes.POINTER(RaycastHit), ctypes.c_float, ctypes.c_int)(self.__find_method_by_criteria('_UnityEngine_Physics_Raycast', self._physics, 'RayCast', 5, ['Parameter 0 type: UnityEngine.Vector3', 'Parameter 1 type: UnityEngine.Vector3', 'Parameter 2 type: UnityEngine.RaycastHit&', 'Parameter 3 type: System.Single', 'Parameter 4 type: System.Int32']))


        self._collider = self.get_class_from_name('UnityEngine.PhysicsModule.dll', 'UnityEngine', 'Collider')
        
        self._UnityEngine_Collider_get_attachedRigidbody = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('UnityEngine_Collider_get_attachedRigidbody', self._collider, 'get_attachedRigidbody'))
        self._UnityEngine_Collider_get_bounds = ctypes.WINFUNCTYPE(Bounds, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('UnityEngine_Collider_get_bounds', self._collider, 'get_bounds'))
        self._UnityEngine_Collider_get_enabled = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('UnityEngine_Collider_get_enabled', self._collider, 'get_enabled'))
        self._UnityEngine_Collider_set_enabled = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('UnityEngine_Collider_set_enabled', self._collider, 'set_enabled'))
        self._UnityEngine_Collider_get_isTrigger = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(self.__find_method('UnityEngine_Collider_get_isTrigger', self._collider, 'get_isTrigger'))
        self._UnityEngine_Collider_set_isTrigger = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p)(self.__find_method('UnityEngine_Collider_set_isTrigger', self._collider, 'set_isTrigger'))
        self._UnityEngine_Collider_Raycast = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, Ray, ctypes.POINTER(RaycastHit), ctypes.c_float)(self.__find_method_by_criteria('UnityEngine_Collider_Raycast', self._collider, 'Raycast', 3, ['Parameter 0 type: UnityEngine.Ray', 'Parameter 1 type: UnityEngine.RaycastHit&', 'Parameter 2 type: System.Single']))

