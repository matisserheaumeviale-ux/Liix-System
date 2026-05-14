import hashlib
import json
import re
import shutil
import statistics
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


SOURCE_DIR = Path("fichiers_sources")
OUTPUT_DIR = Path("output")

SYSTEM_PROMPT = (
    "Tu es Liix-Code-0.2, un assistant spécialisé en STM32, C embarqué, "
    "ARM Cortex-M, HAL/LL, OpenOCD, Makefiles, VSCode, GitHub et architecture AFLC. "
    "Tu dois être précis, ne pas inventer de fonctions HAL, indiquer les hypothèses "
    "de clock/timer, distinguer HAL/LL/registres directs, et expliquer les risques embedded."
)

BASE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
OUTPUT_MODEL = "liix-code-0.2"

FINAL_FILE = OUTPUT_DIR / "liix_code_0_2_dataset.jsonl"
AGENTIC_FILE = OUTPUT_DIR / "dataset_agentic.jsonl"
IOC_FILE = OUTPUT_DIR / "dataset_ioc.jsonl"
REJECTED_FILE = OUTPUT_DIR / "rejected.jsonl"
REPORT_FILE = OUTPUT_DIR / "report.json"
TRAIN_FILE = OUTPUT_DIR / "liix_code_0_2_train.jsonl"
VALID_FILE = OUTPUT_DIR / "liix_code_0_2_valid.jsonl"
TEST_FILE = OUTPUT_DIR / "liix_code_0_2_test.jsonl"

VALID_EXTENSIONS = (".c", ".h", ".yaml", ".yml", ".txt", ".md", ".ioc")
MAX_FILE_BYTES = 1_000_000
MIN_CHUNK_CHARS = 80
MAX_CHUNK_CHARS = 2200
ENABLE_SYNTAX_CHECK = False

BAD_HAL_PATTERNS = [
    re.compile(r"\bHAL_TIM_SetFrequency\b"),
    re.compile(r"\bHAL_TIM_SetPWM\b"),
    re.compile(r"\bHAL_TIM_PWM_SetDuty\b"),
    re.compile(r"\bHAL_GPIO_SetPin\b"),
    re.compile(r"\bHAL_UART_Printf\b"),
    re.compile(r"\bHAL_Delay_us\b"),
    re.compile(r"\bHAL_ADC_Read\b"),
]

PROMPT_VARIANTS = {
    "analyse_code": [
        "Analyse ce fragment STM32 et identifie les périphériques, appels HAL/LL, paramètres critiques et risques embarqués.",
        "Fais une revue technique de ce code STM32 en restant strictement fidèle au contenu fourni.",
    ],
    "debug_code": [
        "Repère les erreurs probables, angles morts et hypothèses manquantes dans ce fragment STM32.",
        "Aide à déboguer ce code embarqué: symptômes possibles, causes plausibles et vérifications conservatrices.",
    ],
    "explique_code": [
        "Explique ce fragment à un étudiant en STM32, avec les points importants pour C embarqué.",
        "Décris le rôle du code et les notions STM32 utiles sans inventer d'API absente.",
    ],
    "améliore_code": [
        "Propose des améliorations conservatrices pour ce fragment STM32 sans changer son intention.",
        "Suggère une version plus robuste ou plus lisible, en signalant ce qui doit être vérifié sur la carte.",
    ],
    "convertis_en_notes": [
        "Transforme ce contenu en notes de cours STM32 concises et actionnables.",
        "Résume ce passage en mémo technique pour un projet STM32 HAL/LL.",
    ],
    "question_reponse": [
        "Réponds comme dans une séance de tutorat STM32 à partir du contenu fourni.",
        "Formule une réponse courte et technique à une question d'étudiant sur ce fragment.",
    ],
    "agentic_tool_use": [
        "Utilise des outils de développement pour inspecter, compiler et proposer une correction STM32.",
    ],
}

PERIPHERAL_WORDS = (
    "GPIO",
    "UART",
    "USART",
    "TIM",
    "ADC",
    "DMA",
    "NVIC",
    "RCC",
    "I2C",
    "SPI",
    "EXTI",
    "OpenOCD",
    "GDB",
    "Makefile",
    "PWM",
)


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def is_probably_binary(path: Path, sample_size: int = 4096) -> bool:
    try:
        data = path.read_bytes()[:sample_size]
    except OSError:
        return True
    if not data:
        return False
    if b"\x00" in data:
        return True
    control = sum(1 for b in data if b < 9 or (13 < b < 32))
    return control / max(len(data), 1) > 0.20


