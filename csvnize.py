import csv
import json


def main() -> None:

    lines = [("name", "display_name", "journal_id", "abbrev_flag")]
    with open("journals.json", "r", encoding="utf-8") as f:
        content = json.load(f)
        for data in content:
            journal_id = data["id"]
            display_name = data["display_name"]
            for name in data["names"]:
                lines.append((name, display_name, journal_id, "0"))
            for abbrev in data["abbrevs"]:
                lines.append((abbrev, display_name, journal_id, "1"))

    with open("journals.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(lines)


if __name__ == "__main__":
    main()
