from pathlib import Path
p=Path(r'D:\hamed agi\hamed-agi-live\app\main.py')
s=p.read_text(encoding='utf-8')
imp='from .lumikids_team import lumikids_studio\n'
if imp not in s:
    s=s.replace('from .youtube_studio import youtube_studio\n','from .youtube_studio import youtube_studio\n'+imp,1)
marker='@app.get("/api/v1/youtube/status")\ndef youtube_status(): return {"status":"ok",**youtube_studio.status()}\n'
block='''\n\n@app.get("/api/v1/lumikids/team")\ndef lumikids_team():\n    return {"status":"ok", **lumikids_studio.status(), "agents_list":[a.__dict__ for a in lumikids_studio.agents.values()]}\n\n@app.post("/api/v1/lumikids/autonomous-cycle")\ndef lumikids_autonomous_cycle(request:dict[str,Any]|None=None):\n    request=request or {}\n    return {"status":"ok", "cycle":lumikids_studio.plan_cycle(str(request.get("topic","daily trending kids content")))}\n\n@app.get("/api/v1/lumikids/daily-report")\ndef lumikids_daily_report():\n    return {"status":"ok", **lumikids_studio.daily_report()}\n'''
if '/api/v1/lumikids/team' not in s:
    if marker not in s: raise SystemExit('youtube status marker not found')
    s=s.replace(marker,marker+block,1)
p.write_text(s,encoding='utf-8')
print('INTEGRATED')
