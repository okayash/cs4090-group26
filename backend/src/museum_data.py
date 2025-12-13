import pandas as pd

def load_museum_data(file_path: str) -> pd.DataFrame:
    '''
    Load museum data from a CSV file into a pandas DataFrame.
    '''
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading museum data: {e}")
        return pd.DataFrame()
    
def parse_museum_data(df: pd.DataFrame) -> list[dict]:
    '''
    Parse the museum DataFrame into a list of dictionaries.
    '''
    museums = []
    for _, row in df.iterrows():
        museum = {
            "id": row.get("id"),
            "name": row.get("name"),
            "description": row.get("description"),
            "location": row.get("location"),
            "type": row.get("type"),
            "rating": row.get("rating"),
            "tags": row.get("tags", "").split(",") if pd.notna(row.get("tags")) else [],
        }
        museums.append(museum)
    return museums
    
def tag_museums():
    '''
    tag museums with certain interest categories based on their names or descriptions
    '''
    tags = {
        "art": ["painting", "sculpture", "gallery", "arts", "art"],
        "history": ["ancient", "medieval", "modern", "war", "history", "memorial", "culture", "cultural", "american", "heritage"],
        "science": ["technology", "natural history", "space", "air", "space", "science", "innovation"],
        "child-friendly": ["children", "kids", "family", "zoo", "interactive"],
        "natural": ["zoo", "plants", "trail"],
    }
    return tags