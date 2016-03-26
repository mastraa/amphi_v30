# -*- mode: python -*-

block_cipher = None



a = Analysis(['metis.py'],
             pathex=['/Users/mastraa/Desktop/1001Vela/6000/Emessi/6024_ProgrammiDecodifica/amphi_v30'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.binaries=[x for x in a.binaries if not x[0].startswith("scipy")]
a.binaries=[x for x in a.binaries if not x[0].startswith("wx")]
a.binaries=[x for x in a.binaries if not x[0].startswith("PIL")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='metis',
          debug=False,
          strip=False,
          upx=True,
          console=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='metis')
