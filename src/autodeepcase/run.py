import csv
import json
from pyknp import KNP, Juman
import parseByPyknp
import surfaceCase_to_deepCase
from utiles import utile
from tqdm import tqdm

# # TSVファイルを開く
# with open('../../data/jnli_train.tsv', mode='r', encoding='utf-8') as file:
#     # csv.readerにタブ文字をdelimiterとして指定
#     tsv_reader = csv.reader(file, delimiter='\t')
#     roop_num = 0
#     surface_cased_dict = []
#     for text in tsv_reader:
#         if 0 < roop_num < 11:
#             surface_cased_sentences = parseByPyknp.parseByknp(text[8])
#             sentences = []
#             for sentence in surface_cased_sentences:
#                 sentences.append(utile.parse_text_to_dict_lists(sentence[0]))
#             surface_cased_dict.append(sentences)
#         roop_num += 1

# knpをインスタンス化
knp = KNP()
# 平文をjumanに投入し、意味情報を得る
jumanpp = Juman()

# json形式を開く
with open('../../../datas/jnli-valid-v1.1.json', 'r', encoding='utf-8') as file:
    data = [json.loads(l) for l in file.readlines()]

surface_cased_dict = []
roop_num = 0
# tqdmを使って進捗バーを表示
for item in tqdm(data, desc="Processing Data", unit="item"):
    # print(item['sentence1'], item['sentence2'])
    predicate_clauses_1 = []
    predicate_clauses_2 = []

    # sentence1に対する処理
    surface_cased_sentences_1_dicts = parseByPyknp.parseByknp(
        item['sentence1'], KNP=knp)
    # for sentence in surface_cased_sentences_1:
    #     predicate_clauses_1.append(
    #         utile.parse_text_to_dict_lists(sentence[0], jumanpp=jumanpp))
    for a_predicate_term in surface_cased_sentences_1_dicts:
        predicate_clauses_1.append(
            utile.parse_text_to_dict_lists(a_predicate_term, jumanpp=jumanpp))

    # sentence2に対する処理
    surface_cased_sentences_2_dicts = parseByPyknp.parseByknp(
        item['sentence2'], KNP=knp)
    # for sentence in surface_cased_sentences_2:
    #     predicate_clauses_2.append(
    #         utile.parse_text_to_dict_lists(sentence[0], jumanpp=jumanpp))
    for a_predicate_term in surface_cased_sentences_2_dicts:
        predicate_clauses_2.append(
            utile.parse_text_to_dict_lists(a_predicate_term, jumanpp=jumanpp))

    predicate_clause_record = {'sentence_pair_id': item['sentence_pair_id'],
                               'sentence_1': predicate_clauses_1, 'sentence_2': predicate_clauses_2, 'label': item['label']}
    surface_cased_dict.append(predicate_clause_record)

    # roop_num += 1
    # if roop_num % 10 == 0:
    #     print(roop_num)

# JSON形式の文字列に変換
json_data = json.dumps(
    surface_cased_dict, ensure_ascii=False, indent=4)

# ファイルに書き出す
with open('../../data/10_26_surfaceCased_sentences.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

print('---------Parsing is complete---------')

# ファイルを開いてJSONデータを読み込む
with open('../../data/10_26_surfaceCased_sentences.json', 'r', encoding='utf-8') as f:
    surface_dict_lists = json.load(f)

    deepCased_sentences_dict = []

    roop_num = 0
    for item in surface_dict_lists:
        predicate_clauses_1 = []
        predicate_clauses_2 = []

        # sentence1に対する処理
        predicate_clauses_1 = surfaceCase_to_deepCase.surfaceCase_to_deepCase(
            item['sentence_1'])

        # sentence2に対する処理
        predicate_clauses_2 = surfaceCase_to_deepCase.surfaceCase_to_deepCase(
            item['sentence_2'])

        predicate_clause_record = {'sentence_pair_id': item['sentence_pair_id'],
                                   'sentence_1': predicate_clauses_1, 'sentence_2': predicate_clauses_2, 'label': item['label']}

        deepCased_sentences_dict.append(predicate_clause_record)
        # print(deep_cased_dict)

        roop_num += 1
        if roop_num % 10 == 0:
            print(roop_num)

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
    for record in deepCased_sentences_include_empty_dict_lists:
        deepCased_sentences_dict.append(
            surfaceCase_to_deepCase.delete_empty_deep_case(record))

# JSON形式の文字列に変換
json_data = json.dumps(deepCased_sentences_dict,
                       ensure_ascii=False, indent=4)

with open('../../data/deepCased_sentences.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
print('---------done---------')