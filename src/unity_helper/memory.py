import ctypes

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", ctypes.c_ulong),
        ("RegionSize", ctypes.c_size_t),
        ("State", ctypes.c_ulong),
        ("Protect", ctypes.c_ulong),
        ("Type", ctypes.c_ulong),
    ]

MEM_COMMIT = 0x1000
PAGE_NOACCESS = 0x01
PAGE_GUARD = 0x100


_ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory

_ReadProcessMemory.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t))
_ReadProcessMemory.restype = ctypes.c_bool

_VirtualQuery = ctypes.windll.kernel32.VirtualQuery

_process_handle = ctypes.windll.kernel32.GetCurrentProcess()

def is_64bit():
    if ctypes.sizeof(ctypes.c_void_p) == 8:
        return True
    return False

def read_bytes(address, size):
    buff = ctypes.create_string_buffer(size)

    if not _ReadProcessMemory(_process_handle, address, buff, size, None):
        return None
    
    return buff.raw


def get_pages():
    address = 0
    limit = 0x7FFFFFFF0000 if is_64bit() else 0x7fff0000

    regions = []

    while address < limit:
        mbi = MEMORY_BASIC_INFORMATION()

        result = _VirtualQuery(ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi))

        if result == 0:
            break

        if mbi.State == MEM_COMMIT and mbi.Protect not in [PAGE_GUARD, PAGE_NOACCESS]:
            regions.append((mbi.BaseAddress, mbi.RegionSize))

        address += mbi.RegionSize
    
    return regions