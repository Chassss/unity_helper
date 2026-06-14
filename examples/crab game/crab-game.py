import unity_helper, time, ctypes, cyminhook
from typing import Callable, TypeVar, Protocol, Any, ParamSpec

# Heavily obfuscated and stripped game example


# Most of the useful methods that are built into unity_helper like find_object() or find_object_with_tag() or GetComponents() are stripped
# so calling some game functions that need a instance just arent reasonable to call like anything in TimeManager since we cant find an instance
# using TimeManager.find_object_of_type()

P = ParamSpec("P")
R = TypeVar("R")
__ACTIVE_HOOKS = []

# Helper for a decorator
class HookedFunction(Protocol[P, R]):
    original: Callable[P, R]
    close: None
    def __call__(self, *args, **kwargs) -> Any: ...

# Decorator helper for using cyminhook
def hook(sig, target) -> Callable[[Callable[P, R]], HookedFunction[P, R]]:
    def decorator(func: Callable[P, R]) -> HookedFunction[P, R]:
        if not target or type(target) == str:
            print('\033[31m' + f"Invalid target for func: {func} hook")
            return None
        h = cyminhook.MinHook(signature=sig, target=target, detour=func)
        h.enable()
        __ACTIVE_HOOKS.append(h)

        func.original = h.original
        func.close = h.close

        return func
    return decorator


def initialize_steam():
    steam = ctypes.WinDLL("steam_api64_net.dll")

    steam.SteamAPI_ISteamFriends_GetFriendPersonaName.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

    steam.SteamAPI_ISteamFriends_GetFriendPersonaName.restype = ctypes.c_char_p

    steam.SteamAPI_Init.restype = ctypes.c_bool

    if not steam.SteamAPI_Init():
        raise RuntimeError("SteamAPI_Init failed")

    steam.SteamAPI_SteamFriends_v017.restype = ctypes.c_void_p

    return steam


config = {}
host_config = {}

command_types = {
    '!god': {'type': 'player_toggle', 'var': 'godmode'},
    '!autorespawn': {'type': 'player_toggle', 'var': 'auto_respawn'},
    # '!snowballs': {'type': 'player_toggle', 'var': 'snowballs'},
    # '!anti_knockback': {'type': 'player_toggle', 'var': 'anti_knockback'},

    '!give': {'type': 'generic', 'var': None},
    '!giveall': {'type': 'generic', 'var': None},
    '!makeitrain': {'type': 'generic', 'var': None},
    '!stop': {'type': 'generic', 'var': None},
    '!respawn': {'type': 'generic', 'var': None},
    '!start': {'type': 'generic', 'var': None},
    '!lobby': {'type': 'generic', 'var': None},
    '!win': {'type': 'generic', 'var': None},
    '!suicide': {'type': 'generic', 'var': None},
    '!removeall': {'type': 'generic', 'var': None},
    '!settimer': {'type': 'generic', 'var': None},

    '!timer': {'type': 'host_toggle', 'var': 'unlimited_time'},
}

ref = unity_helper.Il2cpp(False)

while not ref.memory._GetModuleHandleW('steam_api64_net.dll'):
    time.sleep(0.1)

steam = initialize_steam()



# This is the server side functionality
GameServer = ref.get_class_from_name('Assembly-CSharp.dll', 'ႝႨႤႛ႙ႝႢႡႣႠႣ')
ForceGiveAllWeapon = GameServer.find_method('ForceGiveAllWeapon')
ForceGiveWeapon = GameServer.find_method('ForceGiveWeapon')
PlayerDied = GameServer.find_method('PlayerDied')
QueueRespawn = GameServer.find_method('QueueRespawn')
ForceRemoveAllWeapons = GameServer.find_method('ForceRemoveAllWeapons')


# Might be server side but i couldnt test
Item = ref.get_class_from_name('Assembly-CSharp.dll', 'ႥႜႤ႙ႠႣႛႝႤႦႝ')
ItemID = Item.find_field('Ⴂ႟႙Ⴇ႙ႥႤႣ႙Ⴆႝ') # This isnt actually the ItemID


# This is client side lobby host manager
ClientSideLobbyManager = ref.get_class_from_name('Assembly-CSharp.dll', 'ႛႢႤႦႝႣႜ႙ႝႜႤ')
BanPlayer = ClientSideLobbyManager.find_method('BanPlayer')

# Not server side
ServerManager = ref.get_class_from_name('Assembly-CSharp.dll', 'ႡႠႡ႞ႥႡႝႨႥ႙ႚ')
# RespawnPlayer = ctypes.WINFUNCTYPE(ctypes.c_int64, ctypes.c_int64, ctypes.POINTER(ctypes.c_int64))(ServerManager.find_method('RespawnPlayer').address)


