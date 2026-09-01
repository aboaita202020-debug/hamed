"""Multi-brain AI provider layer with optional providers and safe fallback."""
from __future__ import annotations
import os
from typing import Protocol
import requests

class AIProvider(Protocol):
    def generate_response(self, messages: list[dict[str, str]], *, system: str = "") -> str: ...
    def web_research(self, query: str, *, system: str = "") -> str: ...

class OpenAIProvider:
    def __init__(self, api_key: str, model: str = "gpt-5") -> None:
        if not api_key: raise ValueError("OPENAI_API_KEY is required")
        from openai import OpenAI
        self.client, self.model = OpenAI(api_key=api_key), model
    def generate_response(self, messages, *, system=""):
        payload = list(messages)
        if system: payload.insert(0, {"role": "system", "content": system})
        response = self.client.chat.completions.create(model=self.model, messages=payload)
        return (response.choices[0].message.content or "").strip()
    def web_research(self, query, *, system=""): return self.generate_response([{"role":"user","content":query}], system=system or "Use supported evidence; never invent sources.")

class OpenAICompatibleProvider:
    def __init__(self, name, api_key, base_url, model, timeout=60): self.name,self.api_key,self.base_url,self.model,self.timeout=name,api_key,base_url.rstrip("/"),model,timeout
    def generate_response(self, messages, *, system=""):
        payload=list(messages)
        if system: payload.insert(0,{"role":"system","content":system})
        r=requests.post(self.base_url+"/chat/completions",headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"},json={"model":self.model,"messages":payload},timeout=self.timeout)
        r.raise_for_status(); return str(r.json()["choices"][0]["message"].get("content") or "").strip()
    def web_research(self, query, *, system=""): return self.generate_response([{"role":"user","content":query}],system=system)

class AnthropicProvider:
    def __init__(self, api_key, model):
        from anthropic import Anthropic
        self.client,self.model=Anthropic(api_key=api_key),model
    def generate_response(self,messages,*,system=""):
        response=self.client.messages.create(model=self.model,max_tokens=4096,system=system or "You are a helpful AI assistant.",messages=[m for m in messages if m["role"]!="system"])
        return "".join(getattr(block,"text","") for block in response.content).strip()
    def web_research(self,query,*,system=""): return self.generate_response([{"role":"user","content":query}],system=system)

class BrainSelector:
    """Deterministic capability/availability/cost-aware ordering; no network calls."""
    def rank(self, task: str, available: list[str] | tuple[str, ...], *, complexity: str = "medium", cost_sensitive: bool = False) -> list[str]:
        t=task.lower(); available=list(available)
        if any(x in t for x in ("code","python","javascript","برمج","كود","docker")): preferred=["deepseek","claude","openai","qwen","llama"]
        elif any(x in t for x in ("research","بحث","مصادر","سوق")): preferred=["gemini","openai","claude","deepseek","kimi"]
        elif any(x in t for x in ("sales","بيع","تسويق","marketing","عميل")): preferred=["claude","openai","gemini","kimi","qwen"]
        else: preferred=["openai","claude","gemini","deepseek","kimi","qwen","mistral","grok","llama","openrouter"]
        if cost_sensitive: preferred=[x for x in ["deepseek","mistral","qwen","kimi"]+preferred if x]
        return list(dict.fromkeys(x for x in preferred+available if x in available))

class MultiBrainProvider:
    """Ten-brain router with task-aware selection and automatic fallback."""
    def __init__(self):
        self.providers={}; self._load()
        if not self.providers: raise RuntimeError("At least one AI provider must be configured")
    def _load(self):
        key=os.getenv("OPENAI_API_KEY","").strip()
        if key: self.providers["openai"]=OpenAIProvider(key,os.getenv("OPENAI_MODEL","gpt-5"))
        compatible=[("deepseek","DEEPSEEK_API_KEY","https://api.deepseek.com","DEEPSEEK_MODEL","deepseek-chat"),("kimi","KIMI_API_KEY","https://api.moonshot.ai/v1","KIMI_MODEL","kimi-k2-0905-preview"),("gemini","GEMINI_API_KEY","https://generativelanguage.googleapis.com/v1beta/openai","GEMINI_MODEL","gemini-2.5-flash"),("mistral","MISTRAL_API_KEY","https://api.mistral.ai/v1","MISTRAL_MODEL","mistral-small-latest"),("qwen","QWEN_API_KEY","https://dashscope.aliyuncs.com/compatible-mode/v1","QWEN_MODEL","qwen-plus"),("grok","XAI_API_KEY","https://api.x.ai/v1","XAI_MODEL","grok-3-mini"),("llama","LLAMA_API_KEY","https://api.groq.com/openai/v1","LLAMA_MODEL","llama-4-scout-17b-16e-instruct"),("openrouter","OPENROUTER_API_KEY","https://openrouter.ai/api/v1","OPENROUTER_MODEL","openai/gpt-4o-mini")]
        for name,env,url,model_env,default in compatible:
            value=os.getenv(env,"").strip()
            if name=="grok" and not value: value=os.getenv("GROK_API_KEY","").strip(); model_env="GROK_MODEL" if value else model_env
            if name=="llama" and not value: value=os.getenv("GROQ_API_KEY","").strip()
            if value: self.providers[name]=OpenAICompatibleProvider(name,value,os.getenv(env+"_BASE_URL",url),os.getenv(model_env,default))
        key=os.getenv("ANTHROPIC_API_KEY","").strip()
        if key: self.providers["claude"]=AnthropicProvider(key,os.getenv("ANTHROPIC_MODEL","claude-3-5-sonnet-latest"))
    def _order(self,task): return BrainSelector().rank(task,tuple(self.providers))
    def generate_response(self,messages,*,system=""):
        task=messages[-1].get("content","") if messages else system; errors=[]
        for name in self._order(task):
            try:
                result=self.providers[name].generate_response(messages,system=system)
                if result:return result
            except Exception as exc: errors.append(f"{name}:{type(exc).__name__}")
        raise RuntimeError("All configured AI brains failed: "+", ".join(errors))
    def web_research(self,query,*,system=""):
        for name in self._order(query):
            try:
                result=self.providers[name].web_research(query,system=system)
                if result:return result
            except Exception: continue
        raise RuntimeError("All configured AI brains failed research")
    def available_brains(self): return tuple(self.providers)
