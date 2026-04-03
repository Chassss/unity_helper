import unity_helper


ref = unity_helper.Il2cpp()

player = ref.get_class_from_name('Assembly-CSharp.dll', '', 'Player')
IsAIActive = player.find_method('IsAIActive')
CanBeDamaged = player.find_method('CanBeDamaged')

IsAIActive.native_patch(b'\xb0\x01\xc3') # Make the game auto play for us (mov al,1;ret)
CanBeDamaged.native_patch(b'\xb0\x00\xc3') # Make us unkillable (mov al,0;ret)