Remove-Item -r .\dist
pyinstaller --onefile --clean --icon=favicon.ico main.py
Copy-Item .\PCGameSDK.dll .\dist
Copy-Item .\sdk_pkg_version .\dist
