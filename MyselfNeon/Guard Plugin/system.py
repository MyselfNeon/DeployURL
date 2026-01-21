import sys
import os
import inspect
from pyrogram import Client

_0x_MEM_ALLOC_REF = "PASTE_YOUR_LINK_HEX_HERE"
_0x_TARGET_MOD = "PASTE_YOUR_FILE_HEX_HERE"
_0x_ERR_LOG_REF = "PASTE_YOUR_ERROR_MSG_HEX_HERE"

_0x_CACHE_STATE = False

def _sys_check_integrity():
    global _0x_CACHE_STATE
    if _0x_CACHE_STATE: return

    try:
        def _decode(h): return bytes.fromhex(h)[::-1].decode()
        _t_name = _decode(_0x_TARGET_MOD)
        
        _mod_ref = None
        for _n, _m in list(sys.modules.items()):
            if _n.endswith(_t_name): 
                _mod_ref = _m
                break
        
        if _mod_ref:
            _src_dump = inspect.getsource(_mod_ref)
            _valid_sig = _decode(_0x_MEM_ALLOC_REF)
           
            if _valid_sig not in _src_dump:
                print(f"\n[CRITICAL ERROR] {_decode(_0x_ERR_LOG_REF)}\n")
                
                sys.stdout.flush() 
                os._exit(0)
            
            _0x_CACHE_STATE = True
            
    except Exception:
        os._exit(0)

@Client.on_message(group=-100)
async def _sys_runtime_loader(c, m):
    _sys_check_integrity()
