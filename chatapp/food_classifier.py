import os
import re
import joblib
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load the Hugging Face FoodNER model
model_name = "carolanderson/roberta-base-food-ner"
tokenizer = AutoTokenizer.from_pretrained(model_name, add_prefix_space=True)
model = AutoModelForTokenClassification.from_pretrained(model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Load our trained classifier
model_path = os.path.join(os.path.dirname(__file__), "classifier", "food_classifier.pkl")
classifier = joblib.load(model_path)

# Blacklist to filter out generic or noisy terms
BLACKLIST = {
    "food", "foods", "dishes", "dish", "flavor", "meal", "meals", "joy", "vegan", "vegetarian",
    "favorite", "delicious", "satisfying", "snack", "something", "stuff", "thing", "yum",
    "top", "my", "your", "absolute", "some", "all", "they", "these"
}

def is_blacklisted(text):
    words = re.sub(r'[^\w\s]', '', text.lower()).split()
    return any(word in BLACKLIST for word in words)

def clean_phrase(phrase: str) -> str:
    
    phrase = phrase.lower().strip()

    # Remove common lead-ins
    phrase = re.sub(r"^(i\s+(absolutely\s+)?love|these\s+are|my\s+top\s+\d+\s+favorite\s+.*?(are|include)?|so\s+delicious\s+and\s+)?", "", phrase)
    
    # Remove common trailing expressions
    phrase = re.sub(r"(they\s+are.*|these\s+are.*|that.*|so\s+delicious.*|enjoy.*|what\s+about\s+you.*|favorites.*|delicious.*)$", "", phrase)

    # Remove connecting words
    phrase = re.sub(r"^\b(and|a|an|my|your|the|some|all|absolutely|favorite|top)\b\s*", "", phrase)
    phrase = re.sub(r"[^\w\s\-]", "", phrase)  # Remove punctuation
    phrase = re.sub(r"\s{2,}", " ", phrase)  # Normalize multiple spaces
    phrase = phrase.strip().title()

    # Extra filter: skip very generic or broken terms
    if len(phrase) < 3 or is_blacklisted(phrase) or phrase.lower() in {"your", "absolute", "top 3", "favorites", "some of"}:
        return ""
    
    return phrase

def extract_food_names(answer: str) -> list:
    """
    Extracts food names from user answers using rule-based methods,
    falling back on Hugging Face FoodNER if needed.
    """
    candidates = []

    # 1. Try extracting from numbered list
    numbered_lines = [re.match(r"^\d+\.\s*(.+)", line.strip()) for line in answer.splitlines()]
    numbered_dishes = [clean_phrase(match.group(1)) for match in numbered_lines if match]
    numbered_dishes = [dish for dish in numbered_dishes if dish]

    if len(numbered_dishes) == 3:
        candidates = numbered_dishes
    else:
        # 2. Try comma or 'and' splitting
        phrase = answer.split("are")[-1] if " are " in answer else answer
        raw_items = re.split(r",\s*|\s+and\s+", phrase)
        seen = set()
        for raw in raw_items:
            dish = clean_phrase(raw)
            if dish and dish not in seen:
                candidates.append(dish)
                seen.add(dish)
            if len(candidates) == 3:
                break

    # 3. Fallback to FoodNER
    if len(candidates) < 3:
        ner_results = ner_pipeline(answer)
        for entity in ner_results:
            phrase = clean_phrase(entity["word"])
            if phrase and phrase not in candidates:
                candidates.append(phrase)
            if len(candidates) == 3:
                break

    return candidates[:3]

def classify_food_items(food_names):
    """
    Classifies list of food names into dietary type using the pre-trained classifier.
    """
    if not food_names:
        return "unknown"
    
    labels = classifier.predict(food_names)

    if "non-vegetarian" in labels:
        return "non-vegetarian"
    elif "vegetarian" in labels:
        return "vegetarian"
    elif "vegan" in labels:
        return "vegan"
    return "unknown"