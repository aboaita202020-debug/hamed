# -*- coding: utf-8 -*-
"""Windows 7 compatible Hamed launcher server.

This compatibility server intentionally uses only Python 3.8-compatible syntax
and the standard library so Hamed can start even when the full modern stack
cannot be installed on an old Windows 7 machine.
"""
from __future__ import print_function

import json
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs, urlparse

HOST = os.environ.get("HAMED_HOST", "127.0.0.1")
PORT = int(os.environ.get("HAMED_PORT", "8000"))


def response_for(message):
    text = (message or "").strip()
    lower = text.lower()
    if not text:
        return "أنا حامد. اكتب هدفك التجاري وسأحوّله إلى خطوات عملية."
    if any(word in lower for word in ["موقع", "متجر", "website", "store"]):
        return "حامد جاهز لاكتشاف مشاكل الموقع أو إنشاء موقع/متجر مناسب وكتابة عرض خدمة مخصص."
    if any(word in lower for word in ["عمولة", "affiliate", "تسويق بالعمولة"]):
        return "حامد يقيّم فرص التسويق بالعمولة حسب جودة المنتج، ملاءمة الجمهور، العمولة، التحويلات والمخاطر."
    if any(word in lower for word in ["شراء", "مشتريات", "مورد", "supplier"]):
        return "حامد يستطيع مقارنة الموردين والتكلفة والربح والمخاطر. تنفيذ الشراء أو الدفع يحتاج صلاحية وموافقة."
    if any(word in lower for word in ["بيع", "مبيعات", "عميل", "تفاوض", "خصم"]):
        return "حامد جاهز لتحليل العميل، اكتشاف الاحتياج، بناء العرض، معالجة الاعتراضات والتفاوض داخل الحدود المسموح بها."
    return "أنا حامد AI. السيرفر يعمل بنجاح الآن. عند ربط مزود الذكاء الاصطناعي يمكن تشغيل القدرات المتقدمة."


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload, content_type="application/json; charset=utf-8"):
        body = payload if isinstance(payload, bytes) else payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send(200, json.dumps({
                "status": "ok",
                "name": "Hamed AI",
                "mode": "windows7_compatibility",
                "ai_provider": "fallback"
            }, ensure_ascii=False))
            return
        if parsed.path == "/":
            self._send(200, json.dumps({
                "name": "Hamed AI",
                "status": "running",
                "dashboard": "/dashboard",
                "chat": "/chat"
            }, ensure_ascii=False))
            return
        if parsed.path == "/dashboard":
            page = """<!doctype html><html lang='ar' dir='rtl'><meta charset='utf-8'>
<title>Hamed AI</title><style>body{font-family:Arial;max-width:900px;margin:40px auto;padding:20px}textarea{width:100%;height:120px}button{padding:10px 25px;margin-top:10px}#out{white-space:pre-wrap;background:#f3f3f3;padding:15px;margin-top:20px}</style>
<h1>Hamed AI</h1><p>✅ السيرفر يعمل.</p><textarea id='m' placeholder='اكتب طلبك لحامد'></textarea><br><button onclick='go()'>إرسال</button><div id='out'></div>
<script>function go(){var m=document.getElementById('m').value;fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})}).then(r=>r.json()).then(x=>document.getElementById('out').textContent=x.reply||x.detail||'');}</script>"""
            self._send(200, page, "text/html; charset=utf-8")
            return
        self._send(404, json.dumps({"detail": "Not found"}))

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/chat":
            self._send(404, json.dumps({"detail": "Not found"}))
            return
        try:
            length = int(self.headers.getheader("Content-Length", "0"))
            raw = self.rfile.read(length)
            data = json.loads(raw.decode("utf-8"))
            reply = response_for(data.get("message", ""))
            self._send(200, json.dumps({"reply": reply}, ensure_ascii=False))
        except Exception as exc:
            self._send(400, json.dumps({"detail": str(exc)}, ensure_ascii=False))

    def log_message(self, fmt, *args):
        print("[Hamed] " + fmt % args)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print("Hamed AI compatibility server running at http://%s:%s" % (HOST, PORT))
    print("Dashboard: http://%s:%s/dashboard" % (HOST, PORT))
    print("Health:    http://%s:%s/health" % (HOST, PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping Hamed AI...")
    finally:
        server.server_close()
