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


def has_space_around(s: str) -> bool:
    return s != s.strip()


def main() -> None:
    json_path = "journals.json"
    id_stack = []
    canonical_name_stack = []
    keyword_stack = []

    with open(json_path, "r", encoding="utf-8") as f:
        content = json.load(f)
        for data in content:
            data_id = data["id"]
            canonical_name = data["canonical_name"]
            names = data["names"]
            abbrevs = data["abbrevs"]

            for elem in [data_id, canonical_name] + names + abbrevs:
                if elem == "":
                    raise ValueError(f"{data_id}に空文字が含まれています")
                if elem.strip() == "":
                    raise ValueError(f"{data_id}に空白文字のみの要素が含まれています")
                if elem != elem.strip():
                    raise ValueError(f"{data_id}「{elem}」の前後に空白があります")

            id_stack.append(data_id)

            keywords = names + abbrevs

            if canonical_name not in keywords:
                raise ValueError(
                    f"正規化名「{canonical_name}」として、 names にも abbrevs にも含まれていない文字列が指定されています"
                )
            canonical_name_stack.append(canonical_name)

            keyword_stack.extend(keywords)

    for name, stack in {
        "ID": id_stack,
        "正規化名称": canonical_name_stack,
        "キーワード": keyword_stack,
    }.items():
        for item, count in collections.Counter(stack).items():
            if count != 1:
                raise ValueError(f"{name}で「{item}」が{count}件重複しています。")

    for data_id in id_stack:
        _, suffix = data_id.split("-")
        if not re.fullmatch(r"[A-Z0-9]{6}", suffix):
            raise ValueError(f"{data_id}: IDの文字数が正しくありません")

    print("問題は検出されませんでした。CSV形式に変換します。")
    convert_to_csv(json_path)


if __name__ == "__main__":
    main()
