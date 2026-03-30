# unity_helper

`unity_helper` is a runtime inspection toolkit for Unity applications, designed to expose reflection data including classes, methods, and fields. It allows you to explore and interact with application internals dynamically and in real time.

## Features
- Support for obtaining unity image data
- Support for obtaining unity class data
- Support for obtaining unity method data
- Support for obtaining unity field data
- Supports `IL2CPP` scripting backend

## Installation

unity_helper requires Windows Python 3.11+ (64-bit) operating environment, you can complete the installation through pip:

```bash
pip install -U unity_helper
```

## Examples

```Python
import ctypes
from unity_helper import Il2cpp

# Initialize the class
ref = Il2cpp()

# Getting a MonoClass object
time = ref.get_class_from_name('UnityEngine.CoreModule.dll', 'UnityEngine', 'Time')

# Getting MonoClass info
print('Time info:', time.name, time.object, time.type, time.instance)

# Listing method info in a MonoClass
for method in time.list_methods():
    print('Method info:', method.name, method.address, method.methodInfo, method.is_static, method.param_count, method.param_info)


# Getting a MonoMethod object based off of name
set_timeScale = time.find_method('set_timeScale')

# Calling the method
if not set_timeScale.is_static:
    time.instance = 123456789

set_timeScale((ctypes.c_float(5)))


# Calling the method with a ctypes functype
new_set_timeScale = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_float)(set_timeScale.address)
new_set_timeScale(5.0)



# Listing field info in a MonoClass
for field in time.list_fields():
    print('Field info:', field.name, field.ptr, field.type, field.is_static)

    if not field.is_static:
        time.instance = 123456789
        print('Value:', field.value)


# Getting a field from name
example_field = time.find_field('example_field')


# Setting a field value in a MonoClass
if not example_field.is_static:
    time.instance = 123456789

example_field.value = 9999


# Getting the main camera and getting a rigidbody
main_cam = ref.get_main_camera()
rigidbody = ref.get_RigidBody(123456789)

# Getting/editing rigidbody info
velocity = rigidbody.velocity
velocity.y = 10
rigidbody.velocity = velocity 

pos = rigidbody.position

print(pos.x, pos.y, pos.z)


# Getting/editing camera info
fov = main_cam.fov
main_cam.fov = fov + 10.0

enabled = main_cam.enabled
main_cam.enabled = not enabled

print(main_cam.name)

# Finding a object based off name
player = ref.find_object('Player')


# Finding a object based off of tag
player = ref.find_object_with_tag('Player')


# Listing images
for image in ref.list_assemblies():
    print(image)


# Listing classes in image
for clazz in ref.list_classes_in_image('Assembly-CSharp.dll'):
    print(clazz.name)

```


## More Features

The example above covers some common use cases, but `unity_helper` also enables:

- **Inspecting and interacting with Scene objects** to find and manipulate game entities in real time  
- **Accessing and modifying Component objects**, including Rigidbodies, Cameras, scripts and more  
- **Exploring and updating Transform objects**, such as position, rotation, rect and more