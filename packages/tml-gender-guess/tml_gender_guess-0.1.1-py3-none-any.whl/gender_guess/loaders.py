import csv
from nltk.corpus import names as nltk_names
import os
import pandas as pd
from transformers import pipeline


def load_distilbert_classifier():
    return pipeline("text-classification", model="padmajabfrl/Gender-Classification")    

def load_names_from_csv(paths):
    names = set()
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            for row in csv.reader(f, delimiter=";"):
                if row and row[0]:
                    names.add(row[0].strip().lower())
    return names    
    
def load_data(path="gender-classifier-DFE-791531.csv"):
    data = pd.read_csv(path, encoding="ISO-8859-1")
    data = data[data["gender"].isin(["male", "female"])]
    data = data[pd.notna(data["name"])].reset_index(drop=True)
    before = len(data)
    data = data.drop_duplicates(subset="name").reset_index(drop=True)
    after = len(data)
    print(f"🔍 Duplicates removed: {before - after} (de {before})")  
    return data           

def load_keywords_and_names():
    # Heuristics by keywords
    female_keywords = [
        "queen", "princess", "girl", "grl", "lady", "diva", "miss", "babe", "cutie", "chick",
        "woman", "doll", "goddess", "angel", "babygirl", "honey", "sweetie", "wifey",
        "barbie", "mommy", "momma", "femme", "ms", "mrs", "beauty", "pretty", "mamacita",
        "missy", "ladybug", "qween", "bae", "cutebae", "gurl", "baddie", "she", "her",
        "fem", "slay", "slayer", "queenie", "shygirl", "hotgirl", "girlie", "vixen", "empress",
        "damsel", "glam", "fairy", "witchy", "pastel", "angelbaby", "catmom", "dogmom", "dancer", "pink"
    ]

    male_keywords = [
        "king", "prince", "guy", "boy", "boi", "man", "bro", "dude", "sir", "mr", "lord", "boss",
        "alpha", "daddy", "hombre", "gentleman", "mister", "he", "him", "uncle", "bruh",
        "boyz", "lad", "manly", "don", "player", "papi", "zaddy", "warrior", "hunter", "beast",
        "champ", "chief", "capo", "og", "soldier", "badboy", "brawler", "stud", "baron",
        "rebel", "macho", "ironman", "batman", "spartan", "theking", "savage",
        
        # common names:
        "brother", "rob", "robby", "mark", "sam", "thom", "ton", "rich", "harvey", "jr", "dj", "dozie"
    ]

    female_name_files = [
        "nameLists/USAFemaleUTF8.csv",
        "nameLists/SpainFemaleUTF8.csv",

    ]

    male_name_files = [
        "nameLists/USAMaleUTF8.csv",
        "nameLists/SpainMaleUTF8.csv",
    ]

    # Load names
    female_names = load_names_from_csv(female_name_files).union({name.lower() for name in nltk_names.words("female.txt")})
    male_names = load_names_from_csv(male_name_files).union({name.lower() for name in nltk_names.words("male.txt")})


    # Removing male-typical conflicts from the female set
    conflict_names = {
        "victor", "alex", "james", "joseph", "daniel", "john", "david", "peter", "michael", "robert",
        "william", "george", "charles", "paul", "mark", "henry", "richard", "kevin", "steven", "brian",
        
        # Very common short names for men
        "ben", "sam", "matt", "nick", "tom", "tony", "tim", "jim", "jake", "max",

        # Ambiguous full names
        "alexander", "andrew", "anthony", "sebastian", "jason", "patrick", "nathan", "gregory", "ian", "jeffrey",
        
        # Potential ambiguous diminutives
        "al", "jo", "ray", "ron", "fred", "frank", "ken", "ed", "leo", "lou",
        
        "calum", "alan", "robin", "criss", "david", "glen", "larry", "collins", "pat",
        "martin", "kenneth", "victor", "kevin", "alex", "joseph", "james", "ty",
        "brother", "rob", "robby", "mark", "sam", "thom", "ton", "rich", "harvey", "jr", "dj"
    }

    female_names -= conflict_names 
    female_names = {name for name in female_names if len(name) >= 2}
    male_names = {name for name in male_names if len(name) >= 2}

    female_names.update(female_keywords)
    male_names.update(male_keywords)

    return female_keywords, male_keywords, female_names, male_names
        

def load_diminutive_map(path="nameLists/diminutives.csv", min_length=5):
    diminutive_map = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            names = [n.strip().lower() for n in line.strip().split(";") if n.strip()]
            if not names:
                continue
            base = names[0]
            if len(base) < min_length:
                continue
            for nickname in names[1:]:
                if len(nickname) >= min_length:
                    diminutive_map[nickname] = base
    return diminutive_map
        
        
def load_classifier_cache(classifier_cache_path="distilbert_classifier_cache.csv"):
    if os.path.exists(classifier_cache_path):
        classifier_cache = pd.read_csv(classifier_cache_path)
        classifier_cache_dict = dict(zip(classifier_cache["name"], zip(classifier_cache["label"], classifier_cache["score"])))
    else:
        classifier_cache = pd.DataFrame(columns=["name", "label", "score"])
        classifier_cache_dict = {}
    return classifier_cache, classifier_cache_dict        
        
