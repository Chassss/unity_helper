# unity_helper

> Runtime inspection toolkit for Unity IL2CPP applications — explore classes, methods, fields, and live objects in real time.

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Overview

`unity_helper` is a Python toolkit for runtime inspection of Unity applications using the **IL2CPP scripting backend**.
It provides reflection-like capabilities, allowing you to dynamically explore and interact with internal game structures directly from Python.

---

## 🚀 Features

* Inspect Unity assemblies (images)
* Explore classes, methods, and fields
* Call methods dynamically at runtime
* Read and modify field values
* Interact with live Unity objects (Camera, Rigidbody, etc.)
* Designed specifically for **IL2CPP environments**

---

## ⚡ Quick Start

```python
from unity_helper import Il2cpp

ref = Il2cpp()

# Get a Unity class
time = ref.get_class_from_name(
    'UnityEngine.CoreModule.dll',
    'UnityEngine',
    'Time'
)

print(time.name)
```

---

## 📦 Installation

```bash
pip install -U unity_helper
```

---

## 🧰 Requirements

* Windows (64-bit)
* Python 3.11+
* Target application using Unity IL2CPP

---

## 🧪 Examples

### 🔹 Class & Method Inspection

```python
time = ref.get_class_from_name(
    'UnityEngine.CoreModule.dll',
    'UnityEngine',
    'Time'
)

print('Time info:', time.name, time.object, time.type, time.instance)

for method in time.list_methods():
    print(
        'Method info:',
        method.name,
        method.address,
        method.methodInfo,
        method.is_static,
        method.param_count
    )
```

---

### 🔹 Calling Methods

```python
import ctypes

set_timeScale = time.find_method('set_timeScale')

if not set_timeScale.is_static:
    time.instance = 123456789

set_timeScale(ctypes.c_float(5))
```

Using ctypes directly:

```python
new_set_timeScale = ctypes.WINFUNCTYPE(
    ctypes.c_void_p,
    ctypes.c_float
)(set_timeScale.address)

new_set_timeScale(5.0)
```

---

### 🔹 Field Access

```python
for field in time.list_fields():
    print('Field:', field.name, field.type, field.is_static)

example_field = time.find_field('example_field')

if not example_field.is_static:
    time.instance = 123456789

example_field.value = 9999
```

---

### 🔹 Working with Unity Objects

```python
main_cam = ref.get_main_camera()
rigidbody = ref.get_RigidBody(123456789)
```

#### Rigidbody

```python
velocity = rigidbody.velocity
velocity.y = 10
rigidbody.velocity = velocity

pos = rigidbody.position
print(pos.x, pos.y, pos.z)
```

#### Camera

```python
fov = main_cam.fov
main_cam.fov = fov + 10.0

main_cam.enabled = not main_cam.enabled
print(main_cam.name)
```

---

### 🔹 Finding Objects

```python
player = ref.find_object('Player')
player = ref.find_object_with_tag('Player')
```

---

### 🔹 Assemblies & Classes

```python
for image in ref.list_assemblies():
    print(image)

for clazz in ref.list_classes_in_image('Assembly-CSharp.dll'):
    print(clazz.name)
```

---

## 🎯 Common Use Cases

* Runtime debugging of Unity applications
* Reverse engineering IL2CPP builds
* Building tooling and automation scripts
* Inspecting and modifying live game state
* Creating game mods

---

## ⚠️ Important Notes

- This is a Python script that **must be executed within the game's process**.
- It **does not work as a standalone script** and cannot interact with external processes.
- Running it outside of the game environment will not work.

---

## 📄 License

MIT License
