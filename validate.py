import collections
import json


def main() -> None:
    all_ids = []
    all_display_names = []
    tokens = []

    with open("journals.json", "r", encoding="utf-8") as f:
        content = json.load(f)
        for data in content:
            all_ids.append(data["id"])
            all_display_names.append(data["display_name"])
            tokens.extend(data["names"])
            abbrevs = [a for a in data["abbrevs"] if a != ""]
            if len(abbrevs) != 0:
                tokens.extend(abbrevs)

    for name, item_list in {
        "id": all_ids,
        "display_name": all_display_names,
        "token": tokens,
    }.items():
        for item, count in collections.Counter(item_list).items():
            if count != 1:
                raise ValueError(f"{name}で「{item}」が{count}件重複しています。")

    print("問題は検出されませんでした")


if __name__ == "__main__":
    main()
