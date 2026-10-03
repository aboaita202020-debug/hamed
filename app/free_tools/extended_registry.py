# 185 additional specialist AI/tool adapters; access may be paid, free-tier, or self-hosted.
CATS = {
"llm_platforms":["openrouter","groq","mistral","cohere","together","fireworks","replicate","huggingface-inference","deepinfra","novita"],
"llm_apps":["librechat","lobechat","big-agi","msty","chatbox","chatgpt-next-web","chatglm-webui","fastchat","gradio-chat","litellm"],
"prompting":["guidance","outlines","instructor","marvin","dspy","guidance-ai","promptflow","promptfoo-ui","langfuse","helicone"],
"memory":["mem0","zep","memary","letta","memori","motorhead","supermemory","mem0ai","cognee","graphiti"],
"knowledge_graph":["neo4j","networkx","igraph","rdflib","pykeen","stellargraph","deepgraph","graphrag","nano-graphrag","lightgraph"],
"image_models":["flux","sdxl","sd3","pixart","playground-v2","kolors","idefics","qwen-image","hunyuan-image","lumina-image"],
"image_edit":["lama","instructpix2pix","controlnet","ip-adapter","photomaker","instantid","facefusion","facechain","diffedit","masactrl"],
"video_models":["ltx-video","cogvideox","hunyuan-video","wan-video","animatediff-motion","modelscope-video","zeroscope","text2video-zero","video-crafter","opensora"],
"music":["musicgen","audiocraft","stable-audio-tools","riffusion","magenta","julius","demucs","basicpitch","ace-step","udio-open"],
"speech":["silero-vad","silero-stt","moonshine","seamlessm4t","seamless-communication","parakeet","wav2vec","hubert","data2vec-audio","speechmatics-community"],
"translation":["argos-translate","marian-nmt","nllb","m2m100","opus-mt","bergamot","translate-shell","easy-nmt","sentencepiece","sacremoses"],
"document_ai":["layoutlm","layoutlmv3","donut","nougat","pix2struct","kosmos2","olmocr","marker-pdf","pdf2image","unstructured-inference"],
"recommendation":["implicit","lightfm","surprise","cornac","recbole","spotlight","torchrec","tensorflow-recommenders","merlin","lenskit"],
"forecasting":["prophet","neuralprophet","darts","gluonts","chronos","timesfm","tide","nbeats","nhits","statsforecast"],
"anomaly":["pyod","adtk","anomalib","deepod","merlion","alibi-detect","evidently","whylogs","river","ruptures"],
"optimization":["optuna","ray-tune","hyperopt","nevergrad","scikit-optimize","ax","bohb","pymoo","ortools","cvxpy"],
"synthetic_data":["sdv","ydata-synthetic","mostlyai","synthcity","ctgan","tabddpm","copulas","faker","datamime","gretel-synthetics"],
"deployment":["gradio-deploy","streamlit-community","modal","runpod","vast-ai","lambda-labs","banana-dev","baseten","modal-labs","replicate-deploy"],
"observability":["openlit","opik","phoenix","arize","langsmith","wandb","tensorboard","aim","neptune","comet-ml"]
}
TOOLS=[]
for category,names in CATS.items():
    for name in names:
        key=name.lower().replace("_","-").replace(" ","-")
        TOOLS.append({
          "id":"catalog-"+key,"name":name,"category":category,
          "capabilities":[category,"specialist"],"integration":"catalog",
          "access":"mixed","enabled":False
        })
assert len(TOOLS)==190
TOOLS=TOOLS[:185]
