from tqdm import tqdm
from genderComputer import GenderComputer

from .loaders import (
    load_distilbert_classifier,
    load_data,
    load_keywords_and_names,
    load_diminutive_map,
    load_classifier_cache,
)

from .evaluation import (
    evaluate_model,
    print_metrics,
    save_combined_errors,
    save_predictions,
    save_classifier_cache,
    print_combined_error_stats,
)

from .processor import process_gender_classification

# === Configuration Parameters ===
# Minimum confidence score to accept classifier prediction.
# Lower values (e.g. 0.5) force classification on all cases, higher values only classify when more confident.
CLASSIFIER_SCORE_THRESHOLD = 0.5

VERBOSE = True

# Initialize progress bar
tqdm.pandas()

# Load models and data
classifier = load_distilbert_classifier()
gender_computer = GenderComputer(nameListsPath="nameLists")
data = load_data(path="gender-classifier-DFE-791531.csv")
data = data[["gender", "gender:confidence", "name"]].copy()
female_keywords, male_keywords, female_names, male_names = load_keywords_and_names()
classifier_cache_df, classifier_cache_dict = load_classifier_cache(classifier_cache_path="distilbert_classifier_cache.csv")
diminutive_map = load_diminutive_map()

# Process classification
data, accuracies, combined_errors = process_gender_classification(
    data=data,
    classifier=classifier,
    gender_computer=gender_computer,
    female_keywords=female_keywords,
    male_keywords=male_keywords,
    female_names=female_names,
    male_names=male_names,
    classifier_cache_dict=classifier_cache_dict,
    diminutive_map=diminutive_map,
    classifier_score_threshold=CLASSIFIER_SCORE_THRESHOLD,
    verbose=VERBOSE
)

# Evaluation and output
metrics = evaluate_model(data)
print_combined_error_stats(combined_errors)
print_metrics(metrics)

save_predictions(data)
save_classifier_cache(classifier_cache_dict)
if combined_errors:
    save_combined_errors(combined_errors)

