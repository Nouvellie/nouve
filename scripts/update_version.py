import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
METADATA_DIR = BASE_DIR / "metadata"

def update_version(new_version, new_changes):
    changelog_path = METADATA_DIR / "changelog.json"
    history_path = METADATA_DIR / "version_history.json"

    current_data = {
        "current_version": new_version,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "changes": new_changes
    }

    with changelog_path.open("w") as changelog_file:
        json.dump(current_data, changelog_file, indent=4)

    try:
        with history_path.open("r+") as history_file:
            history_data = json.load(history_file)
            history_data["history"].append(current_data)
            history_file.seek(0)
            json.dump(history_data, history_file, indent=4)
    except FileNotFoundError:
        with history_path.open("w") as history_file:
            json.dump({"history": [current_data]}, history_file, indent=4)

    print(f"Version {new_version} recorded successfully.")

if __name__ == "__main__":
    # Interactive input from the terminal
    new_version = input("Enter the new version (e.g., 1.3.0): ")
    print("Enter the list of changes (end input with an empty line):")
    changes = []
    while True:
        change = input("- ")
        if change == "":
            break
        changes.append(change)
    
    update_version(new_version, changes)