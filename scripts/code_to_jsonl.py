import hashlib
import json
import re
import shutil
import statistics
from collections import Counter, defaultdict
from pathlib import Path


AUTO_INGEST = True

SOURCE_DIR = Path("sources")
OUTPUT_DIR = Path("output")

FINAL_FILE = OUTPUT_DIR / "dataset_stm32_matisse.jsonl"
DEBUG_FILE = OUTPUT_DIR / "dataset_debug.jsonl"
AGENTIC_FILE = OUTPUT_DIR / "dataset_agentic.jsonl"
CONTINUE_QUALITY_FILE = OUTPUT_DIR / "dataset_continue_quality.jsonl"
AGENTIC_QUALITY_FILE = OUTPUT_DIR / "dataset_agentic_quality.jsonl"
IOC_FILE = OUTPUT_DIR / "dataset_ioc.jsonl"
TRAIN_FILE = OUTPUT_DIR / "train.jsonl"
VALID_FILE = OUTPUT_DIR / "valid.jsonl"
TEST_FILE = OUTPUT_DIR / "test.jsonl"
REJECTED_FILE = OUTPUT_DIR / "rejected.jsonl"
REPORT_FILE = OUTPUT_DIR / "report.json"

SYSTEM_PROMPT = (
    "Tu es Liix-Code-0.2, un assistant spécialisé en STM32, C embarqué, "
    "ARM Cortex-M, HAL/LL, OpenOCD, Makefiles, VSCode, GitHub et architecture AFLC. "
    "Tu dois être précis, ne pas inventer de fonctions HAL, indiquer les hypothèses "
    "de clock/timer, distinguer HAL/LL/registres directs, et expliquer les risques embedded."
)

BASE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
OUTPUT_MODEL = "liix-code-0.2"

MAX_TEXT_FILE_BYTES = 5 * 1024 * 1024
MAX_CHUNK_CHARS = 2400
MIN_CHUNK_CHARS = 80
BIG_SOURCE_MAX_LINES = 1500
BIG_SOURCE_MAX_CHARS = 80_000
MAX_FUNCTION_CHARS = 5000
FREERTOS_TASK_PREFIXES = ("xTask", "vTask", "uxTask", "pcTask", "eTask")

