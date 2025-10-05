import json
from pathlib import Path

def load_data():
    """
    Load preprocessed NASA bio data from JSON file.
    Validates and cleans data to prevent null-related issues.
    """
    data_path = Path("data/nasa_bio_data.json")
    
    if not data_path.exists():
        print(f"⚠️ Warning: Data file not found at {data_path.resolve()}")
        print("⚠️ Starting with empty dataset. Add nasa_bio_data.json to continue.")
        return []
    
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        
        # Validate and clean data
        cleaned_data = []
        for item in raw_data:
            # Ensure required fields exist
            if not isinstance(item, dict):
                continue
            
            # Add defaults for missing fields
            cleaned_item = {
                "id": item.get("id", "unknown"),
                "title": item.get("title", "Untitled Dataset"),
                "domain": item.get("domain", None),
                "description": item.get("description", ""),
                "keywords": item.get("keywords") if isinstance(item.get("keywords"), list) else [],
                "data_url": item.get("data_url", None),
                "data_type": item.get("data_type", None),
                "release_date": item.get("release_date", None),
                "authors": item.get("authors") if isinstance(item.get("authors"), list) else [],
                "variables": item.get("variables") if isinstance(item.get("variables"), list) else []
            }
            
            cleaned_data.append(cleaned_item)
        
        print(f"✅ Loaded {len(cleaned_data)} datasets successfully")
        return cleaned_data
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {data_path}: {e}")
        return []
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return []

DATA = load_data()
