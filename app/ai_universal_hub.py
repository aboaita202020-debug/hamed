from __future__ import annotations
from dataclasses import dataclass, asdict
import os
from app.free_tools.specialist_registry import FREE_SPECIALIST_TOOLS
from app.free_tools.extended_registry import TOOLS as EXTENDED_TOOLS
@dataclass(frozen=True)
class AITool:
    id:str; name:str; category:str; capabilities:tuple[str,...]; integration:str="api"; env_key:str|None=None
    @property
    def enabled(self): return self.integration in {"local","sdk","self-hosted","free-specialist"} or bool(self.env_key and os.getenv(self.env_key))
_GROUPS={
"reasoning":[("openai","OpenAI","OPENAI_API_KEY"),("anthropic","Anthropic Claude","ANTHROPIC_API_KEY"),("google-gemini","Google Gemini","GEMINI_API_KEY"),("deepseek","DeepSeek","DEEPSEEK_API_KEY"),("moonshot-kimi","Moonshot Kimi","KIMI_API_KEY"),("mistral","Mistral AI","MISTRAL_API_KEY"),("cohere","Cohere","COHERE_API_KEY"),("xai-grok","xAI Grok","XAI_API_KEY"),("perplexity","Perplexity","PERPLEXITY_API_KEY"),("groq","Groq","GROQ_API_KEY"),("together-ai","Together AI","TOGETHER_API_KEY"),("fireworks-ai","Fireworks AI","FIREWORKS_API_KEY")],
"image":[("stability-ai","Stability AI","STABILITY_API_KEY"),("ideogram","Ideogram","IDEOGRAM_API_KEY"),("midjourney","Midjourney","MIDJOURNEY_API_KEY"),("leonardo","Leonardo AI","LEONARDO_API_KEY"),("black-forest-labs","Black Forest Labs","BFL_API_KEY"),("replicate","Replicate","REPLICATE_API_TOKEN"),("comfyui","ComfyUI",None)],
"video":[("runway","Runway","RUNWAY_API_KEY"),("kling","Kling AI","KLING_API_KEY"),("luma","Luma","LUMA_API_KEY"),("pika","Pika","PIKA_API_KEY"),("heygen","HeyGen","HEYGEN_API_KEY"),("synthesia","Synthesia","SYNTHESIA_API_KEY")],
"voice":[("elevenlabs","ElevenLabs","ELEVENLABS_API_KEY"),("cartesia","Cartesia","CARTESIA_API_KEY"),("deepgram","Deepgram","DEEPGRAM_API_KEY"),("assemblyai","AssemblyAI","ASSEMBLYAI_API_KEY"),("playht","PlayHT","PLAYHT_API_KEY"),("speechmatics","Speechmatics","SPEECHMATICS_API_KEY")],
"coding":[("cursor","Cursor","CURSOR_API_KEY"),("github-copilot","GitHub Copilot","GITHUB_TOKEN"),("replit","Replit","REPLIT_API_KEY"),("codeium","Windsurf/Codeium","WINDSURF_API_KEY"),("sourcegraph","Sourcegraph","SOURCEGRAPH_TOKEN"),("tabnine","Tabnine","TABNINE_API_KEY")],
"documents":[("google-vision","Google Cloud Vision","GOOGLE_APPLICATION_CREDENTIALS"),("azure-ai-vision","Azure AI Vision","AZURE_AI_KEY"),("aws-textract","Amazon Textract","AWS_ACCESS_KEY_ID"),("unstructured","Unstructured","UNSTRUCTURED_API_KEY"),("tesseract","Tesseract OCR",None)],
"research":[("serper","Serper","SERPER_API_KEY"),("tavily","Tavily","TAVILY_API_KEY"),("exa","Exa","EXA_API_KEY"),("firecrawl","Firecrawl","FIRECRAWL_API_KEY"),("browserbase","Browserbase","BROWSERBASE_API_KEY"),("apify","Apify","APIFY_API_TOKEN")],
"data":[("pinecone","Pinecone","PINECONE_API_KEY"),("weaviate","Weaviate","WEAVIATE_API_KEY"),("qdrant","Qdrant","QDRANT_API_KEY"),("milvus","Milvus","MILVUS_URI"),("elasticsearch","Elasticsearch","ELASTIC_API_KEY")],
"automation":[("zapier","Zapier","ZAPIER_API_KEY"),("make","Make","MAKE_API_TOKEN"),("n8n","n8n","N8N_API_KEY")],
"agents":[("langchain","LangChain",None),("langgraph","LangGraph",None),("crewai","CrewAI",None),("autogen","AutoGen",None),("semantic-kernel","Semantic Kernel",None),("llamaindex","LlamaIndex",None)],
"local-models":[("ollama","Ollama","OLLAMA_HOST"),("lm-studio","LM Studio","LMSTUDIO_BASE_URL"),("huggingface","Hugging Face","HF_TOKEN")]
}
_CAPS={"reasoning":("chat","reasoning","vision"),"image":("image","image-editing"),"video":("video","image-to-video"),"voice":("text-to-speech","speech-to-text"),"coding":("coding","code-completion"),"documents":("ocr","document-analysis"),"research":("web-search","research"),"data":("retrieval","vector-search"),"automation":("automation","workflows"),"agents":("multi-agent","orchestration"),"local-models":("local-llm","embeddings")}
_BASE_TOOLS=tuple(AITool(i,n,cat,_CAPS[cat],"local" if i in {"comfyui","tesseract","ollama","lm-studio"} else ("sdk" if cat=="agents" else "api"),k) for cat,rows in _GROUPS.items() for i,n,k in rows)
_FREE_TOOLS=tuple(AITool(x["id"],x["name"],x["category"],tuple(x["capabilities"]),x["integration"],None) for x in FREE_SPECIALIST_TOOLS)
_EXTENDED_TOOLS=tuple(AITool(x["id"],x["name"],x["category"],tuple(x["capabilities"]),x["integration"],None) for x in EXTENDED_TOOLS)
TOOLS=_BASE_TOOLS+_FREE_TOOLS+_EXTENDED_TOOLS
TOOL_REGISTRY={t.id:t for t in TOOLS}
def catalog(): return [asdict(t)|{"enabled":t.enabled} for t in TOOLS]
def status():
    cats={}
    for t in TOOLS: cats[t.category]=cats.get(t.category,0)+1
    en=sum(t.enabled for t in TOOLS)
    for required in ("business_ops",):
        cats.setdefault(required, 0)
    return {"total":len(TOOLS),"enabled":en,"disabled":len(TOOLS)-en,"categories":dict(sorted(cats.items()))}
def find_tools(capability,category=None):
    q=capability.lower().strip()
    return [asdict(t)|{"enabled":t.enabled} for t in TOOLS if q in t.capabilities and (not category or t.category==category)]
def route(capability,preferred=None):
    preferred=preferred or []
    cs=[TOOL_REGISTRY[x] for x in preferred if x in TOOL_REGISTRY]
    cs += [t for t in TOOLS if t not in cs and capability in t.capabilities]
    cs.sort(key=lambda t:not t.enabled)
    return {"status":"ok","capability":capability,"selected":(asdict(cs[0])|{"enabled":cs[0].enabled}) if cs else None,"fallbacks":[asdict(t)|{"enabled":t.enabled} for t in cs[1:8]]}
def health(): return {"status":"ok","registry_size":len(TOOLS),"specialist_free_tools":len(FREE_SPECIALIST_TOOLS),"configured":[t.id for t in TOOLS if t.enabled]}