TEXT_EXTENSIONS = {
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".s",
    ".asm",
    ".ld",
    ".mk",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".ioc",
    ".log",
    ".prompt",
    ".pdf",
    ".cfg",
}
SPECIAL_TEXT_NAMES = {"makefile"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg", ".ico", ".tiff"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}
ARCHIVE_EXTENSIONS = {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"}
BINARY_EXTENSIONS = {".o", ".a", ".so", ".dll", ".exe", ".elf", ".bin", ".hex", ".map", ".dylib"}
SKIP_DIRS = {
    "node_modules",
    ".git",
    "build",
    "dist",
    "out",
    "target",
    "debug",
    "release",
    "__pycache__",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    ".idea",
}
USEFUL_VSCODE_FILES = {"settings.json", "tasks.json", "launch.json", "extensions.json", "c_cpp_properties.json"}


def reject_record(path: Path, reason: str, detail: str = "", file_kind: str = "REJECTED_NO_VALUE") -> dict:
    size = None
    try:
        size = path.stat().st_size
    except OSError:
        pass
    return {
        "path": str(path),
        "extension": path.suffix.lower(),
        "file_kind": file_kind,
        "reason": reason,
        "detail": detail,
        "size_bytes": size,
    }


def should_skip_path(path: Path) -> bool:
    parts = [part.lower() for part in path.parts]
    if ".vscode" in parts:
        return path.name not in USEFUL_VSCODE_FILES
    return any(part in SKIP_DIRS for part in parts)


def skip_reason(path: Path) -> str:
    parts = [part.lower() for part in path.parts]
    if ".vscode" in parts and path.name not in USEFUL_VSCODE_FILES:
        return "vscode_non_useful_config"
    for part in parts:
        if part in SKIP_DIRS:
            return f"ignored_directory:{part}"
    return "ignored_path"


def detect_file_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    name = path.name.lower()
    parts = [part.lower() for part in path.parts]
    if name == "makefile" or suffix == ".mk":
        return "MAKEFILE"
    if suffix == ".ld":
        return "LINKER_SCRIPT"
    if suffix == ".ioc":
        return "STM32_IOC"
    if suffix in {".c", ".h", ".cpp", ".hpp", ".s", ".asm"}:
        return "STM32_CODE"
    if suffix == ".log":
        return "GCC_ERROR_LOG"
    if suffix == ".prompt":
        return "CONTINUE_PROMPT"
    if ".vscode" in parts and name in USEFUL_VSCODE_FILES:
        return "VSCode_CONFIG"
    if ".github" in parts or "workflow" in parts or suffix in {".yaml", ".yml"} and "github" in str(path).lower():
        return "GITHUB_WORKFLOW"
    if "openocd" in name or suffix == ".cfg":
        return "OPENOCD"
    if suffix in {".json", ".yaml", ".yml"}:
        return "TECH_NOTE"
    if suffix in {".md", ".txt", ".pdf"}:
        text_name = name.replace("-", " ").replace("_", " ")
        if "security" in text_name or "vulnerability" in text_name:
            return "SECURITY_DOC"
        if "test" in text_name or "unit" in text_name or "quality" in text_name:
            return "TESTING_DOC"
        if "agent" in text_name or "prompt" in text_name or "continue" in text_name:
            return "AGENTIC_DOC"
        return "TECH_NOTE"
    return "REJECTED_NO_VALUE"


def refine_file_kind(path: Path, content: str, initial_kind: str) -> str:
    lowered = content.lower()
    if initial_kind == "GCC_ERROR_LOG" or re.search(r"\b(error:|undefined reference|collect2:|make: \*\*\*)", lowered):
        return "GCC_ERROR_LOG"
    if "openocd" in lowered or "st-link" in lowered or "stlink" in lowered:
        return "OPENOCD" if initial_kind not in {"STM32_CODE", "STM32_IOC"} else initial_kind
    if path.suffix.lower() == ".md":
        head = lowered[:1200]
        frontmatter_agentic = head.startswith("---") and "name:" in head and "description:" in head
        name_agentic = any(token in path.name.lower() for token in ("agent", "prompt", "continue"))
        if name_agentic or "tool_call" in head or "tool_calls" in head or frontmatter_agentic:
            return "AGENTIC_DOC"
        name = path.name.lower()
        if "breaking" in name or "security" in name or "breaking change" in head or "security" in head:
            return "SECURITY_DOC"
        if any(token in name for token in ("test", "unit", "quality", "error-message")) or "unit test" in head or "test quality" in head:
            return "TESTING_DOC"
    return initial_kind


def is_supported_path(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name.lower() in SPECIAL_TEXT_NAMES


def is_probably_binary(path: Path, sample_size: int = 4096) -> bool:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return False
    if suffix in BINARY_EXTENSIONS:
        return True
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


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def clean_cubemx(text: str) -> str:
    text = normalize_newlines(text)
    text = re.sub(r"/\*\s*USER CODE BEGIN [^*]*\*/", "", text)
    text = re.sub(r"/\*\s*USER CODE END [^*]*\*/", "", text)
    text = re.sub(r"/\*={3,}.*?={3,}\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"/\*\*[\s\S]{0,4000}?(?:@file|@brief|Copyright)[\s\S]*?\*/", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*/\* Private (?:includes|typedef|define|macro|variables|function prototypes|user code).*?\*/\s*$", "", text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r"^\s*(?:static\s+)?void\s+\w+\s*\([^;{}]*\);\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_text(text: str, file_kind: str) -> str:
    text = normalize_newlines(text)
    if file_kind == "STM32_CODE":
        text = clean_cubemx(text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def extract_pdf_text(path: Path):
    try:
        from pypdf import PdfReader
    except ImportError:
        return None, reject_record(path, "pdf_extractor_missing", "Install pypdf to extract PDF text")
    try:
        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)
        text = "\n".join(pages)
    except Exception as exc:
        return None, reject_record(path, "pdf_extract_error", str(exc))
    text = drop_large_register_tables(text)
    return text, None


def drop_large_register_tables(text: str) -> str:
    lines = normalize_newlines(text).splitlines()
    kept = []
    for line in lines:
        lower = line.lower()
        registerish = sum(token in lower for token in ("bit_offset", "bit size", "reset value", "byte_offset", "register offset"))
        if registerish >= 2:
            continue
        kept.append(line)
    return "\n".join(kept)


def safe_read_content(path: Path):
    suffix = path.suffix.lower()
    size = path.stat().st_size
    if suffix in IMAGE_EXTENSIONS:
        return None, reject_record(path, "ignored_image")
    if suffix in VIDEO_EXTENSIONS:
        return None, reject_record(path, "ignored_video")
    if suffix in ARCHIVE_EXTENSIONS:
        return None, reject_record(path, "ignored_archive")
    if not is_supported_path(path):
        return None, reject_record(path, "unsupported_extension")
    if suffix != ".pdf" and size > MAX_TEXT_FILE_BYTES:
        return None, reject_record(path, "file_too_large", f">{MAX_TEXT_FILE_BYTES} bytes")
    if is_probably_binary(path):
        return None, reject_record(path, "probably_binary")
    if suffix == ".pdf":
        return extract_pdf_text(path)
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1"), None
        except UnicodeDecodeError as exc:
            return None, reject_record(path, "decode_error", str(exc))
    except Exception as exc:
        return None, reject_record(path, "read_error", str(exc))


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


def source_line_count(content: str) -> int:
    return len(normalize_newlines(content).splitlines())


def is_big_source(content: str) -> bool:
    return source_line_count(content) > BIG_SOURCE_MAX_LINES or len(content) > BIG_SOURCE_MAX_CHARS


def strip_comments_and_macros(content: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
    text = re.sub(r"//.*", "", text)
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append(stripped)
    return "\n".join(lines).strip()


def is_macro_or_comment_only(content: str) -> bool:
    code = strip_comments_and_macros(content)
    if not code:
        return True
    if not any(token in code for token in (";", "{", "}", "=", "return", "while", "for", "if", "switch")):
        return True
    return False


def find_matching_brace(content: str, open_index: int) -> int:
    depth = 0
    index = open_index
    in_line_comment = False
    in_block_comment = False
    in_string = False
    in_char = False
    escaped = False
    while index < len(content):
        ch = content[index]
        nxt = content[index + 1] if index + 1 < len(content) else ""
        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
        elif in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                index += 1
        elif in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        elif in_char:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == "'":
                in_char = False
        else:
            if ch == "/" and nxt == "/":
                in_line_comment = True
                index += 1
            elif ch == "/" and nxt == "*":
                in_block_comment = True
                index += 1
            elif ch == '"':
                in_string = True
            elif ch == "'":
                in_char = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return index + 1
        index += 1
    return -1


def extract_c_functions(content: str) -> list:
    pattern = re.compile(
        r"(?m)^[ \t]*(?:[A-Za-z_][\w\s\*\(\)]*\s+)+(?P<name>[A-Za-z_]\w*)\s*\([^;{}]*\)\s*(?:/\*.*?\*/\s*)?\{",
        re.DOTALL,
    )
    functions = []
    seen_ranges = set()
    for match in pattern.finditer(content):
        name = match.group("name")
        if name in {"if", "for", "while", "switch", "return", "sizeof"}:
            continue
        open_index = content.find("{", match.start(), match.end())
        end = find_matching_brace(content, open_index)
        if end == -1:
            continue
        start = match.start()
        comment_start = content.rfind("\n/*", 0, start)
        if comment_start != -1 and start - comment_start < 1200:
            start = comment_start + 1
        span = (start, end)
        if span in seen_ranges:
            continue
        seen_ranges.add(span)
        functions.append({"name": name, "content": content[start:end].strip(), "start": start, "end": end})
    return functions


def split_large_function(function_text: str) -> list:
    if len(function_text) <= MAX_FUNCTION_CHARS:
        return [function_text]
    pieces = re.split(r"(?=\n\s*(?:/\*+|//|if\s*\(|for\s*\(|while\s*\(|switch\s*\(|taskENTER_CRITICAL|taskEXIT_CRITICAL))", function_text)
    chunks = []
    current = ""
    for piece in pieces:
        if not piece.strip():
            continue
        if len(current) + len(piece) <= MAX_FUNCTION_CHARS:
            current += piece
        else:
            if current.strip():
                chunks.extend(split_content(current.strip(), max_chars=MAX_FUNCTION_CHARS))
            current = piece
    if current.strip():
        chunks.extend(split_content(current.strip(), max_chars=MAX_FUNCTION_CHARS))
    return [chunk for chunk in chunks if chunk.strip()]


def freertos_priority(function_name: str, function_text: str) -> tuple:
    public = function_name.startswith(FREERTOS_TASK_PREFIXES)
    scheduler_terms = ("scheduler", "tick", "priority", "stack", "critical", "isr", "task", "queue")
    signal = sum(1 for term in scheduler_terms if term.lower() in function_text.lower())
    return (0 if public else 1, -signal, function_name.lower())


def build_code_chunks(content: str) -> list:
    functions = extract_c_functions(content)
    chunks = []
    for function in sorted(functions, key=lambda item: freertos_priority(item["name"], item["content"])):
        if is_macro_or_comment_only(function["content"]):
            continue
        parts = split_large_function(function["content"])
        for part_index, part in enumerate(parts):
            if is_macro_or_comment_only(part):
                continue
            chunks.append(
                {
                    "text": part,
                    "extraction_method": "split_function" if len(parts) > 1 else "function",
                    "function_name": function["name"],
                    "function_part": part_index + 1 if len(parts) > 1 else None,
                    "function_parts": len(parts) if len(parts) > 1 else None,
                }
            )
    if chunks:
        return chunks
    return [
        {"text": chunk, "extraction_method": "file_part", "function_name": None, "function_part": None, "function_parts": None}
        for chunk in split_content(content)
        if not is_macro_or_comment_only(chunk)
    ]


def build_chunks_for_file(content: str, file_kind: str) -> list:
    if file_kind == "STM32_CODE":
        return build_code_chunks(content)
    return [
        {"text": chunk, "extraction_method": "file_part", "function_name": None, "function_part": None, "function_parts": None}
        for chunk in split_content(content)
    ]


def extract_c_symbols(content: str) -> dict:
    functions = sorted(set(re.findall(r"^\s*(?:static\s+)?(?:inline\s+)?[A-Za-z_][\w\s\*]*\s+([A-Za-z_]\w*)\s*\([^;]*\)\s*\{", content, re.MULTILINE)))
    hal = sorted(set(re.findall(r"\bHAL_[A-Za-z0-9_]+\b", content)))
    ll = sorted(set(re.findall(r"\bLL_[A-Za-z0-9_]+\b", content)))
    registers = sorted(set(re.findall(r"\b(?:RCC|GPIO[A-K]|TIM\d+|USART\d+|UART\d+|ADC\d+|DMA\d+|NVIC|SCB|SysTick)->[A-Za-z0-9_]+\b", content)))
    timers = sorted(set(re.findall(r"\bTIM\d+\b|\bhtim\d+\b", content, flags=re.IGNORECASE)))
    pins = sorted(set(re.findall(r"\bGPIO_PIN_(?:\d+|All)\b|\bP[A-K]\d{1,2}\b", content)))
    psc = sorted(set(re.findall(r"\b(?:PSC|Prescaler|\.Prescaler)\s*[=:]\s*([A-Za-z0-9_+\-*/()]+)", content)))
    arr = sorted(set(re.findall(r"\b(?:ARR|Period|\.Period)\s*[=:]\s*([A-Za-z0-9_+\-*/()]+)", content)))
    ccr = sorted(set(re.findall(r"\b(?:CCR[1-4]?|Pulse|\.Pulse)\s*[=:]\s*([A-Za-z0-9_+\-*/()]+)", content)))
    return {"functions": functions, "hal": hal, "ll": ll, "registers": registers, "timers": timers, "pins": pins, "psc": psc, "arr": arr, "ccr": ccr}


def parse_ioc(content: str) -> dict:
    data = {}
    for line in normalize_newlines(content).splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    joined = "\n".join(f"{k}={v}" for k, v in data.items())
    keys = list(data.keys())
    return {
        "mcu": data.get("Mcu.Name") or data.get("Mcu.Family") or data.get("ProjectManager.DeviceId"),
        "pins": sorted(set(re.findall(r"\bP[A-K]\d{1,2}\b", joined)))[:40],
        "timers": sorted(set(re.findall(r"\bTIM\d+\b", joined)))[:30],
        "uart": sorted(set(re.findall(r"\b(?:USART|UART)\d+\b", joined)))[:20],
        "adc": sorted(set(re.findall(r"\bADC\d*\b", joined)))[:20],
        "dma": sorted(set(k for k in keys if "DMA" in k))[:30],
        "nvic": sorted(set(k for k in keys if "NVIC" in k))[:30],
        "clocks": sorted(set(k for k in keys if "Clock" in k or "RCC" in k))[:30],
    }


def detect_log_errors(content: str) -> dict:
    patterns = {
        "gcc_error": r"\berror: .+",
        "gcc_warning": r"\bwarning: .+",
        "make_error": r"make(?:\[\d+\])?: \*\*\* .+",
        "linker_error": r"undefined reference|ld(?:\.exe)?:|collect2:",
        "openocd_error": r"OpenOCD|Error:|Warn :|ST-LINK|stlink|target halted|failed",
    }
    found = {}
    for name, pattern in patterns.items():
        matches = re.findall(pattern, content, flags=re.IGNORECASE)
        if matches:
            found[name] = matches[:12]
    return found


def short(values, limit=8) -> str:
    if not values:
        return "aucun élément explicite"
    shown = list(values)[:limit]
    suffix = "" if len(values) <= limit else f", +{len(values) - limit}"
    return ", ".join(str(v) for v in shown) + suffix


def build_answer(content: str, file_kind: str) -> str:
    if file_kind == "STM32_CODE":
        c = extract_c_symbols(content)
        rtos_terms = sorted(set(re.findall(r"\b(?:xTask\w+|vTask\w+|uxTask\w+|pcTask\w+|eTask\w+|taskENTER_CRITICAL|taskEXIT_CRITICAL|portYIELD_FROM_ISR|pdMS_TO_TICKS)\b", content)))
        rtos_note = ""
        if rtos_terms or re.search(r"\b(?:scheduler|tick|priority|stack|ISR|FreeRTOS)\b", content, re.IGNORECASE):
            rtos_note = (
                f" RTOS: symboles={short(rtos_terms)}; vérifier scheduler, tick, priorité, pile, sections critiques et ISR safety."
            )
        return (
            "Analyse STM32/C: "
            f"fonctions={short(c['functions'])}; HAL={short(c['hal'])}; LL={short(c['ll'])}; "
            f"registres directs={short(c['registers'])}; timers={short(c['timers'])}; pins={short(c['pins'])}. "
            f"Paramètres timer: PSC={short(c['psc'], 4)}, ARR={short(c['arr'], 4)}, CCR/Pulse={short(c['ccr'], 4)}. "
            f"{rtos_note}"
            "Risques: vérifier clock réelle, timeouts bloquants, contexte interruption, overflow de compteurs et cohérence HAL/LL/registres. "
            "Correction conservatrice: ne changer que ce qui est confirmé par le schéma, CubeMX ou la sortie de build."
        )
    if file_kind == "STM32_IOC":
        ioc = parse_ioc(content)
        return (
            "Configuration CubeMX détectée: "
            f"MCU={ioc['mcu'] or 'non indiqué'}, pins={short(ioc['pins'])}, timers={short(ioc['timers'])}, "
            f"UART={short(ioc['uart'])}, ADC={short(ioc['adc'])}, DMA={short(ioc['dma'])}, NVIC={short(ioc['nvic'])}, clocks={short(ioc['clocks'])}. "
            "À vérifier: source d'horloge, prescalers, conflits de pins, activation NVIC/DMA et génération HAL/LL attendue."
        )
    if file_kind in {"GCC_ERROR_LOG", "OPENOCD"}:
        errors = detect_log_errors(content)
        parts = [f"{name}={short(matches, 3)}" for name, matches in errors.items()]
        return (
            "Diagnostic debug: " + ("; ".join(parts) if parts else "aucune erreur structurée détectée") + ". "
            "Méthode: isoler la première erreur racine, distinguer compilation/link/OpenOCD/ST-Link, corriger minimalement, relancer make puis tester sur cible."
        )
    if file_kind in {"CONTINUE_PROMPT", "AGENTIC_DOC"}:
        return (
            "Analyse prompt/agentic: identifier l'objectif, les outils attendus, les contraintes de sécurité, les critères de succès et les cas d'échec. "
            "Transformer en exemple tool-use clair: lecture, recherche, action, observation, synthèse finale et patch minimal si nécessaire."
        )
    if file_kind == "MAKEFILE":
        return "Analyse Makefile: identifier toolchain, flags, targets, objets, script linker et commandes flash/debug. Vérifier chemins Windows/Linux, dépendances et sorties GCC."
    if file_kind == "LINKER_SCRIPT":
        return "Analyse linker script: vérifier MEMORY, sections, stack/heap, vecteurs, placement FLASH/RAM et symboles utilisés par startup."
    return "Analyse technique: extraire les faits utiles, signaler les hypothèses manquantes, éviter les inventions et convertir le contenu en connaissances actionnables."


def instruction_for_kind(file_kind: str) -> str:
    mapping = {
        "STM32_CODE": (
            "Analyse ce code STM32/C embarqué. Extrais fonctions, HAL/LL, registres, timers, GPIO, risques et corrections conservatrices. "
            "Si le fragment touche un RTOS, analyse tâche, scheduler, tick, priorité, pile, section critique et ISR safety."
        ),
        "STM32_IOC": "Explique cette configuration STM32CubeMX .ioc et les points à vérifier avant génération de code.",
        "MAKEFILE": "Analyse ce Makefile pour un projet STM32 et repère les risques de build.",
        "LINKER_SCRIPT": "Analyse ce script linker ARM Cortex-M.",
        "OPENOCD": "Analyse cette sortie/config OpenOCD ou ST-Link et propose un diagnostic.",
        "GCC_ERROR_LOG": "Débogue ce log GCC/make/linker/OpenOCD et propose une marche à suivre.",
        "CONTINUE_PROMPT": "Convertis ce prompt Continue en exemple d'entraînement agentic de qualité.",
        "AGENTIC_DOC": "Analyse cette documentation agentic et transforme-la en exemple tool-use utile.",
        "SECURITY_DOC": "Résume ce document sécurité en règles de codage et revue utiles.",
        "TESTING_DOC": "Transforme ce document de test/qualité en checklist technique.",
        "VSCode_CONFIG": "Analyse cette configuration VSCode pour un projet embedded.",
        "GITHUB_WORKFLOW": "Analyse ce workflow GitHub dans un contexte firmware/CI.",
        "TECH_NOTE": "Transforme cette note technique en connaissances utiles pour Liix-Code-0.2.",
    }
    return mapping.get(file_kind, "Analyse ce contenu et garde seulement la valeur technique utile.")


def make_messages(content: str, file_kind: str):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"{instruction_for_kind(file_kind)}\n\nType: {file_kind}\n\n{content}"},
        {"role": "assistant", "content": build_answer(content, file_kind)},
    ]


def make_agentic_messages(path: Path, content: str, file_kind: str):
    query = "HAL_" if "HAL_" in content else ("error:" if "error:" in content.lower() else path.stem)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Utilise des outils pour inspecter {path.name}, chercher le signal utile, lancer la validation et proposer une correction."},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {"id": "read_1", "type": "function", "function": {"name": "read_file", "arguments": json.dumps({"path": str(path)})}},
                {"id": "search_1", "type": "function", "function": {"name": "search_text", "arguments": json.dumps({"query": query, "path": str(path.parent)})}},
            ],
        },
        {"role": "tool", "tool_call_id": "read_1", "name": "read_file", "content": content[:900]},
        {"role": "tool", "tool_call_id": "search_1", "name": "search_text", "content": f"Occurrences à inspecter pour {query}."},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {"id": "make_1", "type": "function", "function": {"name": "run_make", "arguments": json.dumps({"target": "all"})}},
                {"id": "test_1", "type": "function", "function": {"name": "run_test", "arguments": json.dumps({"kind": "build_or_static_check"})}},
            ],
        },
        {"role": "tool", "tool_call_id": "make_1", "name": "run_make", "content": "Sortie à analyser: première erreur GCC/linker/OpenOCD avant les symptômes secondaires."},
        {"role": "tool", "tool_call_id": "test_1", "name": "run_test", "content": "Validation: build propre ou test matériel ciblé."},
        {"role": "assistant", "content": build_answer(content[:1200], file_kind) + "\nAction finale: proposer un patch minimal, puis ouvrir une issue GitHub si le problème dépasse le correctif local."},
    ]


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def file_hash(path: Path, content: str) -> str:
    h = hashlib.sha256()
    h.update(str(path).replace("\\", "/").lower().encode("utf-8"))
    h.update(b"\0")
    h.update(content[:8192].encode("utf-8", errors="ignore"))
    return h.hexdigest()