# This is where the main functionality of being host exists
HostManager = ref.get_class_from_name('Assembly-CSharp.dll', '႙Ⴅ႟Ⴈ႙ႤႤႝႝႡႠ')
ReceiveChatMessage = HostManager.find_method('ReceiveChatMessage')
UseItem = HostManager.find_method('UseItem')
PlayerDamage = HostManager.find_method('PlayerDamage')
PlayerActiveItem = HostManager.find_method('PlayerActiveItem')
PunchPlayer = HostManager.find_method('PunchPlayer')


# Anti-ban when shooting a DB and a AK, maybe host only but i couldnt test
UseItem.native_patch(b'\x90' * 5, 946)

# MainManager might be a intermediate from HostManager ??? because im pretty sure hostmanager calls some of these functions
MainManager = ref.get_class_from_name('Assembly-CSharp.dll', 'ႠႨႠႤႨႠႚႥႧႧႜ')
SendChatMessage = MainManager.find_method('SendChatMessage')
SendWinner = MainManager.find_method('SendWinner')
RespawnPlayer = MainManager.find_method('RespawnPlayer')
# PlayerDamage = MainManager.find_method('PlayerDamage')


# Another host side thing
GameModeWaiting = ref.get_class_from_name('Assembly-CSharp.dll', 'GameModeWaiting')
StartGame = GameModeWaiting.find_method('ႡႧႢႛႣ႟ႠႦႢႚႤ') # This function is NOT static but for some reason we can still call it as if it was


# Another host side thing
InGameManager = ref.get_class_from_name('Assembly-CSharp.dll', 'ႣႢႨ႙Ⴄ႙ႣႤႜႡႣ')
RestartLobby = InGameManager.find_method('RestartLobby')
SetWinner = InGameManager.find_method('SetWinner')


# Pretty sure this is client side only
InventoryManager = ref.get_class_from_name('Assembly-CSharp.dll', '႙ႧႥႚႛႠႢႢႥႧႚ')
# UseItem = InventoryManager.find_method('UseItem')

# Another host side thing
TimeManager = ref.get_class_from_name('Assembly-CSharp.dll', 'ႜ႟႙႙ႦႡႥႤႛႢႚ')
CurrentTime = TimeManager.find_field('<Ⴂ႟ႣႤႣႠႢႧ႟ႜႢ>k__BackingField')
DefaultTime = TimeManager.find_field('<ႧႥႦႢ႙ႨႣႚႥႛႠ>k__BackingField')
IsRoundActive = TimeManager.find_field('ႨႛႤႢႚႝႦႝႤႚႦ')
SetTimer = TimeManager.find_method('ႣႥႥႠႡႧႡႢႛႜႤ') # This updates the time rather than sets it i believe
AddTime = TimeManager.find_method('ႢႥႚႡႛႝ႞Ⴂ႟ႛႣ')


# Player class which also contains the player name as a field
Player = ref.get_class_from_name('Assembly-CSharp.dll', 'Ⴅႚ႞႞႙ႨႨႚႝ႟ႜ')
set_ping = Player.find_method('set_ping')


# Get username based off steam id (they must be in your lobby or on your friends list)
def get_username(steamID):
    friends = steam.SteamAPI_SteamFriends_v017()
    name = steam.SteamAPI_ISteamFriends_GetFriendPersonaName(friends, steamID)

    return name.decode("utf-8")


def close_hooks():
    for i in __ACTIVE_HOOKS:
        try:
            i.close()
        except:
            pass


def toggle_command(command, steamID=None):
    toggled = {True: 'on', False: 'off'}
    
    if steamID:
        steamName = get_username(steamID)
        val = config[steamID][command] = not config[steamID].get(command, False)
        SendChatMessage(ctypes.c_int64(1), f'Toggled {command} {toggled.get(val)} for user {steamName}.')
    else:
        val = host_config[command] = not host_config.get(command, False)
        SendChatMessage(ctypes.c_int64(1), f'Toggled {command} {toggled.get(val)}.')


def chat_handler(steamID:int, raw:int):
    # Raw is the address of the start our string struct, at offset 20 contains our unicode string and at offset 16 is the length of that string
    message:str = ref.memory.read_unicode_string(raw + 20, ref.memory.read_short(raw + 16) * 2)
    if message.startswith('!'):
        # If you want host specific commands you can compare against your steamID since this is always unique and should NEVER compare against names (create a dict of name: steamID and pull from that)
        msg_split = message.split(' ')
        command = msg_split[0].lower()
        command_type = command_types.get(command, {}).get('type')
        command_var = command_types.get(command, {}).get('var')
        config.setdefault(steamID, {})


        match command_type:
            case 'player_toggle':
                toggle_command(command_var, steamID)
            case 'host_toggle':
                toggle_command(command_var)

            case 'generic':
                match command:
                    case '!give':
                        ForceGiveWeapon.instance = GameServer.find_object_of_type().instance
                        ForceGiveWeapon(ctypes.c_int64(steamID), int(msg_split[1]), 1)
                    case '!giveall':
                        ForceGiveAllWeapon(int(msg_split[1]))
                    case '!makeitrain':
                        for i in range(100):
                            ForceGiveAllWeapon(i % 13) # The item with the highest ID is 13
                    case '!stop':
                        SendChatMessage(ctypes.c_int64(1), 'Shutting down')
                        close_hooks()
                    case '!respawn':
                        QueueRespawn.instance = GameServer.find_object_of_type().instance
                        QueueRespawn(ctypes.c_int64(steamID), 0.0)
                    case '!start':
                        StartGame()
                    case '!lobby':
                        InGameManager.instance = InGameManager.find_object_of_type().instance
                        RestartLobby()
                    case '!win':
                        # 9223372036854775807 this is the max int we do
                        SendWinner(ctypes.c_int64(steamID), ctypes.c_int64(6767676767676767676))
                    case '!suicide':
                        pos = unity_helper.structures.Vec3(0,0,0) # Position quite literally does not matter cause once again bad game code

                        # Wow this game fucking sucks, you can invoke it with a invalid 2nd param
                        PlayerDied(ctypes.c_int64(steamID), ctypes.c_int64(0), pos)
                    case '!removeall':
                        ForceRemoveAllWeapons() # Bad game code, not static yet we can call it like its static lmfao
            
                    # Not possible
                    # case '!settimer':
                    #     TimeManager.instance = TimeManager.find_object_of_type().instance # This returns None
                    #     SetTimer(ctypes.c_float(msg_split[1]))



