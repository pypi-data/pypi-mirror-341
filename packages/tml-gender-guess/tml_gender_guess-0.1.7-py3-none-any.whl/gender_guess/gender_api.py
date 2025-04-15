from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
from tqdm import tqdm

from .genderComputer.genderComputer import GenderComputer
from .loaders import (
    load_distilbert_classifier,
    load_keywords_and_names,
    load_diminutive_map,
    load_classifier_cache,
)

from .processor import process_gender_classification

# Default config
DEFAULT_CLASSIFIER_SCORE_THRESHOLD = 0.5

# Init FastAPI
app = FastAPI()

# Load all once
tqdm.pandas()
classifier = load_distilbert_classifier()
gender_computer = GenderComputer(nameListsPath="nameLists")
female_keywords, male_keywords, female_names, male_names = load_keywords_and_names()
_, classifier_cache_dict = load_classifier_cache("distilbert_classifier_cache.csv")
diminutive_map = load_diminutive_map()


# Input models
class GenderBatchRequest(BaseModel):
    data: List[str]
    classifier_score_threshold: Optional[float] = Field(default=DEFAULT_CLASSIFIER_SCORE_THRESHOLD)


# Output helper
def format_response(row):
    return {
        "name": row["name"],
        "predicted_gender": row["Combined"],
        "method_used": row["MethodUsed"],
        "heuristic": row["Heuristic"],
        "gender_computer": row["GenderComputer"],
        "distilbert": row["DistilbertClassifier"],
        "distilbert_score": row["DistilbertClassifier_Score"],
    }


# API endpoint with full pipeline
@app.post("/predict-gender-batch")
async def predict_gender_batch(request: GenderBatchRequest):
    # Build temporary dataframe
    df = pd.DataFrame({"name": request.data})

    # Process using full pipeline
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
        classifier_score_threshold=request.classifier_score_threshold,
        verbose=False,
    )

    return [format_response(row) for _, row in result_df.iterrows()]