def quality_score(content: str, file_kind: str) -> int:
    score = 5
    if len(content) >= MIN_CHUNK_CHARS:
        score += 10
    if file_kind in {"STM32_CODE", "STM32_IOC", "GCC_ERROR_LOG", "MAKEFILE", "LINKER_SCRIPT"}:
        score += 20
    if file_kind in {"CONTINUE_PROMPT", "AGENTIC_DOC", "TESTING_DOC", "SECURITY_DOC"}:
        score += 16
    if re.search(r"\bHAL_[A-Za-z0-9_]+\b|\bLL_[A-Za-z0-9_]+\b|\bTIM\d+\b|\bGPIO_PIN_\d+\b", content):
        score += 16
    if re.search(r"\b(?:block/|fieldset/|bit_offset|byte_offset|register|peripheral)\b", content, re.IGNORECASE):
        score += 14
    if re.search(r"\b(error:|undefined reference|OpenOCD|ST-LINK|make: \*\*\*)", content, re.IGNORECASE):
        score += 18
    if re.search(r"\b(?:PSC|ARR|CCR|Prescaler|Period|Pulse)\b", content):
        score += 12
    if content.count("USER CODE") > 6:
        score -= 10
    if len(re.findall(r"[A-Za-z_][A-Za-z0-9_]+", content)) < 15:
        score -= 15
    return max(0, min(100, score))


