from .loaders import (
    load_distilbert_classifier,
    load_keywords_and_names,
    load_diminutive_map,
    load_classifier_cache,
)
from .genderComputer import GenderComputer
from .processor import process_gender_classification
import pandas as pd
from tqdm import tqdm

DEFAULT_CLASSIFIER_SCORE_THRESHOLD = 0.5

# Load models once
tqdm.pandas()
classifier = load_distilbert_classifier()
gender_computer = GenderComputer(nameListsPath="nameLists")
female_keywords, male_keywords, female_names, male_names = load_keywords_and_names()
_, classifier_cache_dict = load_classifier_cache("distilbert_classifier_cache.csv")
diminutive_map = load_diminutive_map()


def predict_gender_batch(names: list[str], threshold: float = DEFAULT_CLASSIFIER_SCORE_THRESHOLD):
    df = pd.DataFrame({"name": names})
    result_df, _, _ = process_gender_classification(
        data=df,
        classifier=classifier,
        gender_computer=gender_computer,
        female_keywords=female_keywords,
        male_keywords=male_keywords,
        female_names=female_names,
        male_names=male_names,
        classifier_cache_dict=classifier_cache_dict,
        diminutive_map=diminutive_map,
        classifier_score_threshold=threshold,
        verbose=False
    )

    return result_df

