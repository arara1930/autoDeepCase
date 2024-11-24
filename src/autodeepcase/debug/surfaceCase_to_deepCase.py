import csv
from utiles import add_surfaceOrDeep_case, utile
import re
import json


# 1文ずつ引数にとる
# surface_dict_list = [
#             [
#                 {
#                     "text": "南海トラフ地震の臨時情報（巨大地震注意）発表を",
#                     ...
#                 },
#                 ...
#             ],
#             [
#                 ...
#             ]
#             ...
# ]


def surfaceCase_to_deepCase(surface_dict_list):
    deepCased_predicate_clauses_list = []
    for predicate_clause in surface_dict_list:
        # print(predicate_clause)

        # 深層格付与
        deepCased_predicate_clauses_list.append(
            add_surfaceOrDeep_case.add_deepCase(predicate_clause))
        # print(predicate_clauses_list)

    # # 本番環境とループの回し方が違うので注意
    # deepCased_sentences_dict = []
    # # 読み込んだデータを表示
    # for sentence in surface_dict_list:
    #     predicate_clauses_list = []
    #     predicate_clauses = sentence['predicate_clauses']
    #     for predicate_clause in predicate_clauses:
    #         # print(predicate_clause)

    #         # 深層格付与
    #         predicate_clauses_list.append(
    #             add_surfaceOrDeep_case.add_deepCase(predicate_clause))
    #     predicate_clause_record = {'predicate_clauses': predicate_clauses_list}
    # deepCased_sentences_dict.append(predicate_clause_record)

    # 以下、デバッグ用
    # # 表層格のみ
    # # 'case'と'text'キーだけを抽出する
    # filtered_surface_dict = [{key: item[key]
    #                           for key in ['text', 'case']} for item in surface_dict]
    # print('-------表層格-------')
    # print(filtered_surface_dict)

    # # 深層格のみ
    # # 'case'と'text'キーだけを抽出する
    # filtered_deep_dict = [{key: item[key]
    #                        for key in ['text', 'case']} for item in deep_dict]
    # print('-------深層格-------')
    # print(filtered_deep_dict)
    # print('\n')

    # return deepCased_sentences_dict
    return deepCased_predicate_clauses_list

# "deep_case"が空白文字またはnoneの場合後ろの要素と結合させる


def delete_empty_deep_case(record):
    # 指定されたレコードに対して処理を実行
    for key in ["predicate_clauses"]:  # 両方のキーに対して処理
        for sentence in record[key]:
            while True:  # "deep_case" がなくなるまで繰り返す
                merged_sentence = []  # 結果を格納するリスト
                skip_next = False  # 次の要素をスキップするフラグ
                has_empty_deep_case = False  # "deep_case": "" が存在するかを判定

                for i in range(len(sentence)):
                    if skip_next:
                        skip_next = False
                        continue

                    current = sentence[i]

                    # "deep_case" が空であれば次の要素と結合
                    if current["deep_case"] == "" or current["deep_case"] == "none":
                        has_empty_deep_case = True  # 空の "deep_case" があったことを記録

                        # 次の要素が存在する場合
                        if i + 1 < len(sentence):
                            next_item = sentence[i + 1]
                            # "text" を結合
                            current["text"] += next_item["text"]
                            # "symple_phrase" を False に設定
                            current["symple_phrase"] = False
                            # "surface_case" と "deep_case" を次の要素から引き継ぎ
                            current["surface_case"] = next_item["surface_case"]
                            current["deep_case"] = next_item["deep_case"]
                            # "imisByJuman" と "imisByJuman" を結合
                            current["imisByJuman"] += next_item["imisByJuman"]
                            current["imisByKnp"] += next_item["imisByKnp"]
                            # 次の要素をスキップ
                            skip_next = True

                    # 結合済みまたはそのままの要素を結果に追加
                    merged_sentence.append(current)

                # sentence の更新
                sentence[:] = merged_sentence

                # "deep_case": "" がもうない場合ループを終了
                if not has_empty_deep_case:
                    break

    return record


