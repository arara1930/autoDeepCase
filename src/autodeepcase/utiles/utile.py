import re
from pyknp import Juman
from collections import Counter


def use_juman(jumanpp, text):
    result = jumanpp.analysis(text)
    imis_list = []
    for mrph in result.mrph_list():  # 各形態素にアクセス
        imis_list.append(mrph.imis)
    result = ''.join(imis_list)
    return result


# 要素の重複を判定し、重複要素を返す
def find_duplicates(lst):
    counter = Counter(lst)
    return [item for item, count in counter.items() if count > 1]


def parse_text_to_dict_lists(phrase_dict, jumanpp):
    print("a_predicate_term", phrase_dict)
    print('\n')

    # それぞれのキーを別々のリストに格納
    text = []
    surface_case = []
    deep_case = []
    imisByJuman_text = []
    imisByKnp_text = []
    symple_phrase = []
    for phrase in phrase_dict:
        text.append(phrase['phrase'])
        surface_case.append(phrase['surfaceCase'])

        # tag_partsの要素数分の'none'をdeep_caseに追加する
        # <述語動詞><時間格>などの表層格以外のタグについてはそのまま追加する
        pattern_kanji = r'[\u4E00-\u9FFF]+'
        match_kanji = re.search(pattern_kanji, phrase['surfaceCase'])
        if match_kanji:
            deep_case.append(phrase['surfaceCase'])
        else:
            deep_case.append('none')

        imisByJuman_text.append(use_juman(jumanpp, phrase['phrase']))

        imisByKnp_text.append(phrase['imisByKnp'])

        symple_phrase.append(phrase['symple_phrase'])

    keys = ['text', 'surface_case', 'deep_case',
            'imisByJuman', 'imisByKnp', 'symple_phrase']
    # 辞書型のリストにまとめる
    dict_list = [dict(zip(keys, values))
                 for values in zip(text, surface_case, deep_case, imisByJuman_text, imisByKnp_text, symple_phrase)]

    return dict_list

# def parse_text_to_dict_lists(text, jumanpp):
#     print("sentence[0]", text)

#     # 正規表現を用いて、<>で囲まれた部分とその他の平文を分離する
#     pattern = r'(<[^>]*>)'

#     # パターンにマッチする部分を探し、リストに分割する
#     parts = re.split(pattern, text)

#     # 平文とタグで囲まれた部分を別々のリストに格納
#     plain_text_parts = []
#     tag_parts = []
#     deep_case = []
#     imisByJuman_text = []

#     for part in parts:
#         if part.startswith('<') and part.endswith('>'):
#             tag_parts.append(part.strip())
#         elif part.strip():
#             plain_text_parts.append(part.strip())

#     # tag_partsの要素数分の'none'をdeep_caseに追加する
#     # <述語動詞><時間格>などの表層格以外のタグについてはそのまま追加する
#     pattern_kanji = r'[\u4E00-\u9FFF]+'
#     for tag in tag_parts:
#         match_kanji = re.search(pattern_kanji, tag)
#         if match_kanji:
#             deep_case.append(tag)
#         else:
#             deep_case.append('none')

#     for text in plain_text_parts:
#         imisByJuman_text.append(use_juman(jumanpp, text))

#     keys = ['text', 'surface_case', 'deep_case', 'imisByJuman']
#     # 辞書型のリストにまとめる
#     dict_list = [dict(zip(keys, values))
#                  for values in zip(plain_text_parts, tag_parts, deep_case, imisByJuman_text)]

#     return dict_list
