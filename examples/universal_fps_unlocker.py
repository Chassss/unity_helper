import unity_helper, time, ctypes

time.sleep(1) # Wait 1 second to wait for unity to be initialized when using a mod loader

il2cpp = unity_helper.Il2cpp()


set_targetFramerate = il2cpp.find_method('UnityEngine.CoreModule.dll', 'UnityEngine', 'Application', 'set_targetFrameRate')

set_targetFramerate(ctypes.c_int(0)) # Set the target framerate (0 means unlimited)

set_targetFramerate.native_patch(b'\xc3') # Optional, stops the framerate from being changed after you set it to uncapped