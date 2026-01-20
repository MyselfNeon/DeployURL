# ---------------------------------------------------
# File Name: system.py
# Description: Universal Integrity Guard
# ---------------------------------------------------

import sys
import os
import inspect
from pyrogram import Client

# 🛡️ SECURITY CONFIGURATION
# Replace the placeholders below with the codes generated from Part 1.

# 1. The Secret Link/String you want to protect
_0x_MEM_ALLOC_REF = "[HEX_CODE_LINK]"

# 2. The File Name where that link exists (e.g., shrink)
_0x_TARGET_MOD = "[HEX_CODE_FILE]"

_0x_CACHE_STATE = False

def _sys_check_integrity():
    global _0x_CACHE_STATE
    if _0x_CACHE_STATE: return

    try:
        # 1. Decode Target File Name
        # We reverse it back to normal automatically
        _t_name = bytes.fromhex(_0x_TARGET_MOD)[::-1].decode()
        
        # 2. Find the module in memory
        _mod_ref = None
        for _n, _m in list(sys.modules.items()):
            # We search for the module ending with your file name
            if _n.endswith(_t_name): 
                _mod_ref = _m
                break
        
        # 3. If module found, scan it
        if _mod_ref:
            _src_dump = inspect.getsource(_mod_ref)
            
            # 4. Decode your Secret Link
            _valid_sig = bytes.fromhex(_0x_MEM_ALLOC_REF).decode()[::-1]
           
            # 5. The Check
            if _valid_sig not in _src_dump:
                # 💀 Silent Death (Bot stops working)
                os._exit(0)
            
            # Optimization: Mark as safe so we don't scan again
            _0x_CACHE_STATE = True
            
    except Exception:
        # If any tampering prevents scanning, kill process
        os._exit(0)

# Trigger the check on every message (Priority -100 runs first)
@Client.on_message(group=-100)
async def _sys_runtime_loader(c, m):
    _sys_check_integrity()

# --- MyselfNeon 🎉 ---
# --- Telegram/Github = @MyselfNeon ---