def make_entry(
    path: Path,
    content: str,
    chunk: str,
    file_kind: str,
    index: int,
    total: int,
    variant: str = "standard",
    extraction_method: str = "file_part",
    function_name: str = None,
    function_part: int = None,
    function_parts: int = None,
) -> dict:
    score = quality_score(chunk, file_kind)
    h = file_hash(path, content)
    lines = source_line_count(content)
    big_file = is_big_source(content)
    metadata = {
        "source_path": str(path),
        "file_name": path.name,
        "file_hash": h,
        "file_kind": file_kind,
        "source_file_lines": lines,
        "big_file": big_file,
        "extraction_method": extraction_method,
        "part": index + 1,
        "parts": total,
        "quality_score": score,
        "estimated_tokens": estimate_tokens(chunk),
        "variant": variant,
    }
    if function_name:
        metadata["function_name"] = function_name
    if function_part is not None:
        metadata["function_part"] = function_part
    if function_parts is not None:
        metadata["function_parts"] = function_parts
    return {
        "messages": make_messages(chunk, file_kind),
        "metadata": metadata,
    }


def make_agentic_entry(path: Path, content: str, file_kind: str, variant: str) -> dict:
    h = file_hash(path, content)
    return {
        "messages": make_agentic_messages(path, content, file_kind),
        "tools": [
            {"type": "function", "function": {"name": "read_file", "parameters": {"type": "object"}}},
            {"type": "function", "function": {"name": "search_text", "parameters": {"type": "object"}}},
            {"type": "function", "function": {"name": "run_make", "parameters": {"type": "object"}}},
            {"type": "function", "function": {"name": "run_test", "parameters": {"type": "object"}}},
            {"type": "function", "function": {"name": "create_github_issue", "parameters": {"type": "object"}}},
        ],
        "metadata": {
            "source_path": str(path),
            "file_name": path.name,
            "file_hash": h,
            "file_kind": file_kind,
            "source_file_lines": source_line_count(content),
            "big_file": is_big_source(content),
            "extraction_method": "agentic_tool_use",
            "quality_score": quality_score(content[:1200], file_kind),
            "estimated_tokens": estimate_tokens(content[:1200]),
            "variant": variant,
        },
    }


