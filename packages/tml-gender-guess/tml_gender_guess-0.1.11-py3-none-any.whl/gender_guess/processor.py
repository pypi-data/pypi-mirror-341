from tqdm import tqdm
from .gender_solvers import (
    heuristic_gender,
    classifier_gender,
    gendercomputer_gender,
    fallback_by_token_name,
)


def process_gender_classification(
    data,
    classifier,
    gender_computer,
    female_keywords,
    male_keywords,
    female_names,
    male_names,
    classifier_cache_dict,
    diminutive_map,
    classifier_score_threshold=0.5,
    verbose=False
):
    data["Heuristic"] = ""
    data["DistilbertClassifier"] = ""
    data["DistilbertClassifier_Score"] = 0.0
    data["GenderComputer"] = ""
    data["Combined"] = ""
    data["MethodUsed"] = ""

    accuracies = {
        "Heuristic": 0,
        "DistilbertClassifier": 0,
        "GenderComputer": 0,
        "Combined": 0
    }

    combined_errors = []

    for i in tqdm(range(len(data)), desc="Processing"):
        name = str(data.at[i, "name"])
        #true_gender = str(data.at[i, "gender"]).lower()
        true_gender = str(data.at[i, "gender"]).lower() if "gender" in data.columns else None

        h, name, tokens, female_score, male_score = heuristic_gender(name, female_keywords, male_keywords)
        gc_result = gendercomputer_gender(name, gender_computer)
        classifier_label, classifier_score = classifier_gender(name, classifier, classifier_cache_dict)

        data.at[i, "Heuristic"] = h
        data.at[i, "GenderComputer"] = gc_result
        data.at[i, "DistilbertClassifier"] = classifier_label
        data.at[i, "DistilbertClassifier_Score"] = classifier_score

        if h != "unknown":
            combined = h
            method = "Heuristic"
        elif gc_result != "unknown":
            combined = gc_result
            method = "GenderComputer"
        else:
            fallback, fb_tokens, fb_fem, fb_male = fallback_by_token_name(name, female_names, male_names, diminutive_map)
            if fallback != "unknown":
                combined = fallback
                method = "TokenFallback"
            elif classifier_score >= classifier_score_threshold:
                combined = classifier_label
                method = "DistilbertClassifier"
                fb_tokens, fb_fem, fb_male = [], 0, 0
            else:
                combined = "unknown"
                method = "None"
                fb_tokens, fb_fem, fb_male = [], 0, 0

        data.at[i, "Combined"] = combined
        data.at[i, "MethodUsed"] = method

        for key, prediction in [
            ("Heuristic", h),
            ("GenderComputer", gc_result),
            ("DistilbertClassifier", classifier_label),
            ("Combined", combined)
        ]:
            if prediction == true_gender:
                accuracies[key] += 1

        if combined != true_gender:
            if verbose:
                print(f"[COMBINED ❌] name = {name} | true = {true_gender} | predicted = {combined} | method = {method} | classifier_score = {classifier_score}")
                print(f"tokens = {tokens} | female_score = {female_score} | male_score = {male_score}")
            combined_errors.append({
                "name": name,
                "true_gender": true_gender,
                "predicted_gender": combined,
                "method_used": method,
                "Heuristic": h,
                "GenderComputer": gc_result,
                "DistilbertClassifier": classifier_label,
                "DistilbertClassifier_Score": classifier_score,
                "Heuristic_Tokens": " ".join(tokens),
                "Heuristic_FemaleScore": female_score,
                "Heuristic_MaleScore": male_score,
                "TokenFallback_Tokens": " ".join(fb_tokens) if method == "TokenFallback" else "",
                "TokenFallback_FemaleVotes": fb_fem if method == "TokenFallback" else "",
                "TokenFallback_MaleVotes": fb_male if method == "TokenFallback" else ""
            })


        if verbose and ((i + 1) % 10 == 0 or i == len(data) - 1):
            for key in accuracies:
                acc = accuracies[key] / (i + 1)
                tqdm.write(f"✅ {key} accuracy: {acc:.2%} ({accuracies[key]}/{i + 1})")


    return data, accuracies, combined_errors