def reject_record(path: Path, reason: str, detail: str = "") -> dict:
    return {
        "path": str(path),
        "extension": path.suffix.lower(),
        "reason": reason,
        "detail": detail,
        "size_bytes": path.stat().st_size if path.exists() else None,
    }


def safe_read_text(path: Path):
    size = path.stat().st_size
    if size > MAX_FILE_BYTES:
        return None, reject_record(path, "file_too_large", f">{MAX_FILE_BYTES} bytes")
    if is_probably_binary(path):
        return None, reject_record(path, "probably_binary")
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1"), None
        except UnicodeDecodeError as exc:
            return None, reject_record(path, "decode_error", str(exc))
    except OSError as exc:
        return None, reject_record(path, "read_error", str(exc))


def clean_cubemx_boilerplate(text: str) -> str:
    text = normalize_newlines(text)
    text = re.sub(r"/\*\s*USER CODE BEGIN [^*]*\*/", "", text)
    text = re.sub(r"/\*\s*USER CODE END [^*]*\*/", "", text)
    text = re.sub(r"/\*={3,}.*?={3,}\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"/\*\*[\s\S]{0,4000}?(?:@file|@brief)[\s\S]*?\*/", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*/\*+\s*$|^\s*\*+\s*/\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\*\s*(?:Copyright|All rights reserved|Licensed|Redistribution).*?$", "", text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r"^\s*(?:static\s+)?void\s+\w+\s*\([^;{}]*\);\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*/\* Private (?:includes|typedef|define|macro|variables|function prototypes|user code).*?\*/\s*$", "", text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    return text.strip()


def clean_text(text: str, suffix: str = "") -> str:
    text = normalize_newlines(text)
    if suffix.lower() in (".c", ".h"):
        text = clean_cubemx_boilerplate(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_content(content: str, max_chars: int = MAX_CHUNK_CHARS):
    paragraphs = re.split(r"\n\s*\n", content)
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(para) > max_chars:
            if current.strip():
                chunks.append(current.strip())
                current = ""
            for start in range(0, len(para), max_chars):
                chunks.append(para[start : start + max_chars].strip())
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


def classify_file(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".ioc":
        return "IOC_CONFIG", "CubeMX IOC configuration"
    if suffix in (".c", ".h"):
        return "SOURCE_CODE", "STM32 C/H source"
    if suffix in (".yaml", ".yml"):
        return "REGISTER_DATA", "STM32 register data"
    if suffix in (".md", ".txt"):
        return "TECHNICAL_NOTE", "STM32 technical note"
    return "UNKNOWN", "STM32 content"


def has_bad_hal(text: str):
    return [pattern.pattern.strip(r"\b") for pattern in BAD_HAL_PATTERNS if pattern.search(text)]


def extract_analysis(content: str, kind: str) -> dict:
    hal_functions = sorted(set(re.findall(r"\bHAL_[A-Za-z0-9_]+\b", content)))
    ll_functions = sorted(set(re.findall(r"\bLL_[A-Za-z0-9_]+\b", content)))
    callbacks = sorted(set(re.findall(r"\bHAL_[A-Za-z0-9_]+Callback\b", content)))
    timers = sorted(set(re.findall(r"\bTIM\d+\b|\bhtim\d+\b", content, flags=re.IGNORECASE)))
    uart = sorted(set(re.findall(r"\bUSART\d+\b|\bUART\d+\b|\bhuart\d+\b", content, flags=re.IGNORECASE)))
    gpio_pins = sorted(set(re.findall(r"\bGPIO_PIN_(?:\d+|All)\b|\bP[A-K]\d{1,2}\b", content)))
    gpio_ports = sorted(set(re.findall(r"\bGPIO[A-K]\b", content)))
    psc = sorted(set(re.findall(r"\b(?:PSC|Prescaler|\.Prescaler)\s*[=:]\s*([A-Za-z0-9_+\-*/()]+)", content)))
    arr = sorted(set(re.findall(r"\b(?:ARR|Period|\.Period)\s*[=:]\s*([A-Za-z0-9_+\-*/()]+)", content)))
    ccr = sorted(set(re.findall(r"\b(?:CCR[1-4]?|Pulse|\.Pulse)\s*[=:]\s*([A-Za-z0-9_+\-*/()]+)", content)))
    peripherals = sorted({word for word in PERIPHERAL_WORDS if re.search(rf"\b{re.escape(word)}\b", content, flags=re.IGNORECASE)})

    risks = []
    if "while" in content and "HAL_Delay" not in content and ("HAL_GPIO" in content or "HAL_UART" in content):
        risks.append("boucle potentiellement bloquante ou cadence non explicite")
    if "HAL_Delay" in content:
        risks.append("temporisation bloquante qui peut masquer des problèmes temps réel")
    if "HAL_UART_Transmit" in content and "HAL_MAX_DELAY" in content:
        risks.append("transmission UART bloquante avec timeout infini")
    if "PWM" in content.upper() or ccr:
        risks.append("vérifier cohérence fréquence PWM, rapport cyclique et résolution ARR/CCR")
    if "volatile" not in content and ("IRQHandler" in content or callbacks):
        risks.append("variables partagées interruption/main à protéger ou déclarer volatile si nécessaire")
    if "SystemClock_Config" in content or "RCC" in peripherals:
        risks.append("confirmer la fréquence horloge utilisée dans les calculs de timers")

    missing = []
    if timers and not psc and not arr:
        missing.append("valeurs PSC/ARR ou fréquence timer")
    if gpio_pins and not gpio_ports:
        missing.append("port GPIO exact ou mode de configuration")
    if uart and "BaudRate" not in content:
        missing.append("baudrate et configuration UART")
    if kind == "IOC_CONFIG" and "Mcu.Name" not in content:
        missing.append("référence MCU complète")

    return {
        "peripherals": peripherals,
        "hal_functions": hal_functions,
        "ll_functions": ll_functions,
        "callbacks": callbacks,
        "timers": timers,
        "uart": uart,
        "gpio_pins": gpio_pins,
        "gpio_ports": gpio_ports,
        "psc": psc,
        "arr": arr,
        "ccr": ccr,
        "risks": risks,
        "missing": missing,
    }


def short_list(values, limit=8):
    if not values:
        return "aucun élément explicite"
    shown = values[:limit]
    suffix = "" if len(values) <= limit else f", +{len(values) - limit}"
    return ", ".join(shown) + suffix


def build_assistant_answer(content: str, category: str, kind: str) -> str:
    info = extract_analysis(content, kind)
    lines = [
        f"Analyse {category}: le fragment contient surtout {short_list(info['peripherals'])}.",
    ]
    if info["hal_functions"]:
        lines.append(f"Fonctions HAL détectées: {short_list(info['hal_functions'])}.")
    if info["ll_functions"]:
        lines.append(f"Fonctions LL détectées: {short_list(info['ll_functions'])}.")
    if info["timers"] or info["psc"] or info["arr"] or info["ccr"]:
        lines.append(
            "Timers/PWM: "
            f"timers={short_list(info['timers'], 6)}, "
            f"PSC={short_list(info['psc'], 4)}, ARR={short_list(info['arr'], 4)}, CCR/Pulse={short_list(info['ccr'], 4)}."
        )
    if info["gpio_pins"] or info["gpio_ports"]:
        lines.append(f"GPIO: ports={short_list(info['gpio_ports'], 6)}, pins={short_list(info['gpio_pins'], 10)}.")
    if info["callbacks"]:
        lines.append(f"Callbacks HAL présents: {short_list(info['callbacks'])}; vérifier le contexte interruption et la durée d'exécution.")
    if kind == "IOC_CONFIG":
        ioc = parse_ioc_config(content)
        lines.append(
            "Configuration CubeMX: "
            f"MCU={ioc.get('mcu') or 'non indiqué'}, pins={short_list(ioc['pins'], 8)}, "
            f"clocks={short_list(ioc['clocks'], 5)}, timers={short_list(ioc['timers'], 5)}, "
            f"UART={short_list(ioc['uart'], 5)}, ADC={short_list(ioc['adc'], 5)}, "
            f"DMA={short_list(ioc['dma'], 5)}, NVIC={short_list(ioc['nvic'], 5)}."
        )
    if info["risks"]:
        lines.append("Risques embedded: " + "; ".join(info["risks"]) + ".")
    else:
        lines.append("Risques embedded: vérifier tout de même horloges, timeouts, initialisation GPIO et contraintes temps réel.")
    if info["missing"]:
        lines.append("Hypothèses manquantes: " + "; ".join(info["missing"]) + ".")
    lines.append(
        "Corrections conservatrices: valider les horloges réelles, garder les timeouts bornés, "
        "documenter les unités PSC/ARR/CCR, et ne modifier que les paramètres confirmés par la carte et le schéma."
    )
    return "\n".join(lines)


def parse_ioc_config(content: str) -> dict:
    data = {}
    for line in normalize_newlines(content).splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    keys = list(data.keys())
    values = list(data.values())
    joined = "\n".join(f"{k}={v}" for k, v in data.items())
    pins = sorted(set(re.findall(r"\bP[A-K]\d{1,2}\b", joined)))
    return {
        "mcu": data.get("Mcu.Name") or data.get("Mcu.Family") or data.get("ProjectManager.DeviceId"),
        "pins": pins,
        "clocks": sorted(set(k for k in keys if "RCC" in k or "Clock" in k))[:20],
        "timers": sorted(set(re.findall(r"\bTIM\d+\b", joined)))[:20],
        "uart": sorted(set(re.findall(r"\b(?:USART|UART)\d+\b", joined)))[:20],
        "adc": sorted(set(re.findall(r"\bADC\d*\b", joined)))[:20],
        "dma": sorted(set(k for k in keys + values if "DMA" in k))[:20],
        "nvic": sorted(set(k for k in keys if "NVIC" in k))[:20],
    }


def prompt_for_variant(variant: str, index: int) -> str:
    options = PROMPT_VARIANTS[variant]
    return options[index % len(options)]


def make_messages(content: str, category: str, kind: str, variant: str, index: int):
    instruction = prompt_for_variant(variant, index)
    if variant == "question_reponse":
        instruction = "Question: que faut-il vérifier en priorité dans ce fragment STM32?"
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"{instruction}\n\nType: {kind}\nCatégorie: {category}\n\n{content}"},
        {"role": "assistant", "content": build_assistant_answer(content, category, kind)},
    ]


def quality_score(content: str, category: str, kind: str) -> int:
    score = 0
    lower = content.lower()
    if len(content) >= MIN_CHUNK_CHARS:
        score += 10
    if re.search(r"\b(?:int|void|static|uint\d+_t|#include)\b", content):
        score += 15
    if re.search(r"\bHAL_[A-Za-z0-9_]+Callback\b", content):
        score += 15
    if re.search(r"\b(?:PSC|ARR|CCR[1-4]?|Prescaler|Period|Pulse)\b", content):
        score += 14
    if re.search(r"\b(?:openocd|gdb|arm-none-eabi|make)\b", lower):
        score += 12
    if re.search(r"\bHAL_[A-Za-z0-9_]+\b|\bLL_[A-Za-z0-9_]+\b", content):
        score += 12
    if re.search(r"\bGPIO_PIN_\d+\b|\bTIM\d+\b|\bUSART\d+\b|\bADC\d+\b", content):
        score += 10
    if kind == "IOC_CONFIG":
        score += 12
    if content.count("USER CODE") > 4 or content.count("/*") > 20:
        score -= 12
    if len(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", content)) < 20:
        score -= 10
    if category == "TECHNICAL_NOTE" and not re.search(r"\b(?:STM32|GPIO|timer|UART|HAL|OpenOCD|Makefile)\b", content, re.IGNORECASE):
        score -= 15
    return max(0, min(100, score))


def syntax_check(path: Path):
    if not ENABLE_SYNTAX_CHECK or path.suffix.lower() not in (".c", ".h"):
        return {"syntax_ok": None, "syntax_error": None}
    compiler = shutil.which("arm-none-eabi-gcc") or shutil.which("clang")
    if not compiler:
        return {"syntax_ok": None, "syntax_error": "compiler_not_found"}
    args = [compiler, "-fsyntax-only", str(path)]
    if Path(compiler).name.startswith("clang"):
        args.insert(1, "-x")
        args.insert(2, "c")
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=12)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"syntax_ok": None, "syntax_error": str(exc)}
    return {"syntax_ok": proc.returncode == 0, "syntax_error": proc.stderr.strip()[:1200] if proc.returncode else None}


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def file_key(path: Path, content: str) -> str:
    h = hashlib.sha256()
    h.update(str(path).replace("\\", "/").lower().encode("utf-8"))
    h.update(b"\0")
    h.update(content[:4096].encode("utf-8", errors="ignore"))
    return h.hexdigest()


