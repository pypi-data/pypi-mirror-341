import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from collections import Counter

def save_combined_errors(errors, path="combined_errors_sorted.csv"):
    df = pd.DataFrame(errors).sort_values(by="DistilbertClassifier_Score")
    df.to_csv(path, index=False)
    print(f"❌ Combined method errors saved to '{path}'")

def save_predictions(data, path="predictions.csv"):
    data.to_csv(path, index=False)
    print(f"✅ Results saved to '{path}'")

def save_classifier_cache(cache_dict, path="distilbert_classifier_cache.csv"):
    df = pd.DataFrame([
        {"name": name, "label": label, "score": score}
        for name, (label, score) in cache_dict.items()
    ])
    df.to_csv(path, index=False)
    print(f"✅ DistilbertClassifier cache saved to '{path}'")

def print_combined_error_stats(errors):
    if not errors:
        print("✅ Combined method had no errors.")
        return
    df_errors = pd.DataFrame(errors)
    method_counts = df_errors["method_used"].value_counts()
    print("\n🔍 Methods used in combined errors:")
    for method, count in method_counts.items():
        print(f"🔸 {method}: {count} errors ({count/len(df_errors):.2%})")


def evaluate_model(data):
    total = len(data)
    predictions = data["Combined"]
    true_labels = data["gender"].str.lower()

    correct = sum(predictions == true_labels)
    accuracy_total = correct / total

    labeled = predictions[predictions != "unknown"]
    true_labeled = true_labels[predictions != "unknown"]
    correct_labeled = sum(labeled == true_labeled)

    accuracy_without_unknown = correct_labeled / len(labeled) if len(labeled) else 0
    unknown_count = (predictions == "unknown").sum()
    unknown_label_distribution = true_labels[predictions == "unknown"].value_counts()

    estimated_accuracy_with_random_unknown = (correct_labeled + 0.5 * unknown_count) / total

    return {
        "total": total,
        "correct": correct,
        "accuracy_total": accuracy_total,
        "labeled": labeled,
        "true_labeled": true_labeled,
        "correct_labeled": correct_labeled,
        "accuracy_without_unknown": accuracy_without_unknown,
        "unknown_count": unknown_count,
        "unknown_label_distribution": unknown_label_distribution,
        "estimated_accuracy_with_random_unknown": estimated_accuracy_with_random_unknown
    }


def print_metrics(metrics):
    total = metrics["total"]
    labeled = metrics["labeled"]
    correct_labeled = metrics["correct_labeled"]
    unknown_count = metrics["unknown_count"]

    if unknown_count > 0:
        print("\n🔍 Gender distribution in 'unknown' cases:")
        for gender, count in metrics["unknown_label_distribution"].items():
            print(f"❓ {gender.capitalize()}: {count} ({count/unknown_count:.2%})")
    else:
        print("✅ No names predicted as 'unknown'.")

    print("\n📌 Classification Report (only classified):")
    print(classification_report(metrics["true_labeled"], metrics["labeled"], digits=4))

    cm = confusion_matrix(metrics["true_labeled"], metrics["labeled"], labels=["male", "female"])
    print("\n📌 Confusion Matrix (rows = true, columns = predicted):")
    print("            Pred. Male | Pred. Female")
    print(f"True Male   {cm[0,0]:>11} | {cm[0,1]:>13}")
    print(f"True Female {cm[1,0]:>11} | {cm[1,1]:>13}")

    pred_counts = Counter(metrics["labeled"])
    print("\n📈 Prediction Distribution (excluding 'unknown'):")
    for gender in ["male", "female"]:
        count = pred_counts.get(gender, 0)
        print(f"🔹 {gender.capitalize()}: {count} ({count/len(labeled):.2%})")
                
    print("\n📊 Combined Method Evaluation:")
    print(f"📈 Classified names:        {len(labeled)/total:.2%} ({len(labeled)}/{total})")
    print(f"🎯 Overall accuracy:        {metrics['accuracy_total']:.2%} ({metrics['correct']}/{total})")
    print(f"🎯 Accuracy (classified):   {metrics['accuracy_without_unknown']:.2%} ({correct_labeled}/{len(labeled)})")
    print(f"🎲 Estimated accuracy (random unknowns): {metrics['estimated_accuracy_with_random_unknown']:.2%}")        