def assign_splits(rows) -> dict:
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
        row["metadata"]["split"] = mapping.get(row["metadata"]["file_hash"], "train")
    return mapping


def write_jsonl(path: Path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            json.dump(row, handle, ensure_ascii=False)
            handle.write("\n")


def dataset_bucket(file_kind: str) -> str:
    if file_kind in {"GCC_ERROR_LOG", "OPENOCD"}:
        return "debug"
    if file_kind in {"CONTINUE_PROMPT", "AGENTIC_DOC"}:
        return "continue_quality"
    if file_kind == "STM32_IOC":
        return "ioc"
    return "main"


def scan_files():
    return sorted(path for path in SOURCE_DIR.rglob("*") if path.is_file())


def generate_dataset():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_entries = []
    main_entries = []
    debug_entries = []
    agentic_entries = []
    continue_entries = []
    ioc_entries = []
    rejected = []
    ignored = []
    file_scores = defaultdict(list)
    noisy_scores = defaultdict(int)
    categories = Counter()
    scanned_count = 0

    for path in scan_files():
        scanned_count += 1
        try:
            if AUTO_INGEST and should_skip_path(path):
                item = reject_record(path, skip_reason(path))
                ignored.append(item)
                rejected.append(item)
                continue

            raw, rejection = safe_read_content(path)
            initial_kind = detect_file_kind(path)
            if rejection:
                rejection["file_kind"] = initial_kind
                if rejection["reason"].startswith("ignored_") or rejection["reason"] in {"unsupported_extension", "probably_binary", "file_too_large"}:
                    ignored.append(rejection)
                rejected.append(rejection)
                noisy_scores[str(path)] += 1
                continue

            file_kind = refine_file_kind(path, raw or "", initial_kind)
            if file_kind == "REJECTED_NO_VALUE":
                rejected.append(reject_record(path, "rejected_no_value", file_kind=file_kind))
                noisy_scores[str(path)] += 1
                continue

            content = clean_text(raw or "", file_kind)
            if len(content) < MIN_CHUNK_CHARS:
                rejected.append(reject_record(path, "too_short_after_cleaning", f"{len(content)} chars", file_kind))
                noisy_scores[str(path)] += 1
                continue

            chunks = build_chunks_for_file(content, file_kind)
            accepted_for_file = 0
            for index, chunk_info in enumerate(chunks):
                chunk = chunk_info["text"]
                if len(chunk) < MIN_CHUNK_CHARS:
                    rejected.append(reject_record(path, "chunk_too_short", f"part {index + 1}", file_kind))
                    noisy_scores[str(path)] += 1
                    continue
                if file_kind == "STM32_CODE" and is_macro_or_comment_only(chunk):
                    rejected.append(reject_record(path, "macro_or_comment_only", f"part {index + 1}", file_kind))
                    noisy_scores[str(path)] += 1
                    continue
                score = quality_score(chunk, file_kind)
                if score < 18:
                    rejected.append(reject_record(path, "low_value_chunk", f"score={score}, part={index + 1}", file_kind))
                    noisy_scores[str(path)] += 1
                    continue
                entry = make_entry(
                    path,
                    content,
                    chunk,
                    file_kind,
                    index,
                    len(chunks),
                    extraction_method=chunk_info["extraction_method"],
                    function_name=chunk_info["function_name"],
                    function_part=chunk_info["function_part"],
                    function_parts=chunk_info["function_parts"],
                )
                bucket = dataset_bucket(file_kind)
                all_entries.append(entry)
                if bucket == "debug":
                    debug_entries.append(entry)
                elif bucket == "continue_quality":
                    continue_entries.append(entry)
                elif bucket == "ioc":
                    ioc_entries.append(entry)
                else:
                    main_entries.append(entry)
                file_scores[str(path)].append(score)
                categories[file_kind] += 1
                accepted_for_file += 1

            if accepted_for_file and file_kind in {"STM32_CODE", "GCC_ERROR_LOG", "OPENOCD", "CONTINUE_PROMPT", "AGENTIC_DOC", "MAKEFILE"}:
                agentic = make_agentic_entry(path, content, file_kind, "agentic_tool_use")
                all_entries.append(agentic)
                agentic_entries.append(agentic)
                if file_kind in {"CONTINUE_PROMPT", "AGENTIC_DOC"}:
                    continue_entries.append(agentic)
                categories["AGENTIC_TOOL_USE"] += 1
                file_scores[str(path)].append(agentic["metadata"]["quality_score"])

        except Exception as exc:
            rejected.append(reject_record(path, "unexpected_error", str(exc), detect_file_kind(path)))
            noisy_scores[str(path)] += 1

    assign_splits(all_entries)
    for collection in (main_entries, debug_entries, agentic_entries, continue_entries, ioc_entries):
        for row in collection:
            row["metadata"]["split"] = next((e["metadata"]["split"] for e in all_entries if e["metadata"]["file_hash"] == row["metadata"]["file_hash"]), "train")

    split_rows = defaultdict(list)
    for row in all_entries:
        split_rows[row["metadata"]["split"]].append(row)

    write_jsonl(FINAL_FILE, main_entries)
    write_jsonl(DEBUG_FILE, debug_entries)
    write_jsonl(AGENTIC_FILE, agentic_entries)
    write_jsonl(CONTINUE_QUALITY_FILE, continue_entries)
    write_jsonl(AGENTIC_QUALITY_FILE, continue_entries)
    write_jsonl(IOC_FILE, ioc_entries)
    write_jsonl(TRAIN_FILE, split_rows["train"])
    write_jsonl(VALID_FILE, split_rows["valid"])
    write_jsonl(TEST_FILE, split_rows["test"])
    write_jsonl(REJECTED_FILE, rejected)

    split_leaks = count_split_leaks(split_rows)
    ignored_files = {item["path"] for item in ignored}
    rejected_files = {item["path"] for item in rejected}
    scores = [score for values in file_scores.values() for score in values]
    extraction_methods = Counter(row["metadata"].get("extraction_method", "unknown") for row in all_entries)
    big_file_entries = sum(1 for row in all_entries if row["metadata"].get("big_file"))
    report = {
        "auto_ingest": AUTO_INGEST,
        "base_model": BASE_MODEL,
        "output_model": OUTPUT_MODEL,
        "files_scanned": scanned_count,
        "files_ignored": len(ignored_files),
        "files_rejected": len(rejected_files),
        "rejected_rows": len(rejected),
        "rejection_reasons": Counter(item["reason"] for item in rejected).most_common(20),
        "categories": dict(categories),
        "extraction_methods": dict(extraction_methods),
        "big_file_entries": big_file_entries,
        "estimated_tokens": sum(row["metadata"].get("estimated_tokens", 0) for row in all_entries),
        "average_quality_score": round(statistics.mean(scores), 2) if scores else 0,
        "top_most_useful_files": top_files(file_scores, reverse=True),
        "top_noisiest_files": top_noisy_files(file_scores, noisy_scores),
        "split_leaks": split_leaks,
        "datasets": {
            "dataset_stm32_matisse": len(main_entries),
            "dataset_debug": len(debug_entries),
            "dataset_agentic": len(agentic_entries),
            "dataset_continue_quality": len(continue_entries),
            "dataset_agentic_quality": len(continue_entries),
            "dataset_ioc": len(ioc_entries),
            "train": len(split_rows["train"]),
            "valid": len(split_rows["valid"]),
            "test": len(split_rows["test"]),
            "rejected": len(rejected),
        },
        "outputs": {
            "dataset_stm32_matisse": str(FINAL_FILE),
            "dataset_debug": str(DEBUG_FILE),
            "dataset_agentic": str(AGENTIC_FILE),
            "dataset_continue_quality": str(CONTINUE_QUALITY_FILE),
            "dataset_agentic_quality": str(AGENTIC_QUALITY_FILE),
            "dataset_ioc": str(IOC_FILE),
            "train": str(TRAIN_FILE),
            "valid": str(VALID_FILE),
            "test": str(TEST_FILE),
            "rejected": str(REJECTED_FILE),
            "report": str(REPORT_FILE),
        },
    }
    REPORT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def count_split_leaks(split_rows) -> int:
    locations = defaultdict(set)
    for split, rows in split_rows.items():
        for row in rows:
            locations[row["metadata"]["file_hash"]].add(split)
    return sum(1 for splits in locations.values() if len(splits) > 1)


def top_files(file_scores, reverse=True, limit=10):
    rows = []
    for path, scores in file_scores.items():
        if scores:
            rows.append({"path": path, "score": round(statistics.mean(scores), 2), "entries": len(scores)})
    rows.sort(key=lambda row: row["score"], reverse=reverse)
    return rows[:limit]


def top_noisy_files(file_scores, noisy_scores, limit=10):
    paths = set(file_scores) | set(noisy_scores)
    rows = []
    for path in paths:
        accepted = len(file_scores.get(path, []))
        rejected = noisy_scores.get(path, 0)
        total = accepted + rejected
        if total:
            rows.append({"path": path, "rejected_chunks": rejected, "accepted_chunks": accepted, "noise_ratio": round(rejected / total, 3)})
    rows.sort(key=lambda row: (row["noise_ratio"], row["rejected_chunks"]), reverse=True)
    return rows[:limit]


def main():
    report = generate_dataset()
    print(f"Fichiers scannés: {report['files_scanned']}")
    print(f"Entrées train/valid/test: {report['datasets']['train']}/{report['datasets']['valid']}/{report['datasets']['test']}")
    print(f"Rejets: {report['files_rejected']}")
    print(f"Rapport: {REPORT_FILE}")


if __name__ == "__main__":
    main()