def split_name(key: str) -> str:
    bucket = int(key[:8], 16) % 100
    if bucket < 85:
        return "train"
    if bucket < 95:
        return "valid"
    return "test"


def assign_file_splits(rows) -> dict:
    """Split by source file hash so one file never leaks across splits."""
    keys = sorted({row["metadata"]["file_hash"] for row in rows})
    if not keys:
        return {}
    if len(keys) == 1:
        mapping = {keys[0]: "train"}
    elif len(keys) == 2:
        mapping = {keys[0]: "train", keys[1]: "valid"}
    else:
        train_end = max(1, int(len(keys) * 0.85))
        valid_end = max(train_end + 1, int(len(keys) * 0.95))
        if valid_end >= len(keys):
            valid_end = len(keys) - 1
            train_end = min(train_end, valid_end - 1)
        mapping = {}
        for index, key in enumerate(keys):
            if index < train_end:
                mapping[key] = "train"
            elif index < valid_end:
                mapping[key] = "valid"
            else:
                mapping[key] = "test"
    for row in rows:
        row["metadata"]["split"] = mapping[row["metadata"]["file_hash"]]
    return mapping


def build_entry(path: Path, content: str, chunk: str, index: int, total: int, variant: str, category: str, kind: str, syntax_meta: dict):
    key = file_key(path, content)
    score = quality_score(chunk, category, kind)
    metadata = {
        "source_path": str(path),
        "file_name": path.name,
        "file_hash": key,
        "split": split_name(key),
        "part": index + 1,
        "parts": total,
        "category": category,
        "kind": kind,
        "prompt_variant": variant,
        "quality_score": score,
        "estimated_tokens": estimate_tokens(chunk),
        **syntax_meta,
    }
    return {"messages": make_messages(chunk, category, kind, variant, index), "metadata": metadata}


