rmdir /s /q build
rmdir /s /q dist
pyinstaller darkapp_console.spec
pyinstaller darkapp_wF.spec
