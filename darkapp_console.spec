# -*- mode: python -*-

block_cipher = None


a = Analysis(['darkapp.py'],
             pathex=['C:\\Users\\Feanor\\CodeProjects\\python'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

to_remove = set()
for each in a.binaries:
    name = each[0].lower()
    if any(v in name for v in (
            'api-ms-win',
            'vcruntime',
            'msvcp',
            'printsupport')):
        to_remove.add(each)
        continue

for each in to_remove:
    a.binaries.remove(each)

for each in a.binaries:
    print(each[0])

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='darkapp',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='darkapp')