def build_agentic_example(path: Path, content: str, category: str, kind: str, index: int) -> dict:
    snippet = content[:900]
    grep_query = "HAL_" if "HAL_" in content else ("TIM" if "TIM" in content else path.stem)
    tools = [
        {"type": "function", "function": {"name": "read_file", "description": "Lire un fichier du projet.", "parameters": {"type": "object"}}},
        {"type": "function", "function": {"name": "search_text", "description": "Chercher du texte dans le projet.", "parameters": {"type": "object"}}},
        {"type": "function", "function": {"name": "run_make", "description": "Lancer make et retourner stdout/stderr.", "parameters": {"type": "object"}}},
        {"type": "function", "function": {"name": "analyze_gcc_errors", "description": "Classer les erreurs GCC/linker/OpenOCD.", "parameters": {"type": "object"}}},
        {"type": "function", "function": {"name": "propose_patch", "description": "Proposer un patch minimal sans modifier le comportement voulu.", "parameters": {"type": "object"}}},
        {"type": "function", "function": {"name": "run_test", "description": "Lancer un test logiciel ou une vérification matérielle ciblée.", "parameters": {"type": "object"}}},
        {"type": "function", "function": {"name": "create_github_issue", "description": "Créer une issue GitHub avec un diagnostic.", "parameters": {"type": "object"}}},
    ]
    messages = [
        {"role": "system", "content": "Tu es un agent STM32 prudent. Utilise les outils puis propose un patch minimal."},
        {"role": "user", "content": f"Inspecte {path.name}, cherche les API importantes, lance make, analyse les erreurs GCC et prépare une issue si nécessaire."},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {"id": "call_read_file", "type": "function", "function": {"name": "read_file", "arguments": json.dumps({"path": str(path)})}},
                {"id": "call_search_text", "type": "function", "function": {"name": "search_text", "arguments": json.dumps({"query": grep_query, "path": str(path.parent)})}},
            ],
        },
        {"role": "tool", "tool_call_id": "call_read_file", "name": "read_file", "content": snippet},
        {"role": "tool", "tool_call_id": "call_search_text", "name": "search_text", "content": f"Recherche suggérée: {grep_query} dans {path.parent}."},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {"id": "call_run_make", "type": "function", "function": {"name": "run_make", "arguments": json.dumps({"target": "all"})}}
            ],
        },
        {"role": "tool", "tool_call_id": "call_run_make", "name": "run_make", "content": "Résultat simulé pour dataset: analyser stdout/stderr GCC, OpenOCD ou linker avant de patcher."},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {"id": "call_analyze_gcc", "type": "function", "function": {"name": "analyze_gcc_errors", "arguments": json.dumps({"stderr": "stdout/stderr de make", "context": str(path)})}},
                {"id": "call_propose_patch", "type": "function", "function": {"name": "propose_patch", "arguments": json.dumps({"path": str(path), "strategy": "minimal_conservative"})}},
            ],
        },
        {"role": "tool", "tool_call_id": "call_analyze_gcc", "name": "analyze_gcc_errors", "content": "Classer d'abord include manquant, symbole non défini, erreur de type, script linker ou cible OpenOCD."},
        {"role": "tool", "tool_call_id": "call_propose_patch", "name": "propose_patch", "content": "Patch minimal proposé dans le dataset: corriger seulement la cause confirmée et garder les API HAL réellement présentes."},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {"id": "call_run_test", "type": "function", "function": {"name": "run_test", "arguments": json.dumps({"kind": "build_or_board_smoke_test"})}},
                {"id": "call_create_issue", "type": "function", "function": {"name": "create_github_issue", "arguments": json.dumps({"title": f"Diagnostic STM32: {path.name}", "labels": ["stm32", "build", "diagnostic"]})}},
            ],
        },
        {"role": "tool", "tool_call_id": "call_run_test", "name": "run_test", "content": "Test recommandé: relancer make, flasher si possible, vérifier UART/GPIO/timer concerné."},
        {"role": "tool", "tool_call_id": "call_create_issue", "name": "create_github_issue", "content": "Issue préparée avec contexte, commandes, erreur observée, analyse et patch minimal."},
        {"role": "assistant", "content": build_assistant_answer(snippet, category, kind) + "\nPatch proposé: isoler la cause, modifier le minimum, puis relancer make et un test matériel ciblé."},
    ]
    key = file_key(path, content)
    return {
        "messages": messages,
        "tools": tools,
        "metadata": {
            "source_path": str(path),
            "file_hash": key,
            "split": split_name(key),
            "category": category,
            "kind": kind,
            "prompt_variant": "agentic_tool_use",
            "quality_score": quality_score(snippet, category, kind),
            "agentic_index": index,
        },
    }


