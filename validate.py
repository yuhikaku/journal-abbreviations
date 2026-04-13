import collections
import json
import re


def main() -> None:
    all_ids = []
    all_canonical_names = []
    tokens = []

    with open("journals.json", "r", encoding="utf-8") as f:
        content = json.load(f)
        for data in content:
            all_ids.append(data["id"])
            all_canonical_names.append(data["canonical_name"])
            tokens.extend(data["names"])
            for abbrev in data["abbrevs"]:
                if abbrev != "":
                    tokens.append(abbrev)

    for name, item_list in {
        "id": all_ids,
        "canonical_name": all_canonical_names,
        "token": tokens,
    }.items():
        for item, count in collections.Counter(item_list).items():
            if count != 1:
                raise ValueError(f"{name}で「{item}」が{count}件重複しています。")

    for jid in all_ids:
        _, suffix = jid.split("-")
        if not re.fullmatch(r"[A-Z0-9]{6}", suffix):
            raise ValueError(f"{jid}: IDの文字数が正しくありません")

    print("問題は検出されませんでした")


if __name__ == "__main__":
    main()
