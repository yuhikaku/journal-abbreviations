# README

法律関連の各種媒体の表記一覧です（随時更新）。

[有斐閣ONLINE](https://yuhikaku.com/)における表記の基準の1つとして利用を予定しています。

## [`journals.json`](./journals.json)

| フィールド | 意味 |
| :--- | :--- |
| `id` | 乱数によるID |
| `canonical_name` | 正規化名（この値を表示に用いる） |
| `names` | 名称（表記揺れを配列で表現） |
| `abbrevs` | 略称（表記揺れを配列で表現） |


[`validate.py`](./validate.py) によってID・名称・略称に重複がないことを確認しています。

## [`journals.csv`](./journals.csv)

- [`journals.json`](./journals.json) を [`csvnize.py`](./csvnize.py) によって変換したCSVファイルです
- 略称か否かを `abbrev_flag` 列で表現しています（1=略称）


