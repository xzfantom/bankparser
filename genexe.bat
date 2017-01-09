rem generate exe file
rem pyinstaller --version-file=versionexe.txt --onefile --console --distpath exe -n bankparser "src\bankparser\bankparsercli.py"
pyinstaller --onefile --console --distpath exe -n bankparser "src\bankparser\bankparsercli.py"