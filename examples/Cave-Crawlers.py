import unity_helper

ref = unity_helper.Il2cpp()


DevTools = ref.get_class_from_name('Assembly-CSharp.dll', '', 'DevTools')
EnableDevTools = DevTools.find_field('EnableDevTools')


for i in DevTools.list_fields():
    if i.name == 'instance':
        DevTools.instance = i.value
        EnableDevTools.value = True
        break


# Now we can press f3 to open the built in devtools