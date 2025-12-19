# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['..\\..\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('E:\\project\\watch\\tvDownload\\config.yaml', '.'), ('E:\\project\\watch\\tools\\ffmpeg\\ffmpeg.exe', '.'),
    ('E:\\project\\watch\\tools\\ffmpeg\\ffprobe.exe', '.'), ('E:\\project\\watch\\tvDownload\\statics\\title.ico', '.\\statics')],
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
    a.binaries,
    a.datas,
    [],
    name='视频下载器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="tubiao.ico"
)
