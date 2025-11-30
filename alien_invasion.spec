# -*- mode: python ; coding: GBK -*-

import os

a = Analysis(
    ['alien_invasion.py'],
    pathex=['D:\\work\\homeWork\\python\\大作业_外星人入侵\\Alien_Invasion'],
    binaries=[],
    datas=[
        ('voices', 'voices'),
        ('images', 'images'),
    ],
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
    [],                  # 这里保持原样，第三个参数是空列表
    exclude_binaries=True,
    name='alien_invasion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,        # 先保留控制台，有报错好看
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
    strip=False,
    upx=True,
    upx_exclude=[],
    name='alien_invasion',
)
