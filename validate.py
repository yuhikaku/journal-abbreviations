import collections
import csv
import json
import re
from pathlib import Path


def convert_to_csv(json_path: str) -> None:
    lines = [("name", "canonical_name", "journal_id", "abbrev_flag")]
    with open(json_path, "r", encoding="utf-8") as f:
        content = json.load(f)
        for data in content:
            journal_id = data["id"]
            canonical_name = data["canonical_name"]
            for name in data["names"]:
                lines.append((name, canonical_name, journal_id, "0"))
            for abbrev in data["abbrevs"]:
                lines.append((abbrev, canonical_name, journal_id, "1"))

    out_csv_path = Path(json_path).with_suffix(".csv")
    with open(out_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(lines)


def main() -> None:
    json_path = "journals.json"
    all_ids = []
    all_canonical_names = []
    tokens = []

    with open(json_path, "r", encoding="utf-8") as f:
        content = json.load(f)
        for data in content:
            all_ids.append(data["id"])

            entry_tokens = []
            entry_tokens.extend(data["names"])
            for abbrev in data["abbrevs"]:
                if abbrev != "":
                    entry_tokens.append(abbrev)

            canonical_name = data["canonical_name"]
            if canonical_name not in entry_tokens:
                raise RuntimeError(
                    f"正規化名「{canonical_name}」として、 names にも abbrevs にも含まれていない文字列が指定されています"
                )
            all_canonical_names.append(canonical_name)

            tokens.extend(entry_tokens)

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

    print("問題は検出されませんでした。CSV形式に変換します。")
    convert_to_csv(json_path)


if __name__ == "__main__":
    main()