def write_jsonl(path: Path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            json.dump(row, handle, ensure_ascii=False)
            handle.write("\n")


def length_distribution(rows):
    lengths = [sum(len(m.get("content") or "") for m in row["messages"]) for row in rows]
    if not lengths:
        return {"min": 0, "p50": 0, "p90": 0, "max": 0}
    ordered = sorted(lengths)
    return {
        "min": ordered[0],
        "p50": ordered[len(ordered) // 2],
        "p90": ordered[int(len(ordered) * 0.90) - 1],
        "max": ordered[-1],
    }


def generate_dataset():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    entries = []
    agentic_entries = []
    ioc_entries = []
    rejected = []
    ignored_large_or_binary = []
    categories = Counter()
    file_types = Counter()

    for path in sorted(SOURCE_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in VALID_EXTENSIONS:
            continue
        raw_content, rejection = safe_read_text(path)
        if rejection:
            rejected.append(rejection)
            if rejection["reason"] in {"file_too_large", "probably_binary"}:
                ignored_large_or_binary.append(rejection)
            continue

        cleaned = clean_text(raw_content, path.suffix)
        if len(cleaned) < MIN_CHUNK_CHARS:
            rejected.append(reject_record(path, "too_short_after_cleaning", f"{len(cleaned)} chars"))
            continue

        bad_hal = has_bad_hal(cleaned)
        if bad_hal:
            rejected.append(reject_record(path, "invalid_or_nonexistent_hal_api", ", ".join(bad_hal)))
            continue

        kind, category = classify_file(path)
        syntax_meta = syntax_check(path)
        chunks = split_content(cleaned)
        accepted_for_file = 0

        for index, chunk in enumerate(chunks):
            if len(chunk) < MIN_CHUNK_CHARS:
                rejected.append(reject_record(path, "chunk_too_short", f"part {index + 1}"))
                continue
            score = quality_score(chunk, category, kind)
            if score < 15:
                rejected.append(reject_record(path, "low_embedded_value", f"score={score}, part={index + 1}"))
                continue
            variants = ["analyse_code", "debug_code", "explique_code", "améliore_code"]
            if kind in {"TECHNICAL_NOTE", "REGISTER_DATA"}:
                variants = ["convertis_en_notes", "question_reponse", "explique_code"]
            if kind == "IOC_CONFIG":
                variants = ["explique_code", "question_reponse", "analyse_code"]
            variant = variants[index % len(variants)]
            entry = build_entry(path, cleaned, chunk, index, len(chunks), variant, category, kind, syntax_meta)
            entries.append(entry)
            if kind == "IOC_CONFIG":
                ioc_entries.append(entry)
            accepted_for_file += 1

        if accepted_for_file:
            categories[category] += accepted_for_file
            file_types[path.suffix.lower()] += accepted_for_file
            if len(agentic_entries) < 80 and kind in {"SOURCE_CODE", "TECHNICAL_NOTE", "IOC_CONFIG"}:
                agentic_entries.append(build_agentic_example(path, cleaned, category, kind, len(agentic_entries)))

    split_mapping = assign_file_splits(entries)
    for row in agentic_entries:
        row["metadata"]["split"] = split_mapping.get(row["metadata"]["file_hash"], row["metadata"]["split"])

    split_rows = defaultdict(list)
    for entry in entries:
        split_rows[entry["metadata"]["split"]].append(entry)

    write_jsonl(FINAL_FILE, entries)
    write_jsonl(AGENTIC_FILE, agentic_entries)
    write_jsonl(REJECTED_FILE, rejected)
    write_jsonl(TRAIN_FILE, split_rows["train"])
    write_jsonl(VALID_FILE, split_rows["valid"])
    write_jsonl(TEST_FILE, split_rows["test"])
    if ioc_entries:
        write_jsonl(IOC_FILE, ioc_entries)
    elif IOC_FILE.exists():
        IOC_FILE.unlink()

    scores = [row["metadata"]["quality_score"] for row in entries]
    rejection_reasons = Counter(row["reason"] for row in rejected)
    report = {
        "accepted_count": len(entries),
        "rejected_count": len(rejected),
        "splits": {name: len(rows) for name, rows in split_rows.items()},
        "categories": dict(categories),
        "file_types": dict(file_types),
        "average_score": round(statistics.mean(scores), 2) if scores else 0,
        "top_rejection_reasons": rejection_reasons.most_common(10),
        "length_distribution_chars": length_distribution(entries),
        "agentic_examples_generated": len(agentic_entries),
        "ioc_examples_generated": len(ioc_entries),
        "base_model": BASE_MODEL,
        "output_model": OUTPUT_MODEL,
        "ignored_large_or_binary": ignored_large_or_binary,
        "estimated_tokens": sum(row["metadata"].get("estimated_tokens", 0) for row in entries),
        "outputs": {
            "dataset": str(FINAL_FILE),
            "train": str(TRAIN_FILE),
            "valid": str(VALID_FILE),
            "test": str(TEST_FILE),
            "rejected": str(REJECTED_FILE),
            "report": str(REPORT_FILE),
            "agentic": str(AGENTIC_FILE),
            "ioc": str(IOC_FILE) if ioc_entries else None,
        },
    }
    REPORT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main():
    report = generate_dataset()
    print(f"Dataset généré: {report['accepted_count']} entrées")
    print(f"Rejets: {report['rejected_count']}")
    print(f"Train/Valid/Test: {report['splits']}")
    print(f"Rapport: {REPORT_FILE}")


if __name__ == "__main__":
    main()
