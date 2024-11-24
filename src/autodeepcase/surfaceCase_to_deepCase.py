import csv
from utiles import add_surfaceOrDeep_case, utile
import re
import json
import copy


# input_text = '彼は<ガ格>読書が<ガ格>好きだ<述語動詞>'
# input_text = '10日(土)午後3時には<時間格>日本の東に<ニ格>あって、<述語動詞>'
# input_text = '店で<デ格>買い物を<ヲ格>する<述語動詞>'
# input_text = 'わしが<ガ格>扇で<デ格>合図を<ヲ格>する<述語動詞>'
# input_text = '私には<ニ格>度胸が<ガ格>ありません。<述語動詞>'
# input_text = '午後八時に<ニ格>点呼がある<述語動詞>'
# input_text = 'おじいさんが<ガ格>孫を<ヲ格>寝かしつけようとしている<ト格>'
# input_text = '岸田首相が<ga>バイデン大統領と<to>会談する<述語動詞>'
input_text = '子供が<ga>学校から<kara>帰る<述語動詞>'

# # 実験用
# surface_dict = utile.parse_text_to_dict_lists(input_text)

# # 表層格のみ
# # 'case'と'text'キーだけを抽出する
# filtered_surface_dict = [{key: item[key]
#                           for key in ['text', 'case']} for item in surface_dict]
# print(filtered_surface_dict)

# # 深層格付与後
# deep_dict = add_surfaceOrDeep_case.add_deepCase(surface_dict)
# # 'case'と'text'キーだけを抽出する
# filtered_deep_dict = [{key: item[key]
#                        for key in ['text', 'case']} for item in deep_dict]
# print(filtered_deep_dict)


def surfaceCase_to_deepCase(surface_dict_list):
    deepCased_predicate_clauses_list = []
    for predicate_clause in surface_dict_list:
        # print(predicate_clause)

        # 深層格付与
        deepCased_predicate_clauses_list.append(
            add_surfaceOrDeep_case.add_deepCase(predicate_clause))
        # print(predicate_clauses_list)

    # deepCased_sentences_dict = []
    # # 読み込んだデータを表示
    # for sentences in surface_dict_list:
    #     deepCased_sentence_dict = []
    #     for surface_dict in sentences:
    #         # 深層格付与
    #         deep_dict = add_surfaceOrDeep_case.add_deepCase(surface_dict)
    #         deepCased_sentence_dict.append(deep_dict)
    #     deepCased_sentences_dict.append(deepCased_sentence_dict)

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

    return deepCased_predicate_clauses_list


# "deep_case"が空白文字またはnoneの場合後ろの要素と結合させる
def delete_empty_deep_case(record):
    # 指定されたレコードに対して処理を実行
    for key in ["sentence_1", "sentence_2"]:  # 両方のキーに対して処理
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
    for key in ["sentence_1", "sentence_2"]:  # 処理対象のキー
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
    with open('../../data/surfaceCased_sentences.json', 'r', encoding='utf-8') as f:
        surface_dict_lists = json.load(f)

        deepCased_sentences_dict = []

        for item in surface_dict_lists:
            predicate_clauses_1 = []
            predicate_clauses_2 = []

            # sentence1に対する処理
            predicate_clauses_1 = surfaceCase_to_deepCase(
                item['sentence_1'])

            # sentence2に対する処理
            predicate_clauses_2 = surfaceCase_to_deepCase(
                item['sentence_2'])

            predicate_clause_record = {'sentence_pair_id': item['sentence_pair_id'],
                                       'sentence_1': predicate_clauses_1, 'sentence_2': predicate_clauses_2, 'label': item['label']}

            deepCased_sentences_dict.append(predicate_clause_record)

    # JSON形式の文字列に変換
    json_data = json.dumps(deepCased_sentences_dict,
                           ensure_ascii=False, indent=4)

    # ファイルに書き出す
    with open('../../data/deepCased_sentences.json', 'w', encoding='utf-8') as f:
        f.write(json_data)

    # "deep_case"が空白文字またはnoneの場合後ろの要素と結合させる
    with open('../../data/deepCased_sentences.json', 'r', encoding='utf-8') as f:
        deepCased_sentences_include_empty_dict_lists = json.load(f)
        deepCased_sentences_dict = []
        deepCased_sentences_dict2 = []

        for record in deepCased_sentences_include_empty_dict_lists:
            deepCased_sentences_dict.append(delete_empty_deep_case(record))

        for record in deepCased_sentences_dict:
            deepCased_sentences_dict2.append(merge_sahendoushi(record))

    # JSON形式の文字列に変換
    json_data = json.dumps(deepCased_sentences_dict,
                           ensure_ascii=False, indent=4)

    with open('../../data/deepCased_sentences.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


if __name__ == "__main__":
    main()