def merge_sahendoushi(record):
    for key in ["predicate_clauses"]:  # 処理対象のキー
        for sentence in record[key]:
            while True:  # 無限ループ。ただし has_sahendoushi が False の場合終了
                merged_sentence = []  # 結合後のリストを格納
                skip_next = False  # 次の要素をスキップするフラグ
                has_sahendoushi = False  # ループ内で <サ変> が見つかったかどうか

                for i in range(len(sentence)):
                    if skip_next:
                        skip_next = False
                        continue

                    current = sentence[i]

                    # <サ変> が含まれているか確認
                    pattern_sahendoushi = r'<サ変>(.*?)<非用言格解析:動>'
                    match_sahendoushi = re.search(
                        pattern_sahendoushi, current.get('imisByKnp', ''))

                    # 条件を満たす場合に次の要素と結合
                    if match_sahendoushi and i + 1 < len(sentence):
                        next_item = sentence[i + 1]

                        if next_item['deep_case'] == '<述語動詞>' or next_item['deep_case'] == '<受動態>':
                            has_sahendoushi = True  # ループ継続の条件をセット
                            # "text" を結合
                            current["text"] += next_item["text"]
                            # "symple_phrase" を False に設定
                            current["symple_phrase"] = False
                            # "surface_case" と "deep_case" を次の要素から引き継ぎ
                            current["surface_case"] = next_item["surface_case"]
                            current["deep_case"] = next_item["deep_case"]
                            # "imisByJuman" と "imisByJuman" を結合
                            current["imisByJuman"] += next_item["imisByJuman"]
                            current["imisByKnp"] += next_item["imisByKnp"]
                            # 次の要素をスキップ
                            skip_next = True

                    # 結合済みまたはそのままの要素を追加
                    merged_sentence.append(current)

                # sentence を更新
                sentence[:] = merged_sentence

                # <サ変> がもう存在しない場合ループを終了
                if not has_sahendoushi:
                    break

    return record


def main():
    # ファイルを開いてJSONデータを読み込む
    with open('../../../data/debug/surfaceCased_sentences.json', 'r', encoding='utf-8') as f:
        surface_dict_lists = json.load(f)
    # print(surface_dict_lists[0]['predicate_clauses'])
    # surfaceCase_to_deepCase(surface_dict_lists[0]['predicate_clauses'])

    deep_cased_dict = []
    for surface_dict_list in surface_dict_lists:
        # print(surface_dict_list['predicate_clauses'])
        predicate_clauses = surfaceCase_to_deepCase(
            surface_dict_list['predicate_clauses'])
        # print(predicate_clauses)
        predicate_clause_record = {'predicate_clauses': predicate_clauses}
        deep_cased_dict.append(predicate_clause_record)
        # print(deep_cased_dict)

    # JSON形式の文字列に変換
    json_data = json.dumps(deep_cased_dict,
                           ensure_ascii=False, indent=4)

    # ファイルに書き出す
    with open('../../../data/debug/deepCased_sentences.json', 'w', encoding='utf-8') as f:
        f.write(json_data)

    # "deep_case"が空白文字またはnoneの場合後ろの要素と結合させる
    with open('../../../data/debug/deepCased_sentences.json', 'r', encoding='utf-8') as f:
        deepCased_sentences_include_empty_dict_lists = json.load(f)
        deepCased_sentences_dict = []
        deepCased_sentences_dict2 = []

        for record in deepCased_sentences_include_empty_dict_lists:
            deepCased_sentences_dict.append(delete_empty_deep_case(record))

        for record in deepCased_sentences_dict:
            deepCased_sentences_dict2.append(merge_sahendoushi(record))

    # JSON形式の文字列に変換
    json_data = json.dumps(deepCased_sentences_dict2,
                           ensure_ascii=False, indent=4)

    with open('../../../data/debug/deepCased_sentences.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


if __name__ == "__main__":
    main()
