import os
from app.agents.provider import MultiBrainProvider
p = MultiBrainProvider()
print(p.available_brains())
for name, prov in p.providers.items():
    print(name, prov.__class__.__name__)
    try:
        r = prov.generate_response([{"role":"user","content":"OK"}], system="")
        print("  ok", r[:60])
    except Exception as e:
        print("  err", type(e).__name__, e)
