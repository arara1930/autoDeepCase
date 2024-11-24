import json
# # サンプルデータ（ユーザーが提供したデータ）
# data = [
#     {
#         "sentence_pair_id": "0",
#         "sentence_1": [
#             [
#                 {
#                     "text": "時計がついている場所に",
#                     "surface_case": "<ni>",
#                     "deep_case": "<場所格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "パブリックマーケットセンターとかかれた看板が",
#                     "surface_case": "<ga>",
#                     "deep_case": "<場所格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "設置されています。",
#                     "surface_case": "<受動態>",
#                     "deep_case": "<受動態>",
#                     "imis": "..."
#                 }
#             ]
#         ],
#         "sentence_2": [
#             [
#                 {
#                     "text": "屋根の上に",
#                     "surface_case": "<ni>",
#                     "deep_case": "<場所格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "看板が",
#                     "surface_case": "<ga>",
#                     "deep_case": "<主格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "あり",
#                     "surface_case": "<述語動詞>",
#                     "deep_case": "<述語動詞>",
#                     "imis": "..."
#                 }
#             ],
#             [
#                 {
#                     "text": "時計も",
#                     "surface_case": "<mo>",
#                     "deep_case": "<主格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "ついています。",
#                     "surface_case": "<述語動詞>",
#                     "deep_case": "<述語動詞>",
#                     "imis": "..."
#                 }
#             ]
#         ],
#         "label": "neutral"
#     },
#     {
#         "sentence_pair_id": "1",
#         "sentence_1": [
#             [
#                 {
#                     "text": "キリンが、",
#                     "surface_case": "<ga>",
#                     "deep_case": "<主格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "木の中から",
#                     "surface_case": "<kara>",
#                     "deep_case": "<起点格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "首を",
#                     "surface_case": "<wo>",
#                     "deep_case": "<対象格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "出しています。",
#                     "surface_case": "<述語動詞>",
#                     "deep_case": "<述語動詞>",
#                     "imis": "..."
#                 }
#             ]
#         ],
#         "sentence_2": [
#             [
#                 {
#                     "text": "キリンが",
#                     "surface_case": "<ga>",
#                     "deep_case": "<主格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "木々のあいだから",
#                     "surface_case": "<kara>",
#                     "deep_case": "<起点格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "顔を",
#                     "surface_case": "<wo>",
#                     "deep_case": "<対象格>",
#                     "imis": "..."
#                 },
#                 {
#                     "text": "出しています。",
#                     "surface_case": "<述語動詞>",
#                     "deep_case": "<述語動詞>",
#                     "imis": "..."
#                 }
#             ]
#         ],
#         "label": "entailment"
#     }
# ]

# 同一述語項内に重複するdeep_caseがないか確認する関数


def check_duplicate_deep_case(data):
    count = 0
    for entry in data:
        sentence_1 = entry.get("sentence_1", [])
        for predicate in sentence_1:
            deep_cases = [item["deep_case"] for item in predicate]
            # 同一deep_caseが存在するか確認
            if len(deep_cases) != len(set(deep_cases)):
                print(
                    f"Duplicate deep_case found in sentence_pair_id {entry['sentence_pair_id']}")
                print(f"Deep cases: {deep_cases}")
                count += 1
    print(count)


def main():
    # ファイルを開いてJSONデータを読み込む
    with open('../../data/deepCased_sentences.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 重複チェックを実行
    check_duplicate_deep_case(data)


if __name__ == "__main__":
    main()
