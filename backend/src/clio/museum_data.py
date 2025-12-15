import os
import re
import pandas as pd

from .db import get_conn  

def get_tag_rules() -> dict[str, list[str]]:
    '''
    some key words associated with the names of museums and attractions
    '''
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


def assign_tags(text: str, rules: dict[str, list[str]]) -> list[str]:
    '''
    assign interests tags based on name
    '''
    t = (text or "").lower()
    found: list[str] = []
    for tag, kws in rules.items():
        if any(kw in t for kw in kws):
            found.append(tag)
    return found or ["culture"]


def extract_state(address: str) -> str | None:
    '''
    return the state within the address
    '''
    if not isinstance(address, str):
        return None
    m = re.search(r",\s*([A-Z]{2})\s*\d{5}(?:-\d{4})?\b", address)
    return m.group(1) if m else None


def extract_city(address: str) -> str | None:
    '''
    return the city within the address
    '''
    if not isinstance(address, str):
        return None
    parts = [p.strip() for p in address.split(",")]
    if len(parts) >= 2:
        return parts[1]
    return None

def _print_db_info(cur) -> None:
    '''
    print database info for debugging
    '''
    cur.execute("SELECT DATABASE()")
    db_name = cur.fetchone()[0]
    print("DB connected to:", db_name)

    cur.execute("SELECT COUNT(*) FROM Attractions")
    before = cur.fetchone()[0]
    print("Attractions BEFORE:", before)


def _safe_fetchone(cur, err_msg: str) -> tuple:
    '''
    fetch one row from cursor, raise error if none
    Returns the fetched row tuple.
    '''
    row = cur.fetchone()
    if not row:
        raise RuntimeError(err_msg)
    return row

def seed_from_csv(
    csv_filename: str = "tripadvisor_museum_USonly.csv",
    seed_tags: bool = True,
    limit: int | None = None,
) -> None:
    '''
    load the tripadvisor museum dataset
    
    '''
    here = os.path.dirname(os.path.abspath(__file__))
    csv_path = csv_filename if os.path.isabs(csv_filename) else os.path.join(here, csv_filename)

    print("CWD:", os.getcwd())
    print("Script dir:", here)
    print("CSV path:", csv_path)
    print("CSV exists:", os.path.exists(csv_path))

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    df = pd.read_csv(csv_path)
    print("Rows in CSV:", len(df))
    print("Columns:", list(df.columns))

    required_cols = ["MuseumName", "Address", "Description", "Fee", "Rating"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")

    if limit is not None:
        df = df.head(int(limit))
        print("Limiting rows to:", len(df))

    rules = get_tag_rules()

    conn = get_conn()
    cur = conn.cursor()

    try:
        _print_db_info(cur)

        insert_attraction = '''
            INSERT INTO Attractions (name, `type`, city, price, rating)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              `type`=VALUES(`type`),
              city=VALUES(city),
              price=VALUES(price),
              rating=VALUES(rating)
        '''

        insert_tag = '''
            INSERT INTO Attraction_Tags (tag_name)
            VALUES (%s)
            ON DUPLICATE KEY UPDATE tag_name=tag_name
        '''
        get_tag_id = "SELECT tag_id FROM Attraction_Tags WHERE tag_name = %s"

        insert_tag_map = '''
            INSERT IGNORE INTO Attraction_Tags_Map (attraction_name, tag_id)
            VALUES (%s, %s)
        '''

        processed = 0
        inserted_preview = 0

        for i, row in df.iterrows():
            name = str(row.get("MuseumName", "")).strip()
            if not name:
                continue

            address = str(row.get("Address", "")).strip()
            desc = str(row.get("Description", "")).strip()

            city = extract_city(address) or "Unknown"

            fee_raw = str(row.get("Fee", "")).strip().lower()

            price = 1.0 if fee_raw.startswith("y") else 0.0

            rating = row.get("Rating", None)

            _state = extract_state(address)

            a_type = "museum"


            if inserted_preview < 3:
                print(f"INSERT PREVIEW: {name} | city={city} | state={_state} | rating={rating} | fee={fee_raw}")
                inserted_preview += 1

            cur.execute(insert_attraction, (name, a_type, city, price, rating))


            if seed_tags:
                tags = assign_tags(f"{name} {desc}", rules)
                for tag in tags:
                    cur.execute(insert_tag, (tag,))
                    cur.execute(get_tag_id, (tag,))
                    tag_id = _safe_fetchone(cur, f"Could not fetch tag_id for tag={tag!r}")[0]
                    cur.execute(insert_tag_map, (name, tag_id))

            processed += 1

        conn.commit()

        cur.execute("SELECT COUNT(*) FROM Attractions")
        after = cur.fetchone()[0]
        print("Processed rows:", processed)
        print("Attractions AFTER:", after)

        if after == 0:
            print(
                "\nNothing"
            )
    finally:
        cur.close()
        conn.close()


def main():
    seed_from_csv(
        csv_filename="tripadvisor_museum_USonly.csv",
        seed_tags=True,
        limit=None, 
    )

if __name__ == "__main__":
    main()
