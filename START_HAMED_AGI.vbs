Option Explicit

Dim sh, fso, base, pythonw, key, cmd, http, ready
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

base = "D:\hamed agi\hamed-main\hamed-main"
pythonw = "C:\Users\2hamed\AppData\Local\Programs\Python\Python311\pythonw.exe"
key = "HKCU\Software\Microsoft\Windows\CurrentVersion\Run\HamedAGI"

If Not fso.FolderExists(base) Then
    MsgBox "Hamed AGI folder not found:" & vbCrLf & base, 16, "Hamed AGI"
    WScript.Quit 1
End If

If Not fso.FileExists(pythonw) Then
    MsgBox "Python 3.11 pythonw.exe not found:" & vbCrLf & pythonw, 16, "Hamed AGI"
    WScript.Quit 1
End If

sh.RegWrite key, "wscript.exe \"" & WScript.ScriptFullName & "\"", "REG_SZ"

ready = False
On Error Resume Next
Set http = CreateObject("WinHttp.WinHttpRequest.5.1")
http.SetTimeouts 500, 500, 700, 700
http.Open "GET", "http://127.0.0.1:8000/health", False
http.Send
If Err.Number = 0 And http.Status = 200 Then ready = True
Err.Clear
On Error GoTo 0

If Not ready Then
    sh.CurrentDirectory = base
    cmd = "\"" & pythonw & "\" -m uvicorn cloud_server:app --host 127.0.0.1 --port 8000"
    sh.Run cmd, 0, False
End If

sh.Run "http://127.0.0.1:8000/dashboard", 1, False

Set http = Nothing
Set fso = Nothing
Set sh = Nothing
