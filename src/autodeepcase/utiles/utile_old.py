import re
from pyknp import Juman


def use_juman(jumanpp, text):
    result = jumanpp.analysis(text)
    imis_list = []
    for mrph in result.mrph_list():  # 各形態素にアクセス
        imis_list.append(mrph.imis)
    result = ''.join(imis_list)
    return result


def parse_text_to_dict_lists(text, jumanpp):

    # 正規表現を用いて、<>で囲まれた部分とその他の平文を分離する
    pattern = r'(<[^>]*>)'

    # パターンにマッチする部分を探し、リストに分割する
    parts = re.split(pattern, text)

    # 平文とタグで囲まれた部分を別々のリストに格納
    plain_text_parts = []
    tag_parts = []
    deep_case = []
    imis_text = []

    for part in parts:
        if part.startswith('<') and part.endswith('>'):
            tag_parts.append(part.strip())
        elif part.strip():
            plain_text_parts.append(part.strip())

    # tag_partsの要素数分の'none'をdeep_caseに追加する
    # <述語動詞><時間格>などの表層格以外のタグについてはそのまま追加する
    pattern_kanji = r'[\u4E00-\u9FFF]+'
    for tag in tag_parts:
        match_kanji = re.search(pattern_kanji, tag)
        if match_kanji:
            deep_case.append(tag)
        else:
            deep_case.append('none')

    for text in plain_text_parts:
        imis_text.append(use_juman(jumanpp, text))

    keys = ['text', 'surface_case', 'deep_case', 'imis']
    # 辞書型のリストにまとめる
    dict_list = [dict(zip(keys, values))
                 for values in zip(plain_text_parts, tag_parts, deep_case, imis_text)]

    return dict_list
