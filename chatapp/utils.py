import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_foods_from_text(text, max_items=3):
    
    foods = []

    numbered_items = re.split(r'\n?\s*\d+[.)]\s*', text)
    numbered_items = [item.strip() for item in numbered_items if item.strip()]

    if len(numbered_items) >= 2:
        for item in numbered_items[:max_items]:
            main_part = re.split(r'\b(with|and|or|,|;)\b', item, maxsplit=1, flags=re.I)[0].strip()

            doc = nlp(main_part)
            candidate_words = []
            for token in doc:
                if token.pos_ in {"NOUN", "ADJ", "PROPN"}:
                    candidate_words.append(token.text)
                elif candidate_words:
                    break  
            if candidate_words:
                food = " ".join(candidate_words)
                food = re.sub(r'^(vegan|vegetarian)\s+', '', food, flags=re.I)  
                foods.append(food.title())

        if foods:
            return foods[:max_items]

    doc = nlp(text)
    seen = set()
    for chunk in doc.noun_chunks:
        candidate = chunk.text.strip()
        if candidate and len(candidate.split()) >= 2 and candidate.lower() not in seen:
            foods.append(candidate.title())
            seen.add(candidate.lower())
        if len(foods) >= max_items:
            break

    return foods[:max_items]
