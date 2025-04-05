from pyknp import KNP, Juman
import parseByPyknp
import surfaceCase_to_deepCase
from utiles import utile
import json2deepCasedTxt
from utiles import utile
import json


def make_surface_cased_json(text, knp, jumanpp):
    surface_cased_sentence_dicts = parseByPyknp.parseByknp(text, KNP=knp)

    predicate_clauses = []
    surface_cased_dicts = []

    print('surface_cased_sentence_dicts:', surface_cased_sentence_dicts)
    print('\n')

    for a_predicate_term in surface_cased_sentence_dicts:
        predicate_clauses.append(
            utile.parse_text_to_dict_lists(a_predicate_term, jumanpp=jumanpp))
    predicate_clause_record = {'predicate_clauses': predicate_clauses}
    surface_cased_dicts.append(predicate_clause_record)

    # # JSON形式の文字列に変換
    # json_data = json.dumps(surface_cased_dicts, ensure_ascii=False, indent=4)

    return surface_cased_dicts


def make_deep_cased_json(json_data):
    deep_cased_json_data = []

    deep_cased_json_data = surfaceCase_to_deepCase.surfaceCase_to_deepCase(
        surface_dict_list=json_data)

    return deep_cased_json_data


def main(text: str):

    knp = KNP()     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)
    # 平文をjumanに投入し、意味情報を得る
    jumanpp = Juman()

    # 入力テキストに表層格を付与し、JSON形式に変換
    json_data = make_surface_cased_json(text, knp, jumanpp)
    # print(json_data)

    # print(json_data[0]['predicate_clauses'])
    # exit()
    # 表層格付きjsonに深層格を付与し、json形式で返す
    deep_cased_json_data = make_deep_cased_json(
        json_data[0]['predicate_clauses'])
    # print(deep_cased_json_data)

    # "deep_case"が空白文字またはnoneの場合後ろの要素と結合させる
    deepCased_sentence_dict = []
    for record in deep_cased_json_data:
        # print(record)
        # break
        deepCased_sentence_dict.append(
            surfaceCase_to_deepCase.delete_empty_deep_case(sentence=record))
    # print(deepCased_sentence_dict)

    # 名詞句と深層格を辞書型から文字列に変換
    sentence_dicts = json2deepCasedTxt.json2deepCasedTxt(
        deepCased_sentence_dict[0])
    print(sentence_dicts)


if __name__ == "__main__":
    text = 'その男性はそのギターを弾いていて、そのギターのケースを寄付のために開いた状態にしている'
    main(text)

    # text = '男性はそのギターをギターケースの中に片づけている'
    # main(text)
