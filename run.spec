# -*- mode: python ; coding: utf-8 -*-

import os
import importlib
#from PyInstaller.utils.hooks import collect_submodules
block_cipher = None
#hidden_imports = collect_submodules('keras')

a = Analysis(['run.py'],
             pathex=[],
             binaries=[],
             datas=[('./models/yolov4_1024/', './models/yolov4_1024/'),('./output/', './output/'), (os.path.join(os.path.dirname(importlib.import_module('tensorflow').__file__), "lite/experimental/microfrontend/python/ops/_audio_microfrontend_op.so"),"tensorflow/lite/experimental/microfrontend/python/ops/")],
             hiddenimports=['keras', 'keras.api', 'keras.api._v2'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='run')
