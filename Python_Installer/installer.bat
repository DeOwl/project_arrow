@echo off
set TELLO_EDU_PYTHON=%HOMEDRIVE%+%HOMEPATH%+\AppData\Local\TelloEduPython
setlocal enableextensions
md %HOMEDRIVE%%HOMEPATH%\AppData\Local\TelloEduPython
endlocal
echo Устанавливаем python, не закрывате окно!
python_installer.exe /passive DefaultJustForMeTargetDir=%HOMEDRIVE%%HOMEPATH%\AppData\Local\TelloEduPython Shortcuts=0 Include_doc=0 Include_test=0 Include_tools=0
setx TELLO_EDU_PYTHON %HOMEDRIVE%%HOMEPATH%\AppData\Local\TelloEduPython\pythonw.exe
@echo on
%HOMEDRIVE%%HOMEPATH%\AppData\Local\TelloEduPython\python.exe -m pip install -r requirements.txt
pause