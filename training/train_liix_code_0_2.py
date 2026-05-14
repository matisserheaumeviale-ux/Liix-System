import inspect
import json
from pathlib import Path

import torch
from datasets import load_dataset
from peft import LoraConfig, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
try:
    from trl import SFTConfig, SFTTrainer
except ImportError:
    from trl import SFTTrainer

    SFTConfig = None


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRAIN_FILE = PROJECT_ROOT / "output" / "train.jsonl"
VALID_FILE = PROJECT_ROOT / "output" / "valid.jsonl"

BASE_MODEL = "models/qwen2.5-coder-7b-instruct"
OUTPUT_MODEL = "liix-code-0.2-alpha"
OUTPUT_DIR = PROJECT_ROOT / "models" / "liix-code-0.2-alpha-adapter"

MAX_SEQ_LENGTH = 2048
SEED = 42

LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
LORA_TARGET_MODULES = [
    "q_proj",
    "k_proj",
    "v_proj",
    "o_proj",
    "gate_proj",
    "up_proj",
    "down_proj",
]


def require_cuda() -> None:
    print(f"torch version: {torch.__version__}")
    print(f"CUDA disponible: {torch.cuda.is_available()}")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA est absent. Ce script QLoRA 4-bit nécessite un GPU NVIDIA CUDA.")

    device_index = torch.cuda.current_device()
    props = torch.cuda.get_device_properties(device_index)
    total_vram_gb = props.total_memory / 1024**3
    print(f"GPU: {props.name}")
    print(f"VRAM totale: {total_vram_gb:.2f} Go")


def require_bitsandbytes() -> None:
    try:
        import bitsandbytes as bnb  # noqa: F401
    except Exception as exc:
        raise RuntimeError(
            "bitsandbytes est absent ou incompatible. Installe une version compatible CUDA/Windows, "
            "puis relance depuis le venv."
        ) from exc


def select_compute_dtype() -> torch.dtype:
    bf16_supported = torch.cuda.is_bf16_supported()
    dtype = torch.bfloat16 if bf16_supported else torch.float16
    print(f"dtype choisi: {dtype}")
    return dtype


def load_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return tokenizer


def format_messages(example, tokenizer):
    messages = example.get("messages") or []
    if tokenizer.chat_template:
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    else:
        parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content") or ""
            if content:
                parts.append(f"<|{role}|>\n{content}")
        text = "\n".join(parts).strip()
        if tokenizer.eos_token:
            text += tokenizer.eos_token
    return {"text": text.strip()}


def load_and_format_dataset(tokenizer):
    if not TRAIN_FILE.exists() or not VALID_FILE.exists():
        raise FileNotFoundError(f"Dataset introuvable: {TRAIN_FILE} / {VALID_FILE}")

    dataset = load_dataset(
        "json",
        data_files={"train": str(TRAIN_FILE), "validation": str(VALID_FILE)},
    )

    dataset = dataset.map(
        lambda example: format_messages(example, tokenizer),
        remove_columns=dataset["train"].column_names,
        desc="Application du chat template",
    )
    dataset = dataset.filter(lambda example: bool(example["text"].strip()), desc="Filtre exemples vides")

    print(f"Nombre exemples train: {len(dataset['train'])}")
    print(f"Nombre exemples valid: {len(dataset['validation'])}")
    print("\n--- Exemple formaté ---")
    print(dataset["train"][0]["text"][:1600])
    print("--- Fin exemple ---\n")
    return dataset


def build_model(compute_dtype: torch.dtype):
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=compute_dtype,
    )

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=quant_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model.config.use_cache = False
    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)
    return model


def build_lora_config() -> LoraConfig:
    return LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=LORA_TARGET_MODULES,
    )


def build_training_args(compute_dtype: torch.dtype):
    kwargs = {
        "output_dir": str(OUTPUT_DIR),
        "num_train_epochs": 2,
        "per_device_train_batch_size": 1,
        "per_device_eval_batch_size": 1,
        "gradient_accumulation_steps": 16,
        "learning_rate": 1e-4,
        "lr_scheduler_type": "cosine",
        "warmup_ratio": 0.03,
        "weight_decay": 0.01,
        "logging_steps": 10,
        "eval_steps": 100,
        "save_steps": 100,
        "save_total_limit": 3,
        "gradient_checkpointing": True,
        "optim": "paged_adamw_8bit",
        "fp16": compute_dtype == torch.float16,
        "bf16": compute_dtype == torch.bfloat16,
        "max_grad_norm": 0.3,
        "report_to": "none",
        "seed": SEED,
    }

    args_cls = SFTConfig if SFTConfig is not None else TrainingArguments
    signature = inspect.signature(args_cls.__init__)
    if "eval_strategy" in signature.parameters:
        kwargs["eval_strategy"] = "steps"
    else:
        kwargs["evaluation_strategy"] = "steps"

    if args_cls is SFTConfig:
        kwargs["dataset_text_field"] = "text"
        kwargs["max_length"] = MAX_SEQ_LENGTH
        kwargs["packing"] = False

    return args_cls(**kwargs)


