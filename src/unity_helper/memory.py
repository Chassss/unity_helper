import ctypes
from keystone import Ks, KS_ARCH_X86, KS_MODE_64, KS_MODE_32

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

_WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory

_WriteProcessMemory.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t))
_WriteProcessMemory.restype = ctypes.c_int

_VirtualQuery = ctypes.windll.kernel32.VirtualQuery

_process_handle = ctypes.windll.kernel32.GetCurrentProcess()

def is_64bit():
    if ctypes.sizeof(ctypes.c_void_p) == 8:
        return True
    return False

_ks = Ks(KS_ARCH_X86, KS_MODE_64 if is_64bit() else KS_MODE_32)

def assemble(code:str) -> bytes:
    return _ks.asm(code, as_bytes=True)[0]

def read_ctype(address:int, ctype:ctypes._CDataType) -> ctypes._CDataType:
    _ReadProcessMemory(_process_handle, address, ctypes.byref(ctype), ctypes.sizeof(ctype), None)
    return ctype

def read_unicode_string(address:int, length:int) -> str:
    data = read_bytes(address, length)
    if not data:
        return None
    if len(data) % 2 != 0:
        data = data[:-1]
    return data.decode("utf-16-le", errors="ignore").rstrip("\x00")

def read_string(address, length=50, encoding='UTF-8') -> str:
    buff = read_bytes(address, length)
    if buff:
        i = buff.find(b'\x00')
        if i != -1:
            buff = buff[:i]
        buff = buff.decode(encoding)
    return buff

def read_bytes(address, length) -> bytes:
    return read_ctype(address, (ctypes.c_char * length)()).raw

def read_bool(address:int) -> bool:
    return read_ctype(address, ctypes.c_bool()).value

def read_double(address:int) -> float:
    return read_ctype(address, ctypes.c_double()).value

def read_float(address:int) -> float:
    return read_ctype(address, ctypes.c_float()).value

def read_int(address:int) -> int:
    return read_ctype(address, ctypes.c_int()).value

def read_long(address:int) -> int:
    return read_ctype(address, ctypes.c_long()).value

def read_longlong(address:int) -> int:
    return read_ctype(address, ctypes.c_longlong()).value

def read_short(address:int) -> int:
    return read_ctype(address, ctypes.c_short()).value

def read_uint(address:int) -> int:
    return read_ctype(address, ctypes.c_uint()).value

def read_ulong(address:int) -> int:
    return read_ctype(address, ctypes.c_ulong()).value

def read_ulonglong(address:int) -> int:
    return read_ctype(address, ctypes.c_ulonglong()).value

def read_ushort(address:int) -> int:
    return read_ctype(address, ctypes.c_ushort()).value

def read_char(address:int) -> str:
    return read_ctype(address, ctypes.c_char()).value.decode()

def read_uchar(address:int) -> bytes:
    return read_ctype(address, ctypes.c_ubyte()).value


def write_ctype(address, ctype:ctypes._CDataType) -> int:
    return _WriteProcessMemory(_process_handle, address, ctypes.cast(ctypes.byref(ctype), ctypes.c_void_p), ctypes.sizeof(ctype), None)

def write_bytes(address:int, new_bytes:bytes) -> int:
    buff = (ctypes.c_char * len(new_bytes))()
    buff.value = new_bytes
    return write_ctype(address, buff)

def write_bool(address:int, value:bool) -> int:
    return write_ctype(address, ctypes.c_bool(value))

def write_double(address:int, value:float) -> int:
    return write_ctype(address, ctypes.c_double(value))

def write_float(address:int, value:float) -> int:
    return write_ctype(address, ctypes.c_float(value))

def write_int(address:int, value:int) -> int:
    return write_ctype(address, ctypes.c_int(value))

def write_long(address:int, value:int) -> int:
    return write_ctype(address, ctypes.c_long(value))

def write_longlong(address:int, value:int) -> int:
    return write_ctype(address, ctypes.c_longlong(value))

def write_short(address:int, value:int) -> int:
    return write_ctype(address, ctypes.c_short(value))

def write_uint(address:int, value:int) -> int:
    return write_ctype(address, ctypes.c_uint(value))

def write_ulong(address:int, value:int) -> int:
    return write_ctype(address, ctypes.c_ulong(value))

def write_ulonglong(address:int, value:int) -> int:
    return write_ctype(address, ctypes.c_ulonglong(value))

def write_ushort(address:int, value) -> int:
    return write_ctype(address, ctypes.c_ushort(value))

def write_char(address:int, value:str) -> int:
    return write_ctype(address, ctypes.c_char(value))

def write_uchar(address:int, value:str) -> int:
    return write_ctype(address, ctypes.c_ubyte(value))

def write_string(address:int, value:str) -> int:
    return write_bytes(address, value.encode('UTF-8'))

def write_unicode_string(address:int, value:str) -> int:
    return write_bytes(address, value.encode('utf-16-le'))

def get_pages() -> list[int, int]:
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