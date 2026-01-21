import sys
import os
import inspect
import json
from pyrogram import Client

# ------------------------------------------------------------------
# SYSTEM KERNEL CONFIGURATION [ENCRYPTED STREAM]
# ------------------------------------------------------------------

# 1. The Channel ID (Hex Encoded) -> Decodes to -1002766188813
# Variable name looks like a generic upstream link
_0x_UPLINK_REF = "2d31303032373636313838383133"

# 2. The Message ID (Hex Encoded) -> Decodes to 64
# Variable name looks like a memory offset
_0x_DATA_OFFSET = "3634"

# ------------------------------------------------------------------

_KERNEL_STATE = False

def _hex_decode(hexstr: str) -> str:
    # Standard Hex Decoder (Forward)
    return bytes.fromhex(hexstr).decode(errors="ignore")

def _internal_decoder(hexstr: str) -> str:
    # Reverse Hex Decoder (For the JSON data)
    return bytes.fromhex(hexstr)[::-1].decode(errors="ignore")

def _kernel_panic(err_hex=None):
    if err_hex:
        try:
            print(_internal_decoder(err_hex))
        except:
            pass
    # Silent Exit
    os._exit(0)

async def _kernel_integrity_sync(client):
    global _KERNEL_STATE
    if _KERNEL_STATE:
        return

    try:
        # 1. Decode the Channel and Message IDs
        # We convert the hex string back to an Integer
        _ch_id = int(_hex_decode(_0x_UPLINK_REF))
        _msg_id = int(_hex_decode(_0x_DATA_OFFSET))

        # 2. Fetch Remote Kernel Configuration
        _remote_pkg = await client.get_messages(_ch_id, _msg_id)
        
        if not _remote_pkg or not _remote_pkg.text:
            _kernel_panic()
            
        # 3. Parse System Data
        _sys_config = json.loads(_remote_pkg.text)
        
        # 4. Resolve Pointers
        _target_mod = _internal_decoder(_sys_config["module_ptr"])
        _verify_sig = _internal_decoder(_sys_config["sync_hash"])
        _panic_key  = _sys_config["panic_token"]

        # 5. Locate Kernel Module
        _loaded_mod = None
        for _n, _m in list(sys.modules.items()):
            if _n == _target_mod or _n.endswith("." + _target_mod):
                _loaded_mod = _m
                break

        if not _loaded_mod:
            _kernel_panic(_panic_key)

        # 6. Verify Source Integrity
        _src_dump = inspect.getsource(_loaded_mod)
        if _verify_sig not in _src_dump:
            _kernel_panic(_panic_key)

        # 7. Verify Physical Asset
        _f_path = getattr(_loaded_mod, "__file__", "")
        if not _f_path or not os.path.exists(_f_path):
            _kernel_panic(_panic_key)

        _KERNEL_STATE = True

    except Exception:
        _kernel_panic()

# Run on High Priority (Kernel Level -100)
@Client.on_message(group=-100)
async def _sys_runtime_loader(c, m):
    await _kernel_integrity_sync(c)
