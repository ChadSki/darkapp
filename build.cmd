rmdir /s /q build
rmdir /s /q dist
pyinstaller darkapp.spec
xcopy /S /I /Y src\*.py dist\
