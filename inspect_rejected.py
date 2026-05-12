import json
from collections import Counter, defaultdict
from pathlib import Path

REJECT_FILE = Path("output/rejected.jsonl")

reason_count = Counter()
category_count = Counter()
kind_count = Counter()
examples_by_reason = defaultdict(list)

with REJECT_FILE.open("r", encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)

        meta = row.get("metadata", {})
        reasons = meta.get("reasons", ["unknown_error"])

        category = meta.get("category", "UNKNOWN")
        kind = meta.get("kind", "UNKNOWN")
        file = meta.get("file", row.get("path", "UNKNOWN"))
        score = meta.get("quality_score", "N/A")

        category_count[category] += 1
        kind_count[kind] += 1

        if not reasons:
            reasons = ["low_score_or_short"]

        for reason in reasons:
            reason_count[reason] += 1
            if len(examples_by_reason[reason]) < 5:
                examples_by_reason[reason].append((file, category, kind, score))

print("\n=== Raisons de rejet ===")
for reason, count in reason_count.most_common():
    print(f"{reason:30} {count}")

print("\n=== Rejets par catégorie ===")
for cat, count in category_count.most_common():
    print(f"{cat:20} {count}")

print("\n=== Rejets par type ===")
for kind, count in kind_count.most_common():
    print(f"{kind:20} {count}")

print("\n=== Exemples par raison ===")
for reason, examples in examples_by_reason.items():
    print(f"\n--- {reason} ---")
    for file, category, kind, score in examples:
        print(f"{file} | {category} | {kind} | score={score}")