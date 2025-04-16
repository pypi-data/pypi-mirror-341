import re
import wordninja
from wordsegment import load, segment
load()

def split_name(name):
    return segment(name.lower())

def heuristic_gender(name, female_keywords, male_keywords):
    tokens = wordninja.split(name.lower())

    female_score = sum(1 for word in tokens if word in female_keywords)
    male_score = sum(1 for word in tokens if word in male_keywords)

    if female_score > male_score:
        return "female", name, tokens, female_score, male_score
    elif male_score > female_score:
        return "male", name, tokens, female_score, male_score
    else:    
        return "unknown", name, tokens, female_score, male_score


def classifier_gender(name, classifier, classifier_cache_dict):
    name = name.strip()
    if name in classifier_cache_dict:
        label, score = classifier_cache_dict[name]
    else:
        try:
            result = classifier(name)
            label = result[0]["label"].lower()
            score = result[0]["score"]
            classifier_cache_dict[name] = (label, score)  # Guardar en cache temporal
        except:
            label = "unknown"
            score = 0.0
    return label, score


def gendercomputer_gender(name, gc):
    countries = ["USA", "UK", "Canada", "Australia", "Spain", "Germany", "France", "Italy", "Brazil", "India"]
    try:
        for country in countries:
            result = gc.resolveGender(name, country=country)
            if result and result != "unisex":
                return result
        return "unknown"
    except:
        return "unknown"


# Search for principal name from token or diminutive
def resolve_token(token, female_names, male_names, diminutive_map, use_diminutives=False):
    token = token.lower()
    in_female = token in female_names
    in_male = token in male_names

    if in_female and in_male:
        return "both"
    elif in_female:
        return "female"
    elif in_male:
        return "male"
    
    if use_diminutives and token in diminutive_map:
        base = diminutive_map[token]
        base_in_female = base in female_names
        base_in_male = base in male_names

        if base_in_female and base_in_male:
            return "both"
        elif base_in_female:
            return "female"
        elif base_in_male:
            return "male"
    
    return "unknown"
    
    

# Fallback based on tokens (from longest to shortest)
def fallback_by_token_name(name, female_names, male_names, diminutive_map):
    import re
    #tokens = sorted(wordninja.split(name.lower()), key=len, reverse=True)
    tokens = sorted(wordninja.split(name.lower()))

    results = []
    for token in tokens:
        gender = resolve_token(token, female_names, male_names, diminutive_map, use_diminutives=False)
                
        if gender == "female":
            results.append((token, "female"))
        elif gender == "male":
            results.append((token, "male"))
        elif gender == "both":
            results.append((token, "female"))
            results.append((token, "male"))
                  
    if not results:
        return "unknown", [], 0, 0

    # Counting votes
    female_votes = sum(1 for t, g in results if g == "female")
    male_votes = sum(1 for t, g in results if g == "male")

    if female_votes > male_votes:
        return "female", [t for t, _ in results], female_votes, male_votes
    elif male_votes > female_votes:
        return "male", [t for t, _ in results], female_votes, male_votes
    else:
        first_token = sorted(results, key=lambda x: name.lower().find(x[0]))[0]
        return first_token[1], [t for t, _ in results], female_votes, male_votes
    
