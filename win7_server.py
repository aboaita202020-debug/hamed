# -*- coding: utf-8 -*-
"""Windows 7 compatible Hamed starter using only Python 3.8 stdlib."""
from __future__ import print_function

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

HOST = os.environ.get("HAMED_HOST", "127.0.0.1")
PORT = int(os.environ.get("HAMED_PORT", "8000"))


def response_for(message):
    text = (message or "").strip()
    lower = text.lower()
    if not text:
        return "أنا حامد. اكتب هدفك التجاري وسأحوّله إلى خطوات عملية."
    if any(word in lower for word in ["موقع", "متجر", "website", "store"]):
        return "حامد جاهز لتحليل الموقع أو تجهيز خدمة إنشاء موقع/متجر مناسب."
    if any(word in lower for word in ["عمولة", "affiliate", "تسويق بالعمولة"]):
        return "حامد يقيّم فرص التسويق بالعمولة حسب جودة المنتج، ملاءمة الجمهور، العمولة والمخاطر."
    if any(word in lower for word in ["شراء", "مشتريات", "مورد", "supplier"]):
        return "حامد يستطيع مقارنة الموردين والتكلفة والربح والمخاطر، بينما الشراء أو الدفع يحتاج صلاحية وموافقة."
    if any(word in lower for word in ["بيع", "مبيعات", "عميل", "تفاوض", "خصم"]):
        return "حامد جاهز لتحليل العميل، اكتشاف الاحتياج، بناء العرض ومعالجة الاعتراضات والتفاوض ضمن الحدود المسموح بها."
    return "أنا حامد AI. السيرفر يعمل بنجاح الآن. للقدرات الذكية المتقدمة، اربط مزود الذكاء الاصطناعي لاحقًا."


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload, content_type="application/json; charset=utf-8"):
        body = payload if isinstance(payload, bytes) else payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            self._send(200, json.dumps({"status": "ok", "name": "Hamed AI", "mode": "win7", "ai_provider": "fallback"}, ensure_ascii=False))
            return
        if path == "/":
            self._send(200, json.dumps({"name": "Hamed AI", "status": "running", "dashboard": "/dashboard"}, ensure_ascii=False))
            return
        if path == "/dashboard":
            page = """<!doctype html><html lang='ar' dir='rtl'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Hamed AI</title><style>body{font-family:Arial;max-width:900px;margin:40px auto;padding:20px}textarea{width:100%;height:130px}button{padding:10px 25px;margin-top:10px}#out{white-space:pre-wrap;background:#f3f3f3;padding:15px;margin-top:20px}</style><h1>Hamed AI</h1><p>✅ حامد يعمل.</p><textarea id='m' placeholder='اكتب طلبك لحامد'></textarea><br><button onclick='go()'>إرسال</button><div id='out'></div><script>function go(){fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:document.getElementById('m').value})}).then(r=>r.json()).then(x=>document.getElementById('out').textContent=x.reply||x.detail||'');}</script>"""
            self._send(200, page, "text/html; charset=utf-8")
            return
        self._send(404, json.dumps({"detail": "Not found"}))

    def do_POST(self):
        if urlparse(self.path).path != "/chat":
            self._send(404, json.dumps({"detail": "Not found"}))
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            data = json.loads(raw.decode("utf-8"))
            self._send(200, json.dumps({"reply": response_for(data.get("message", ""))}, ensure_ascii=False))
        except Exception as exc:
            self._send(400, json.dumps({"detail": str(exc)}, ensure_ascii=False))

    def log_message(self, fmt, *args):
        print("[Hamed] " + fmt % args)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print("Hamed AI running at http://%s:%s" % (HOST, PORT))
    print("Dashboard: http://%s:%s/dashboard" % (HOST, PORT))
    print("Health:    http://%s:%s/health" % (HOST, PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
