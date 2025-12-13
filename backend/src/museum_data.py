import pandas as pd
import re

def load_museum_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["state"] = df["address"].str.extract(r",\s*([A-Z]{2})\s*\d{5}")
    return df

def get_tag_rules() -> dict[str, list[str]]:
    return {
        "art": ["painting", "sculpture", "gallery", "art", "arts"],
        "history": ["history", "historic", "heritage", "memorial", "war", "ancient", "museum of the city"],
        "science": ["science", "technology", "innovation", "space", "planetarium", "natural history"],
        "kids": ["children", "kids", "family", "interactive", "hands-on"],
        "nature": ["zoo", "botanical", "garden", "park", "aquarium", "wildlife", "natural"],
        "architecture": ["architecture", "design"],
        "music": ["music", "jazz"],
        "transportation": ["aviation", "air", "rail", "subway", "transit", "maritime", "ship"],
    }

def assign_tags_to_row(text: str, rules: dict[str, list[str]]) -> list[str]:
    if not isinstance(text, str):
        text = ""
    t = text.lower()

    found = []
    for tag, keywords in rules.items():
        for kw in keywords:
            # basic substring match is enough for MVP
            if kw in t:
                found.append(tag)
                break

    # fallback so every attraction has at least one tag
    if not found:
        found = ["culture"]
    return found