def build_trainer(model, tokenizer, dataset, lora_config, training_args):
    signature = inspect.signature(SFTTrainer.__init__)
    kwargs = {
        "model": model,
        "args": training_args,
        "train_dataset": dataset["train"],
        "eval_dataset": dataset["validation"],
        "peft_config": lora_config,
    }

    if "processing_class" in signature.parameters:
        kwargs["processing_class"] = tokenizer
    elif "tokenizer" in signature.parameters:
        kwargs["tokenizer"] = tokenizer

    if "dataset_text_field" in signature.parameters:
        kwargs["dataset_text_field"] = "text"
    if "max_seq_length" in signature.parameters:
        kwargs["max_seq_length"] = MAX_SEQ_LENGTH

    return SFTTrainer(**kwargs)


def trainable_parameter_report(model) -> None:
    trainable = 0
    total = 0
    for _, param in model.named_parameters():
        count = param.numel()
        total += count
        if param.requires_grad:
            trainable += count
    pct = 100 * trainable / total if total else 0
    print(f"Paramètres LoRA entraînables: {trainable:,} / {total:,} ({pct:.4f}%)")


def save_training_config(compute_dtype: torch.dtype) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config = {
        "base_model": BASE_MODEL,
        "output_model": OUTPUT_MODEL,
        "output_dir": str(OUTPUT_DIR),
        "train_file": str(TRAIN_FILE),
        "valid_file": str(VALID_FILE),
        "max_seq_length": MAX_SEQ_LENGTH,
        "qlora": {
            "load_in_4bit": True,
            "bnb_4bit_quant_type": "nf4",
            "bnb_4bit_use_double_quant": True,
            "bnb_4bit_compute_dtype": str(compute_dtype),
        },
        "lora": {
            "r": LORA_R,
            "lora_alpha": LORA_ALPHA,
            "lora_dropout": LORA_DROPOUT,
            "bias": "none",
            "task_type": "CAUSAL_LM",
            "target_modules": LORA_TARGET_MODULES,
        },
        "training": {
            "num_train_epochs": 2,
            "per_device_train_batch_size": 1,
            "per_device_eval_batch_size": 1,
            "gradient_accumulation_steps": 16,
            "learning_rate": 1e-4,
            "lr_scheduler_type": "cosine",
            "warmup_ratio": 0.03,
            "weight_decay": 0.01,
            "eval_steps": 100,
            "save_steps": 100,
            "save_total_limit": 3,
            "optim": "paged_adamw_8bit",
            "max_grad_norm": 0.3,
            "seed": SEED,
        },
    }
    (OUTPUT_DIR / "training_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    try:
        require_cuda()
        require_bitsandbytes()
        compute_dtype = select_compute_dtype()

        tokenizer = load_tokenizer()
        dataset = load_and_format_dataset(tokenizer)
        model = build_model(compute_dtype)
        lora_config = build_lora_config()
        training_args = build_training_args(compute_dtype)
        trainer = build_trainer(model, tokenizer, dataset, lora_config, training_args)

        trainable_parameter_report(trainer.model)
        save_training_config(compute_dtype)

        trainer.train()
        eval_metrics = trainer.evaluate()
        print(f"Évaluation valid: {eval_metrics}")

        trainer.save_model(str(OUTPUT_DIR))
        tokenizer.save_pretrained(str(OUTPUT_DIR))
        save_training_config(compute_dtype)
        print(f"Adapter LoRA sauvegardé dans: {OUTPUT_DIR}")

    except torch.cuda.OutOfMemoryError as exc:
        raise RuntimeError(
            "CUDA OOM. Essaie gradient_accumulation_steps=32, MAX_SEQ_LENGTH=1536, "
            "ou LORA_R=8 pour réduire la VRAM."
        ) from exc


if __name__ == "__main__":
    main()
