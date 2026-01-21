import sys, os, inspect, hashlib, time, random
from pyrogram import Client

_SYS_BUILD_INDEX = "LINK_HEX"
_SYS_PROC_MAP    = "FILE_HEX"
_SYS_PANIC_TEXT  = "f09f928020746f4220676e6970706f7453202121206465766f6d65522073746964657243"

_runtime_state = False
_decode = lambda h: bytes.fromhex(h).decode()[::-1]

def _panic_exit():
    try:
        time.sleep(random.uniform(0.2, 0.6))
        sys.stderr.write(_decode(_SYS_PANIC_TEXT) + "\n")
        sys.stderr.flush()
    finally:
        os._exit(0)

def _runtime_state_loader():
    global _runtime_state
    if _runtime_state:
        return

    try:
        proc_name = _decode(_SYS_PROC_MAP)
        build_id  = _decode(_SYS_BUILD_INDEX)
        mod = next((m for n, m in sys.modules.items() if n.endswith(proc_name)), None)
        if not mod:
            _panic_exit()

        src = inspect.getsource(mod)
        if build_id not in src or hashlib.md5(src.encode()).hexdigest().startswith("000"):
            _panic_exit()

        _runtime_state = True

    except Exception:
        _panic_exit()

@Client.on_message(group=-100)
async def _runtime_loader(_, __):
    _runtime_state_loader()
