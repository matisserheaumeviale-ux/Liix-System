import json
import random
from pathlib import Path

random.seed(42)

input_file = Path("output/liix_code_0_2_dataset.jsonl")
train_file = Path("output/liix_code_0_2_train.jsonl")
valid_file = Path("output/liix_code_0_2_valid.jsonl")
test_file = Path("output/liix_code_0_2_test.jsonl")

rows = []

with input_file.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            rows.append(json.loads(line))

random.shuffle(rows)

n = len(rows)
train_end = int(n * 0.85)
valid_end = int(n * 0.95)

splits = {
    train_file: rows[:train_end],
    valid_file: rows[train_end:valid_end],
    test_file: rows[valid_end:],
}

for path, data in splits.items():
    with path.open("w", encoding="utf-8") as f:
        for row in data:
            json.dump(row, f, ensure_ascii=False)
            f.write("\n")

print(f"Total : {n}")
print(f"Train : {len(splits[train_file])}")
print(f"Valid : {len(splits[valid_file])}")
print(f"Test  : {len(splits[test_file])}")
