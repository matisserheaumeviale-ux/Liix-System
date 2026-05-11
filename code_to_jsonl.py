import os
import json
import re
from pathlib import Path

SOURCE_DIR = Path("fichiers_sources")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "dataset_stm32_matisse.jsonl"

VALID_EXTENSIONS = (".c", ".h", ".yaml", ".yml", ".txt", ".md")

def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def split_content(content: str, max_chars: int = 1800):
    paragraphs = content.split("\n\n")
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= max_chars:
            current += para + "\n\n"
        else:
            if current.strip():
                chunks.append(current.strip())
            current = para + "\n\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks

def classify_file(file: str):
    if file.endswith((".c", ".h")):
        return "Source Code", "Analyse ce segment de code C/C++ STM32. Explique son rôle, les fonctions importantes, les risques et les améliorations possibles."
    if file.endswith((".yaml", ".yml")):
        return "Hardware Register Data", "Analyse ces données matérielles STM32. Explique les registres, offsets, champs importants et leur utilité en C embarqué."
    if file.endswith((".md", ".txt")):
        return "Academic Note", "Résume cette note technique et transforme-la en connaissances utiles pour programmer un STM32."
    return "Unknown", "Analyse ce contenu pour un projet STM32."

def is_bad_chunk(chunk: str):
    if len(chunk) < 80:
        return True
    if chunk.count("{") > 20 and len(chunk) < 500:
        return False
    return False

def generate_dataset():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    with OUTPUT_FILE.open("w", encoding="utf-8") as outfile:
        for path in SOURCE_DIR.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in VALID_EXTENSIONS:
                continue

            try:
                raw_content = path.read_text(encoding="utf-8", errors="ignore")
                raw_content = clean_text(raw_content)

                if len(raw_content) < 80:
                    continue

                chunks = split_content(raw_content, max_chars=1800)
                type_info, instruction = classify_file(path.name)

                for i, chunk in enumerate(chunks):
                    if is_bad_chunk(chunk):
                        continue

                    entry = {
                        "instruction": instruction,
                        "input": f"File: {path.name}\nType: {type_info}\nPart: {i+1}/{len(chunks)}\n\n{chunk}",
                        "output": "Explique ce contenu de manière claire, technique et orientée STM32. Identifie les éléments importants, les risques possibles et comment l'utiliser dans un projet embarqué."
                    }

                    json.dump(entry, outfile, ensure_ascii=False)
                    outfile.write("\n")
                    count += 1

            except Exception as e:
                print(f"Erreur sur {path}: {e}")

    print(f"Dataset généré : {count} entrées")
    print(f"Fichier : {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_dataset()