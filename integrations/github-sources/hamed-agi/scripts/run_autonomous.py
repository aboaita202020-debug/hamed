from __future__ import annotations

import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from app.autonomous import autonomous_agent


if __name__ == "__main__":
    result = autonomous_agent.run_cycle()
    print(json.dumps(result, ensure_ascii=False, indent=2))
