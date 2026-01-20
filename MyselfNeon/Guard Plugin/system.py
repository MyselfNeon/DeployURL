# ---------------------------------------------------
# File Name: system.py
# Description: Universal Integrity Guard
# ---------------------------------------------------

import sys
import os
import inspect
from pyrogram import Client

_0x_MEM_ALLOC_REF = "[HEX_CODE_LINK]"
_0x_TARGET_MOD = "[HEX_CODE_FILE]"
_0x_CACHE_STATE = False

def _sys_check_integrity():
    global _0x_CACHE_STATE
    if _0x_CACHE_STATE: return

    try:
        _t_name = bytes.fromhex(_0x_TARGET_MOD)[::-1].decode()
        
        _mod_ref = None
        for _n, _m in list(sys.modules.items()):

            if _n.endswith(_t_name): 
                _mod_ref = _m
                break
        
        if _mod_ref:
            _src_dump = inspect.getsource(_mod_ref)
            
            _valid_sig = bytes.fromhex(_0x_MEM_ALLOC_REF).decode()[::-1]
           
            if _valid_sig not in _src_dump:
                os._exit(0)
            
            _0x_CACHE_STATE = True
            
    except Exception:
        os._exit(0)
        
@Client.on_message(group=-100)
async def _sys_runtime_loader(c, m):
    _sys_check_integrity()

# --- MyselfNeon 🎉 ---
# --- Telegram/Github = @MyselfNeon ---
