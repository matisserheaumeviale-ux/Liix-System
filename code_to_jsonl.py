import re
import json
import hashlib
import random
from pathlib import Path
from typing import List, Dict, Tuple

# ============================================================
# CONFIG
# ============================================================

SOURCE_DIR = Path("fichiers_sources")
OUTPUT_DIR = Path("output")

FINAL_FILE = OUTPUT_DIR / "dataset_stm32_matisse.jsonl"
TRAIN_FILE = OUTPUT_DIR / "train.jsonl"
VALID_FILE = OUTPUT_DIR / "valid.jsonl"
TEST_FILE = OUTPUT_DIR / "test.jsonl"
REJECT_FILE = OUTPUT_DIR / "rejected.jsonl"
REPORT_FILE = OUTPUT_DIR / "report.json"

VALID_EXTENSIONS = (
    ".c", ".h", ".md", ".txt", ".yaml", ".yml", ".mk"
)

MAX_CODE_CHARS = 2800
MAX_NOTE_CHARS = 1400
MIN_CHARS = 120
RANDOM_SEED = 42

SYSTEM_PROMPT = (
    "Tu es Liix-Code-Mini, un assistant spécialisé en STM32, C embarqué, "
    "ARM Cortex-M, HAL/LL, OpenOCD, Makefiles et architecture AFLC. "
    "Tu dois être précis, ne pas inventer de fonctions HAL, indiquer les hypothèses "
    "de clock/timer, distinguer HAL/LL/registres directs, et expliquer les risques embedded."
)

HAL_BLACKLIST = [
    "HAL_TIM_SetFrequency",
    "HAL_TIM_SetPWM",
    "HAL_PWM_Write",
    "HAL_StartTimerInterrupt",
    "HAL_TIM_StartInterrupt",
    "HAL_GPIO_Toggle",
]

BAD_DATASHEET_PATTERNS = [
    r"Peripheral Bus Register map",
    r"Reserved APB",
    r"0x400[0-9A-Fa-f]{4}",
    r"Section\s+\d+\.\d+",
    r"page\s+\d+",
]

STM32_KEYWORDS = [
    "HAL_", "GPIO", "TIM", "UART", "USART", "ADC", "DMA", "NVIC", "RCC",
    "STM32", "Cortex", "OpenOCD", "ST-Link", "STLINK",
    "arm-none-eabi", "Makefile", "htim", "huart", "hadc",
    "MX_", "SystemClock_Config",
    "HAL_TIM_PeriodElapsedCallback",
    "HAL_TIM_IC_CaptureCallback",
    "HAL_GPIO_WritePin",
    "GPIOA->", "GPIOB->", "GPIOC->",
    "AFLC", "PWM", "tach", "rpm", "Blue Pill"
]


# ============================================================
# BASIC CLEANING
# ============================================================

