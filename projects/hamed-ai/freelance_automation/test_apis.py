#!/usr/bin/env python3
"""
🧪 اختبار AI APIs - اتأكد إن كل الـ APIs شغالة
"""
import os
import sys
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    sys.exit(1)

# Get API keys
ANTHROPIC_KEY = os.getenv('ANTHROPIC_API_KEY', '')
OPENAI_KEY = os.getenv('OPENAI_API_KEY', '')
KIMI_KEY = os.getenv('KIMI_API_KEY', '')
GEMINI_KEY = os.getenv('GEMINI_API_KEY', '')

print("=" * 60)
print("🧪 اختبار AI APIs")
print("=" * 60)
print()

# Test Anthropic Claude
print("1️⃣  اختبار Anthropic Claude...")
if ANTHROPIC_KEY and ANTHROPIC_KEY != 'sk-ant-api03--1Y...mAAA':
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{"role": "user", "content": "قل مرحبا بالعربية"}]
        )
        print(f"✅ Anthropic شغال!")
        print(f"   الرد: {response.content[0].text[:50]}...")
    except Exception as e:
        print(f"❌ Anthropic فشل: {e}")
else:
    print("⚠️  مفتاح Anthropic غير موجود أو غير صحيح")
print()

# Test OpenAI
print("2️⃣  اختبار OpenAI GPT-4...")
if OPENAI_KEY and OPENAI_KEY != 'key_C8KiWEvc7gnmHzxF':
    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "قل مرحبا بالعربية"}],
            max_tokens=100
        )
        print(f"✅ OpenAI شغال!")
        print(f"   الرد: {response.choices[0].message.content[:50]}...")
    except Exception as e:
        print(f"❌ OpenAI فشل: {e}")
else:
    print("⚠️  مفتاح OpenAI غير موجود أو غير صحيح")
print()

# Test Kimi
print("3️⃣  اختبار Kimi Moonshot...")
if KIMI_KEY:
    try:
        import requests
        response = requests.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {KIMI_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "moonshot-v1-8k",
                "messages": [{"role": "user", "content": "قل مرحبا بالعربية"}],
                "max_tokens": 100
            },
            timeout=10
        )
        if response.status_code == 200:
            text = response.json()['choices'][0]['message']['content']
            print(f"✅ Kimi شغال!")
            print(f"   الرد: {text[:50]}...")
        else:
            print(f"❌ Kimi فشل: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Kimi فشل: {e}")
else:
    print("⚠️  مفتاح Kimi غير موجود")
print()

# Test Gemini
print("4️⃣  اختبار Google Gemini...")
if GEMINI_KEY:
    try:
        import requests
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{
                    "parts": [{"text": "قل مرحبا بالعربية"}]
                }]
            },
            timeout=10
        )
        if response.status_code == 200:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ Gemini شغال!")
            print(f"   الرد: {text[:50]}...")
        else:
            print(f"❌ Gemini فشل: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Gemini فشل: {e}")
else:
    print("⚠️  مفتاح Gemini غير موجود")
print()

print("=" * 60)
print("✅ انتهى الاختبار!")
print("=" * 60)