# This function actually either A is the wrong function or B the message is encoded
# @hook(ctypes.WINFUNCTYPE(ctypes.c_int64, ctypes.c_int64, ctypes.c_int64), ReceiveChatMessage.address)
# def HookedReceiveChatMessage(steamID, message):
#     # chat_handler(steamID, message)
#     print(hex(message))
#     HookedReceiveChatMessage.close()
#     return HookedReceiveChatMessage.original(steamID, message)


# Pretty sure this makes it so only we can use the commands but i was originally wanting to hook ReceiveChatMessage
@hook(ctypes.WINFUNCTYPE(ctypes.c_int64, ctypes.c_int64, ctypes.c_int64), SendChatMessage.address)
def HookedSendChatMessage(steamID, message):
    chat_handler(steamID, message)
    return HookedSendChatMessage.original(steamID, message)


# Not really setting the timer more like updating the timer, dnspy shows the signature being c_bool return and no param input but ida-pro shows this signature
@hook(ctypes.WINFUNCTYPE(ctypes.c_char, ctypes.c_int64), SetTimer.address)
def HookedSetTimer(this):
    toggled = host_config.get('unlimited_time')

    if toggled:
        TimeManager.instance = this
        if IsRoundActive.value == True and DefaultTime.value > 15:
            return b'\x00'
    
    return HookedSetTimer.original(this)


# Host only method called when a player is killed, the actual function name dani should of named it is "KillPlayer(steamID, player_object)" and completely drop the position param
# This isnt a callback but rather the actual function that kills the player
@hook(ctypes.WINFUNCTYPE(ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, unity_helper.structures.Vec3), PlayerDied.address)
def HookedPlayerDied(steamID, player, pos):
    godmode = config.get(steamID).get('godmode') if config.get(steamID) else None
    auto_respawn = config.get(steamID).get('auto_respawn') if config.get(steamID) else None
    if godmode:
        return 0
    elif auto_respawn:
        death = HookedPlayerDied.original(steamID, player, pos)
        QueueRespawn.instance = GameServer.find_object_of_type().instance
        QueueRespawn(ctypes.c_int64(steamID), 0.0)
        return death
    return HookedPlayerDied.original(steamID, player, pos)

# Server side damage player function
@hook(ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_int64, ctypes.c_int64, ctypes.c_int32), PlayerDamage.address)
def HookedPlayerDamage(steamID, player, damage):
    toggled = config.get(steamID).get('godmode') if config.get(steamID) else None
    if toggled:
        return 0
    return HookedPlayerDamage.original(steamID, player, damage)






# Server side punch method
# @hook(ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_int64, ctypes.c_int64), PunchPlayer.address)
# def HookedPunchPlayer(steamID, player):
#     toggled = config.get(steamID).get('anti_knockback') if config.get(steamID) else None
#     if toggled:
#         return 0
#     return HookedPunchPlayer.original(steamID, player)


# Server side use item method (i couldnt figure out how to get the real ID of the item since the item param is a item class but that item class didnt look like it stored its id anywhere)
# The field i labeled as ItemID actually for some reason always prints out to be a value of 24 so ig its not the item id 
# @hook(ctypes.WINFUNCTYPE(ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p), UseItem.address)
# def HookedUseItem(steamID, item):
#     used = HookedUseItem.original(steamID, item)
#     player_config = config.get(steamID)
#     if player_config and player_config.get('snowballs'):
#         Item.instance = item
#         print(PlayerActiveItem(ctypes.c_int64(steamID), ctypes.c_void_p(item)))
#         if ItemID.value == 9: # This isnt actually the ItemID
#             ForceGiveWeapon.instance = GameServer.find_object_of_type().instance
#             ForceGiveWeapon(ctypes.c_int64(steamID), 9, 0)
#     return used