def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def clean_code_text(text: str) -> str:
    text = normalize_newlines(text)
    text = "\n".join(line.rstrip() for line in text.splitlines())
    text = re.sub(r"/\*[-*=\s]{20,}\*/", "/* --- */", text)
    text = re.sub(r"//[-*=]{20,}", "// ---", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_note_text(text: str) -> str:
    text = normalize_newlines(text)
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ============================================================
# FILE TYPE
# ============================================================

def is_valid_extension(path: Path) -> bool:
    if path.name.lower() == "makefile":
        return True
    return path.suffix.lower() in VALID_EXTENSIONS


def file_kind(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()

    if name == "makefile" or suffix == ".mk":
        return "MAKEFILE"
    if suffix == ".c":
        return "C_SOURCE"
    if suffix == ".h":
        return "C_HEADER"
    if suffix in [".yaml", ".yml"]:
        return "YAML"
    if suffix in [".md", ".txt"]:
        return "TECH_NOTE"
    return "UNKNOWN"


# ============================================================
# CLASSIFICATION
# ============================================================

def count_hits(text: str, keywords: List[str]) -> int:
    lower = text.lower()
    return sum(1 for k in keywords if k.lower() in lower)


def classify_category(text: str, path: Path) -> str:
    lower = text.lower()
    name = path.name.lower()

    timer_keywords = [
        "hal_tim",
        "tim_handletypedef",
        "psc",
        "arr",
        "prescaler",
        "autoreload",
        "periodelapsed",
        "hal_tim_base",
        "hal_tim_pwm",
        "hal_tim_ic",
        "__hal_tim_set_compare",
        "__hal_tim_set_counter",
        "__hal_tim_get_counter",
    ]

    pwm_keywords = [
        "pwm",
        "duty",
        "compare",
        "__hal_tim_set_compare",
        "ccr",
        "fan",
        "25khz",
        "25 khz",
    ]

    gpio_keywords = [
        "gpio",
        "hal_gpio",
        "gpioa->",
        "gpiob->",
        "gpioc->",
        "idr",
        "odr",
        "bsrr",
        "exti",
        "pull-up",
        "pull-down",
        "breadpin",
        "vwriteport",
    ]

    adc_keywords = [
        "adc",
        "hal_adc",
        "hadc",
        "adc raw",
        "temperature",
    ]

    uart_keywords = [
        "uart",
        "usart",
        "hal_uart",
        "huart",
        "printf-scanf",
    ]

    makefile_keywords = [
        "makefile",
        "arm-none-eabi",
        ".elf",
        ".bin",
        ".hex",
        "ldscript",
        "linker",
        "cflags",
        "ldflags",
    ]

    openocd_keywords = [
        "openocd",
        "st-link",
        "stlink",
        "target remote",
        "stm32f1x.cfg",
    ]

    aflc_keywords = [
        "aflc",
        "fan",
        "tach",
        "rpm",
        "ventilateur",
        "fan_pwm",
        "fan_tach",
    ]

    scores = {
        "TIMER": count_hits(text, timer_keywords),
        "PWM": count_hits(text, pwm_keywords),
        "GPIO": count_hits(text, gpio_keywords),
        "ADC": count_hits(text, adc_keywords),
        "UART": count_hits(text, uart_keywords),
        "MAKEFILE": count_hits(text, makefile_keywords),
        "OPENOCD": count_hits(text, openocd_keywords),
        "AFLC": count_hits(text, aflc_keywords),
    }

    if name == "makefile" or path.suffix.lower() == ".mk":
        return "MAKEFILE"

    if scores["OPENOCD"] >= 2:
        return "OPENOCD"

    if scores["MAKEFILE"] >= 2:
        return "MAKEFILE"

    if scores["AFLC"] >= 2:
        return "AFLC"

    if scores["PWM"] >= 2 and scores["TIMER"] >= 1:
        return "PWM"

    if scores["TIMER"] >= 2:
        return "TIMER"

    if scores["ADC"] >= 2:
        return "ADC"

    if scores["UART"] >= 2:
        return "UART"

    if scores["GPIO"] >= 2:
        return "GPIO"

    if path.suffix.lower() == ".h":
        return "HEADER"

    return "GENERAL_STM32"


def detect_mcu(text: str) -> str:
    patterns = [
        "STM32F103C8T6",
        "STM32F103",
        "STM32F1",
        "STM32F4",
        "STM32G0",
        "STM32",
    ]

    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return p

    return "Unknown"


# ============================================================
# REJECTION / QUALITY
# ============================================================

def looks_like_bad_datasheet_dump(text: str) -> bool:
    hits = 0

    for pattern in BAD_DATASHEET_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            hits += 1

    many_addresses = len(re.findall(r"0x400[0-9A-Fa-f]{4}", text)) >= 5

    return hits >= 2 or many_addresses


def has_blacklisted_hal(text: str) -> Tuple[bool, List[str]]:
    found = []

    for bad in HAL_BLACKLIST:
        if bad in text:
            found.append(bad)

    return len(found) > 0, found


def quality_score(text: str, path: Path, category: str) -> Tuple[int, List[str]]:
    score = 0
    reasons = []

    if len(text) >= MIN_CHARS:
        score += 10
    else:
        reasons.append("too_short")

    keyword_hits = sum(1 for k in STM32_KEYWORDS if k.lower() in text.lower())
    score += min(keyword_hits * 4, 32)

    if re.search(r"\bvoid\s+\w+\s*\(", text):
        score += 10

    if re.search(r"\b(static\s+)?(void|int|char|float|double|uint\d+_t|bool)\s+\w+\s*\(", text):
        score += 8

    if "HAL_" in text:
        score += 10

    if "SystemClock_Config" in text:
        score += 10

    if "MX_" in text:
        score += 8

    if "GPIOA->" in text or "GPIOB->" in text or "GPIOC->" in text:
        score += 8

    if "HAL_TIM_PeriodElapsedCallback" in text:
        score += 12

    if "HAL_TIM_PWM_Start" in text:
        score += 10

    if "HAL_GPIO_WritePin" in text:
        score += 8

    if "__HAL_TIM_SET_COMPARE" in text:
        score += 10

    if category == "TIMER" and any(x in text for x in ["PSC", "ARR", "Prescaler", "Period"]):
        score += 12

    if category == "MAKEFILE" and "arm-none-eabi" in text:
        score += 15

    if category == "OPENOCD" and "openocd" in text.lower():
        score += 15

    bad_hal, found = has_blacklisted_hal(text)

    if bad_hal:
        score -= 30
        for f in found:
            reasons.append(f"blacklisted_hal:{f}")

    if looks_like_bad_datasheet_dump(text):
        score -= 25
        reasons.append("bad_datasheet_dump")

    if path.suffix.lower() in [".c", ".h"]:
        if text.count("{") != text.count("}"):
            score -= 10
            reasons.append("brace_mismatch_possible")

    return max(score, 0), reasons


def should_reject(content: str, score: int, reasons: List[str]) -> bool:
    if len(content) < MIN_CHARS:
        return True

    if score < 28:
        return True

    if "bad_datasheet_dump" in reasons:
        return True

    if any(r.startswith("blacklisted_hal") for r in reasons):
        return True

    return False


# ============================================================
# CHUNKING / FUNCTION EXTRACTION
# ============================================================

def extract_c_functions(text: str) -> List[Dict[str, str]]:
    pattern = re.compile(
        r"""
        (?P<header>
            ^[a-zA-Z_][\w\s\*\(\),]*?
            \s+
            (?P<name>[a-zA-Z_]\w*)
            \s*\([^;]*?\)
        )
        \s*
        \{
        """,
        re.MULTILINE | re.VERBOSE,
    )

    results = []

    for match in pattern.finditer(text):
        name = match.group("name")

        if name in ["if", "while", "for", "switch"]:
            continue

        start = match.start()
        brace_start = text.find("{", match.end() - 1)

        if brace_start == -1:
            continue

        depth = 0
        end = None

        for i in range(brace_start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break

        if end:
            code = text[start:end].strip()
            if len(code) >= MIN_CHARS:
                results.append({
                    "name": name,
                    "code": code,
                })

    return results


def split_generic(content: str, max_chars: int) -> List[str]:
    paragraphs = content.split("\n\n")
    chunks = []
    current = ""

    for para in paragraphs:
        para = para.strip()

        if not para:
            continue

        if len(para) > max_chars:
            lines = para.splitlines()
            block = ""

            for line in lines:
                if len(block) + len(line) + 1 <= max_chars:
                    block += line + "\n"
                else:
                    if block.strip():
                        chunks.append(block.strip())
                    block = line + "\n"

            if block.strip():
                chunks.append(block.strip())

            continue

        if len(current) + len(para) + 2 <= max_chars:
            current += para + "\n\n"
        else:
            if current.strip():
                chunks.append(current.strip())
            current = para + "\n\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks


# ============================================================
# DATASET ENTRY
# ============================================================

def make_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def build_instruction(kind: str, category: str) -> str:
    if kind in ["C_SOURCE", "C_HEADER"]:
        return (
            f"Analyse ce segment de code STM32/C embarqué de catégorie {category}. "
            "Explique le rôle, les fonctions importantes, les dépendances HAL/LL/registres, "
            "les risques embedded et les améliorations possibles sans modifier la logique."
        )

    if kind == "MAKEFILE":
        return (
            "Analyse ce Makefile STM32/ARM GCC. Explique les flags, le linker script, "
            "la génération ELF/BIN/HEX, les risques de compilation et les bonnes pratiques."
        )

    if category == "TIMER":
        return (
            "Analyse ce contenu STM32 lié aux timers. Vérifie les hypothèses de clock, "
            "PSC/ARR, fréquence, période, interruptions, PWM ou input capture."
        )

    if category == "GPIO":
        return (
            "Analyse ce contenu STM32 lié aux GPIO. Vérifie les modes entrée/sortie, "
            "pull-up/pull-down, limites 3.3 V/5 V, courant maximal, EXTI et accès registre."
        )

    return (
        "Analyse ce contenu technique STM32 et transforme-le en connaissance utile "
        "pour un assistant IA local spécialisé en C embarqué."
    )


def build_expected_output(category: str) -> str:
    outputs = {
        "TIMER": (
            "Analyse technique STM32 timer.\n"
            "- Identifier les timers utilisés\n"
            "- Vérifier PSC/ARR si présents\n"
            "- Expliquer la fréquence timer et la période\n"
            "- Mentionner le risque APB prescaler/timer clock doublée\n"
            "- Identifier interruptions, PWM ou input capture\n"
            "- Ne pas inventer de fonctions HAL"
        ),
        "PWM": (
            "Analyse technique PWM STM32.\n"
            "- Identifier le timer et le canal PWM\n"
            "- Vérifier la fréquence PWM\n"
            "- Expliquer duty cycle, ARR et CCR\n"
            "- Mentionner les risques pour ventilateur 4 pins\n"
            "- Ne pas inventer de fonctions HAL"
        ),
        "GPIO": (
            "Analyse technique GPIO STM32.\n"
            "- Identifier les ports et broches utilisés\n"
            "- Vérifier entrée/sortie, pull-up/pull-down\n"
            "- Mentionner les limites 3.3 V et tolérance 5 V\n"
            "- Vérifier les risques de courant maximal\n"
            "- Distinguer HAL et accès registre direct"
        ),
        "ADC": (
            "Analyse technique ADC STM32.\n"
            "- Identifier l'ADC et le canal\n"
            "- Vérifier résolution, référence et conversion\n"
            "- Expliquer le traitement de valeur brute\n"
            "- Mentionner les risques d'échelle et de calibration"
        ),
        "UART": (
            "Analyse technique UART/USART STM32.\n"
            "- Identifier USART utilisé\n"
            "- Vérifier baudrate et pins TX/RX\n"
            "- Expliquer transmission/réception\n"
            "- Mentionner les risques de blocage et buffer"
        ),
        "MAKEFILE": (
            "Analyse technique Makefile STM32.\n"
            "- Vérifier arm-none-eabi-gcc\n"
            "- Vérifier flags Cortex-M\n"
            "- Vérifier includes et sources\n"
            "- Vérifier linker script\n"
            "- Vérifier génération ELF/BIN/HEX et arm-none-eabi-size"
        ),
        "OPENOCD": (
            "Analyse technique OpenOCD/ST-Link.\n"
            "- Identifier interface et target cfg\n"
            "- Vérifier commande flash/program/verify/reset\n"
            "- Vérifier GDB target remote si présent\n"
            "- Mentionner risques de mauvais target STM32"
        ),
        "AFLC": (
            "Analyse technique AFLC.\n"
            "- Identifier PWM fan, tach, LCD, UART ou capteurs\n"
            "- Vérifier architecture STM32F103 Blue Pill\n"
            "- Mentionner risques hardware/software\n"
            "- Proposer améliorations conservatrices"
        ),
    }

    return outputs.get(
        category,
        (
            "Analyse technique STM32 embarqué.\n"
            "- Identifier les périphériques STM32\n"
            "- Identifier les dépendances HAL/LL/registres\n"
            "- Identifier les risques embedded\n"
            "- Proposer des améliorations sans inventer de code"
        ),
    )


def wrap_code_block(content: str, kind: str) -> str:
    if kind in ["C_SOURCE", "C_HEADER"]:
        lang = "c"
    elif kind == "MAKEFILE":
        lang = "makefile"
    elif kind == "YAML":
        lang = "yaml"
    else:
        lang = "text"

    return f"```{lang}\n{content}\n```"


def build_entry(
    path: Path,
    content: str,
    part: str,
    kind: str,
    category: str,
    score: int,
    reasons: List[str],
) -> Dict:
    mcu = detect_mcu(content)

    user_prompt = (
        f"{build_instruction(kind, category)}\n\n"
        f"Fichier: {path.name}\n"
        f"Chemin: {str(path)}\n"
        f"Type: {kind}\n"
        f"Catégorie: {category}\n"
        f"MCU: {mcu}\n"
        f"Partie: {part}\n"
        f"Score qualité: {score}\n\n"
        f"{wrap_code_block(content, kind)}"
    )

    return {
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
            {
                "role": "assistant",
                "content": build_expected_output(category),
            },
        ],
        "metadata": {
            "file": path.name,
            "path": str(path),
            "kind": kind,
            "category": category,
            "mcu": mcu,
            "part": part,
            "quality_score": score,
            "reasons": reasons,
            "hash": make_hash(content),
        },
    }


# ============================================================
# COLLECT
# ============================================================

def collect_entries() -> Tuple[List[Dict], List[Dict]]:
    entries = []
    rejected = []
    seen_hashes = set()

    for path in SOURCE_DIR.rglob("*"):
        if not path.is_file() or not is_valid_extension(path):
            continue

        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
            kind = file_kind(path)

            if kind in ["C_SOURCE", "C_HEADER", "MAKEFILE"]:
                cleaned = clean_code_text(raw)
            else:
                cleaned = clean_note_text(raw)

            if not cleaned:
                continue

            chunks = []

            if kind in ["C_SOURCE", "C_HEADER"]:
                functions = extract_c_functions(cleaned)

                for f in functions:
                    chunks.append((f"function:{f['name']}", f["code"]))

                if len(cleaned) <= MAX_CODE_CHARS:
                    chunks.insert(0, ("full_file", cleaned))
                else:
                    parts = split_generic(cleaned, MAX_CODE_CHARS)
                    for i, part in enumerate(parts):
                        chunks.append((f"file_part:{i + 1}", part))

            elif kind == "TECH_NOTE":
                parts = split_generic(cleaned, MAX_NOTE_CHARS)
                for i, part in enumerate(parts):
                    chunks.append((f"note_part:{i + 1}", part))

            else:
                parts = split_generic(cleaned, MAX_CODE_CHARS)
                for i, part in enumerate(parts):
                    chunks.append((f"part:{i + 1}", part))

            for part_name, chunk in chunks:
                h = make_hash(chunk)

                if h in seen_hashes:
                    continue

                seen_hashes.add(h)

                category = classify_category(chunk, path)
                score, reasons = quality_score(chunk, path, category)

                entry = build_entry(
                    path=path,
                    content=chunk,
                    part=part_name,
                    kind=kind,
                    category=category,
                    score=score,
                    reasons=reasons,
                )

                if should_reject(chunk, score, reasons):
                    rejected.append(entry)
                else:
                    entries.append(entry)

        except Exception as e:
            rejected.append({
                "error": str(e),
                "path": str(path),
            })

    return entries, rejected


# ============================================================
# SAVE / SPLIT / REPORT
# ============================================================

def save_jsonl(path: Path, rows: List[Dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            json.dump(row, f, ensure_ascii=False)
            f.write("\n")


def split_dataset(entries: List[Dict]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    random.seed(RANDOM_SEED)
    shuffled = entries[:]
    random.shuffle(shuffled)

    total = len(shuffled)
    train_end = int(total * 0.85)
    valid_end = int(total * 0.95)

    return (
        shuffled[:train_end],
        shuffled[train_end:valid_end],
        shuffled[valid_end:],
    )


def generate_report(entries: List[Dict], rejected: List[Dict]) -> Dict:
    by_category = {}
    by_kind = {}
    scores = []

    for e in entries:
        meta = e.get("metadata", {})
        category = meta.get("category", "UNKNOWN")
        kind = meta.get("kind", "UNKNOWN")
        score = meta.get("quality_score", 0)

        by_category[category] = by_category.get(category, 0) + 1
        by_kind[kind] = by_kind.get(kind, 0) + 1
        scores.append(score)

    avg_score = sum(scores) / len(scores) if scores else 0

    return {
        "accepted_entries": len(entries),
        "rejected_entries": len(rejected),
        "average_quality_score": round(avg_score, 2),
        "by_category": by_category,
        "by_kind": by_kind,
        "output_files": {
            "final": str(FINAL_FILE),
            "train": str(TRAIN_FILE),
            "valid": str(VALID_FILE),
            "test": str(TEST_FILE),
            "rejected": str(REJECT_FILE),
            "report": str(REPORT_FILE),
        },
    }


def generate_dataset() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    entries, rejected = collect_entries()
    train, valid, test = split_dataset(entries)

    save_jsonl(FINAL_FILE, entries)
    save_jsonl(TRAIN_FILE, train)
    save_jsonl(VALID_FILE, valid)
    save_jsonl(TEST_FILE, test)
    save_jsonl(REJECT_FILE, rejected)

    report = generate_report(entries, rejected)

    with REPORT_FILE.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("Dataset généré")
    print(f"Acceptés : {len(entries)}")
    print(f"Rejetés  : {len(rejected)}")
    print(f"Train    : {len(train)}")
    print(f"Valid    : {len(valid)}")
    print(f"Test     : {len(test)}")
    print(f"Score moyen : {report['average_quality_score']}")
    print(f"Fichier : {FINAL_FILE}")
    print(f"Rapport : {REPORT_FILE}")


if __name__ == "__main__":
    generate_dataset()