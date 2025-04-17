# ragstruct/setup_prompt.py
import sys
import time
import os
from sentence_transformers import SentenceTransformer

def animated_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def confirm_model_install():
    print("\n🔧 ragstruct Setup: Model Installation Guide\n")
    animated_print("📌 Default model: BAAI/bge-large-en-v1.5")
    animated_print("📦 Size         : ~1.5 GB")
    animated_print("🧠 Min RAM      : 4 GB (8 GB recommended)")
    animated_print("⏱️  Download time depends on your internet.\n")

    choice = input("❓ Do you want to install this model now? (Y/n): ").strip().lower()
    if choice in ["", "y", "yes"]:
        try:
            print("\n📥 Downloading model...")
            SentenceTransformer("BAAI/bge-large-en-v1.5")
            print("✅ Model installed successfully!\n")
        except Exception as e:
            print("❌ Failed to install model:", str(e))
    else:
        print("⚠️ Skipped model download. Make sure to install manually before using ragstruct.\n")

import subprocess

def post_install_message():
    print(r"""
🎵  ragstruct Installed Successfully!
--------------------------------------
📦 A Pseudo-Finetuning RAG Framework
💡 JSON-based memory, semantic retrieval
🔧 Optional: BGE model for embedding

Built by: Joshikaran K.
GitHub   : https://github.com/Joshikarank
""")

    choice = input("👉 Do you want to auto-install BGE (BAAI/bge-large-en-v1.5)? [Y/n]: ").strip().lower()
    
    if choice in ["y", "yes", ""]:
        print("⬇️ Installing BGE model via sentence-transformers...")
        subprocess.run(["python", "-c", "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-large-en-v1.5')"])
        print("✅ BGE installed successfully!\n")
    else:
        print("⚠️ Skipped BGE install. Please install manually if needed.\n")

if __name__ == "__main__":
    post_install_message()
    confirm_model_install()
