' Hamed AGI - silent Windows launcher
Option Explicit
Dim shell, fso, root, py, cmd
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
root = fso.GetParentFolderName(fso.GetParentFolderName(WScript.ScriptFullName))
shell.CurrentDirectory = root
py = shell.ExpandEnvironmentStrings("%LocalAppData%\Programs\Python\Python311\pythonw.exe")
If Not fso.FileExists(py) Then py = "pythonw.exe"
cmd = Chr(34) & py & Chr(34) & " -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
shell.Run cmd, 0, False
