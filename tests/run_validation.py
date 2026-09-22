import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from risk_engine import calculate_risk

TEST_SET_PATH = Path(__file__).resolve().parent / "test_set.csv"
RESULTS_PATH = Path(__file__).resolve().parent / "validation_results.json"
DELAY_SECONDS = 16


def load_test_set():
    with open(TEST_SET_PATH, newline="") as f:
        return list(csv.DictReader(f))


def run():
    rows = load_test_set()
    results = []
    tp = fp = tn = fn = 0

    for i, row in enumerate(rows, start=1):
        url = row["url"]
        true_label = row["label"]

        outcome = calculate_risk(url)
        predicted_label = "legit" if outcome["verdict"] == "Low Risk - Likely Legitimate" else "scam"
        correct = predicted_label == true_label

        if predicted_label == "scam" and true_label == "scam":
            tp += 1
        elif predicted_label == "scam" and true_label == "legit":
            fp += 1
        elif predicted_label == "legit" and true_label == "legit":
            tn += 1
        else:
            fn += 1

        results.append({
            "url": url,
            "true_label": true_label,
            "category": row["category"],
            "predicted_label": predicted_label,
            "correct": correct,
            "score": outcome["score"],
            "verdict": outcome["verdict"],
            "red_flags": outcome["red_flags"],
            "notes": outcome["notes"],
        })

        status = "OK " if correct else "MISS"
        print(f"[{i}/{len(rows)}] {status} {true_label:6s} -> {predicted_label:6s} ({outcome['score']:3d}) {url}")

        if i < len(rows):
            time.sleep(DELAY_SECONDS)

    total = tp + fp + tn + fn
    accuracy = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0

    summary = {
        "total": total,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "accuracy": round(accuracy, 3),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump({"summary": summary, "results": results}, f, indent=2)

    print("\n--- Summary ---")
    print(json.dumps(summary, indent=2))
    print(f"\nFull results written to {RESULTS_PATH}")


if __name__ == "__main__":
    run()
