# -*- mode: python ; coding: utf-8 -*-
import sys

if sys.platform == "win32":
    from kivy_deps import sdl2, glew

    more = [Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)]
else:
    more = []



a = Analysis(
    ['surviwan.py'],
    pathex=[],
    binaries=[],
    datas=[('surviwan.kv', '.'), ("textures/", "textures/")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Surviwan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    *more,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='surviwan',
)
