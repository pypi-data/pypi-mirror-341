# 🎵 ragstruct — A Pseudo-Finetuning RAG Framework

> 🔍 Lightweight semantic retriever using structured JSON 
> 💡 Built with love by [Joshikaran K. (Joshi Felix)](https://github.com/Joshikarank)

---

## 🧠 What is ragstruct?

**ragstruct** is a minimal, blazing-fast semantic retrieval library built for anyone who wants to simulate fine-tuned behavior *without* ever training a model. You give it structured JSON memory, and it gives your LLM meaningful context, fast.

No vector DBs. No finetuning. No heavy dependencies.

---

## ✨ Key Features

- ✅ Zero-database JSON-based retriever
- 🎯 Built on **BGE embeddings** (BAAI/bge-large-en-v1.5)
- ⏳ Fast top-k semantic matches
- 🔄 Memory tracking for context injection
- 💪 Works with **any** LLM (OpenAI, Mistral, local)
- 🙌 Great for agents, personal AIs, digital twins

---

## 🚀 Installation

```bash
pip install ragstruct .
```

---

## 📊 Use Case Examples

- 👤 Digital Twin memory retrieval (e.g., Joshi AI)
- 🧑‍💼 Resume bots and personal agent context
- 🧠 Mental health / therapy state tracking
- 🎓 LLM Study-buddy with syllabus JSON
- 📚 Retrieval-based storytelling agents
- 🎮 Game character memory/NPCs

---

## 🎡 Why ragstruct Exists

I (Joshikaran) built ragstruct while creating **Joshi AI**, a digital twin that could talk like me, remember my projects, reflect my mindset.

Every existing RAG pipeline felt like overkill. LangChain + vector DB + server just to search my own memory? Nah.

So I built this:

> “I wanted a RAG system that was so simple it could run in a terminal, speak like me, and understand what part of me it's referring to.”

---

## 🕵️‍♂️ When to Use ragstruct

Use ragstruct if:

- ✅ You have **structured memory or JSON knowledge**
- ✅ You want **fast retrieval** from text keys
- ✅ You want **context-aware LLMs** without training
- ✅ You care about **token savings** + control
- ✅ You’re building **personal AI or local agents**

---

## 🪖 How it Works (Pseudo-Finetuning)

Instead of retraining the model, you **remind** the model *what to say* by:

1. Embedding your JSON keys
2. Matching input queries to relevant memory
3. Injecting that into the LLM prompt

This creates the *effect* of fine-tuning, without touching weights.

---

## 📊 Comparison: Finetuning vs ragstruct

| Traditional Finetuning              | ragstruct (Pseudo)                       |
|------------------------------------|----------------------------------------|
| Requires large training data       | Works off your real JSON               |
| Needs GPUs, money, time            | Just Python + CPU                     |
| Locked once trained                | Dynamic memory updates                 |
| Expensive to iterate               | Instant memory edits                   |
| One model only                     | Use any LLM (local/cloud)              |

---

## 🔄 Smart Tips

### 🔄 Format Your JSON

Nested or list-heavy JSON? ragstruct flattens and formats it like this:

```json
{
  "name": "Felix AI",
  "description": "A crypto forecasting agent.",
  "tech_stack": ["Python", "XGBoost"]
}
```

...so your LLM sees clean chunks. Perfect for memory injection.

### 🧐 Compress Chat History

If injecting full chat is too heavy, summarize it:

```python
from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer(chat_text, max_length=100)[0]['summary_text']
```

---

## 🌐 Structuring Text into JSON (Optional)

Use the `Structurer` module to convert long `.txt` docs into structured JSON using any LLM:

```python
from ragstruct.structurer import Structurer
struct = Structurer(llm=your_llm)
structured = struct.structure_document("raw text block")
```

Handles chunking, cleaning, and LLM-guided structuring.

---

## ⚠️ What ragstruct *Is Not*

- Not a full generation pipeline — you supply the LLM
- Not multi-user scalable out of the box (but extendable)
- Not a replacement for real finetuning — it fakes it smartly

---

## 🔖 Summary

- 🔄 ragstruct injects only what matters
- ✅ JSON-only, no infra needed
- 🌍 Works with any LLM or chat agent
- 🚀 Fast, clean, dev-focused retrieval
- 🫠 Perfect for personal AI memory

> “Don’t train your model. Train your memory.” — Joshi Felix

---

Ready to build something with soul? Plug in your JSON, choose your LLM, and go.

Built with vim & vision by Joshi Felix.
