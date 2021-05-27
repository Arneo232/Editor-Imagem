# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


added_files = [
         ( 'model.h5', '.' ),
         ( 'model_3channels.h5', '.' ),
         ( 'interface.kv', '.' ),
         ( 'icones', 'icones' )
         ]


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Aluno\\Documents\\GitHub\\Editor-Imagem'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
