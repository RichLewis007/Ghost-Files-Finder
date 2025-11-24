# -*- mode: python ; coding: utf-8 -*-

import os
import pathlib

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# PyInstaller runs from the project directory, so use current working directory
project_dir = pathlib.Path.cwd()
src_dir = project_dir / "src"
package_root = src_dir / "rfe"

icon_dir = package_root / "resources" / "icons"
feather_dir = icon_dir / "feather"
app_icon = icon_dir / "GhostFilesFinder.icns"
audio_dir = package_root / "resources" / "audio"
rules_file = project_dir / "tests" / "data" / "rclone-filter-list.txt"

# Collect PySide6 data files but exclude Qt3D and other unnecessary frameworks
all_pyside6_datas = collect_data_files("PySide6")
qt3d_framework_names = [
    "Qt3DAnimation",
    "Qt3DCore",
    "Qt3DExtras",
    "Qt3DInput",
    "Qt3DLogic",
    "Qt3DRender",
    "QtCharts",
    "QtDataVisualization",
    "QtQuick",
    "QtQuick3D",
    "QtWebEngine",
    "QtWebEngineCore",
    "QtWebEngineWidgets",
]
# Filter out Qt3D framework data files to avoid symlink conflicts
pyside6_datas = [
    (name, path)
    for name, path in all_pyside6_datas
    if not any(framework in name for framework in qt3d_framework_names)
]

extra_datas = [
    (str(feather_dir), "rfe/resources/icons/feather"),
    (str(app_icon), "rfe/resources/icons"),
    (str(audio_dir), "rfe/resources/audio"),
    (str(rules_file), "tests/data"),
]

datas = pyside6_datas + extra_datas

# Collect only the PySide6 modules we actually use
# Exclude 3D, WebEngine, and other modules we don't need to avoid symlink issues
all_pyside6_modules = collect_submodules("PySide6")
excluded_modules = [
    "PySide6.Qt3D",
    "PySide6.Qt3DAnimation",
    "PySide6.Qt3DCore",
    "PySide6.Qt3DExtras",
    "PySide6.Qt3DInput",
    "PySide6.Qt3DLogic",
    "PySide6.Qt3DRender",
    "PySide6.QtCharts",
    "PySide6.QtDataVisualization",
    "PySide6.QtQuick",
    "PySide6.QtQuick3D",
    "PySide6.QtQuickControls2",
    "PySide6.QtWebEngine",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebSockets",
    "PySide6.QtBluetooth",
    "PySide6.QtNfc",
    "PySide6.QtPositioning",
    "PySide6.QtLocation",
    "PySide6.QtSensors",
    "PySide6.QtSerialPort",
    "PySide6.QtTextToSpeech",
    "PySide6.QtWebChannel",
]
hiddenimports = [m for m in all_pyside6_modules if not any(m.startswith(exc) for exc in excluded_modules)]

block_cipher = None

a = Analysis(
    [str(package_root / "app.py")],
    pathex=[str(src_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded_modules,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Filter out Qt3D and other unnecessary framework binaries to avoid symlink conflicts
qt3d_frameworks = [
    "Qt3DAnimation",
    "Qt3DCore",
    "Qt3DExtras",
    "Qt3DInput",
    "Qt3DLogic",
    "Qt3DRender",
    "QtCharts",
    "QtDataVisualization",
    "QtQuick",
    "QtQuick3D",
    "QtWebEngine",
    "QtWebEngineCore",
    "QtWebEngineWidgets",
]
a.binaries = [
    (name, path, typecode)
    for name, path, typecode in a.binaries
    if not any(framework in name for framework in qt3d_frameworks)
]

# Also filter datas to exclude Qt3D framework data files
# datas can be tuples of 2 (name, path) or 3 (name, path, typecode) elements
a.datas = [
    item
    for item in a.datas
    if not any(framework in str(item[0]) for framework in qt3d_frameworks)
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher, allow_arch=False)

# macOS app bundle Info.plist contents
info_plist = {
    "CFBundleName": "Ghost Files Finder",
    "CFBundleDisplayName": "Ghost Files Finder",
    "CFBundleIdentifier": "com.richlewis.ghostfilesfinder",
    "CFBundleVersion": "1.0.0",
    "CFBundleShortVersionString": "1.0.0",
    "CFBundlePackageType": "APPL",
    "CFBundleSignature": "GFFX",
    "LSMinimumSystemVersion": "10.13",
    "NSHighResolutionCapable": True,
    "NSRequiresAquaSystemAppearance": False,
}

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Ghost Files Finder",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(app_icon),
)

# Collect all files into a directory
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Ghost Files Finder",
)

# Create macOS app bundle with Info.plist for proper dock name
app = BUNDLE(
    coll,
    name="Ghost Files Finder.app",
    icon=str(app_icon),
    bundle_identifier="com.richlewis.ghostfilesfinder",
    info_plist=info_plist,
)
