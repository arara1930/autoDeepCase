import json
import csv
import re
from pyknp import KNP, Juman
from utiles import make_two_dimensional_array, make_hierarchy, bunsetsuParser, utile, add_surfaceOrDeep_case


# def parseByknp(text):
#     print("----------文節----------")
#     parsed_text = bunsetsuParser.parse_text2bunsetsu(text)  # 文節ごとにリストで返される
#     print(parsed_text)

#     print("----------基本句----------")
#     # 渡された各文節に対して表層格を埋め込んでいく
#     knp = KNP()     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)
#     surface_cased_sentence_dicts = []
#     for bnst in parsed_text:
#         parsed_result = knp.parse(bnst)
#         pre_tag_list = []
#         tag_list = []
#         for tag in parsed_result.tag_list():  # 各基本句へのアクセス
#             print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親基本句ID:%d, 素性:%s"
#                   % (tag.tag_id, "".join(mrph.midasi for mrph in tag.mrph_list()), tag.dpndtype, tag.parent_id, tag.fstring))

#             # pattern_kaisekikaku = r'<解析格:(.*?)>'
#             pattern_kaisekikaku = r'<解析格:([^ァ-ヶー]+)>'
#             match_kaisekikaku = re.search(pattern_kaisekikaku, tag.fstring)
#             pattern_kakari = r'<係:([ァ-ヶー]+)格>'
#             match_kakari = re.search(pattern_kakari, tag.fstring)
#             pattern_joshi_1 = r'<([ァ-ヶー]+)><助詞>'
#             match_joshi_1 = re.search(pattern_joshi_1, tag.fstring)
#             # pattern_joshi_2 = r'<([^<>]+)><助詞>'
#             pattern_joshi_2 = r'([ァ-ヶー]+)[^ァ-ン]*<助詞>'
#             match_joshi_2 = re.search(pattern_joshi_2, tag.fstring)
#             pattern_judoutai = r'<態:受動>'
#             match_judoutai = re.search(pattern_judoutai, tag.fstring)
#             if match_kaisekikaku:
#                 tag_record = {'id': tag.tag_id, 'midasi': "".join(
#                     mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': match_kaisekikaku.group(1), 'fstring': tag.fstring}
#             elif match_kakari:
#                 tag_record = {'id': tag.tag_id, 'midasi': "".join(
#                     mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': match_kakari.group(1), 'fstring': tag.fstring}
#             elif match_joshi_1:
#                 tag_record = {'id': tag.tag_id, 'midasi': "".join(
#                     mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': match_joshi_1.group(1), 'fstring': tag.fstring}
#             elif match_joshi_2:
#                 tag_record = {'id': tag.tag_id, 'midasi': "".join(
#                     mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': match_joshi_2.group(1), 'fstring': tag.fstring}
#             elif match_judoutai:
#                 tag_record = {'id': tag.tag_id, 'midasi': "".join(
#                     mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': '受動態', 'fstring': tag.fstring}
#             else:
#                 tag_record = {'id': tag.tag_id, 'midasi': "".join(
#                     mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': 'none', 'fstring': tag.fstring}

#             pre_tag_list.append(tag_record)

#         for tag_record in pre_tag_list:  # 並列構造があった場合にparent_idを-1に変換する

#             if tag_record['parent_id'] == -1:
#                 tag_record_after = {
#                     'id': tag_record['id'], 'midasi': tag_record['midasi'], 'surface_case': tag_record['surface_case'], 'parent_id': tag_record['parent_id'], 'is_verb': 'verb'}
#                 tag_list.append(tag_record_after)
#             else:
#                 tag_record_after = {
#                     'id': tag_record['id'], 'midasi': tag_record['midasi'], 'surface_case': tag_record['surface_case'], 'parent_id': tag_record['parent_id'], 'is_verb': 'no_verb'}
#                 tag_list.append(tag_record_after)

#         print('----------tag_list----------')
#         print(tag_list)

#         print('----------result----------')
#         # 係り受けの階層構造を辞書型で定義する
#         result, hierarchy = make_hierarchy.build_hierarchy(tag_list)
#         print(result)
#         print(hierarchy)  # 係り受けの階層構造辞書

#         print('----------predicate_clause----------')
#         # 係り受けの階層構造辞書をリストに変換
#         nested_hierarchy_list = make_hierarchy.hierarchy_to_list(hierarchy)
#         hierarchy_list = make_two_dimensional_array.make(nested_hierarchy_list)
#         print(hierarchy_list)

#         print('----------surface_cased_sentence_record----------')

#         for predicate_clause_2dim_list in hierarchy_list:
#             surface_cased_sentence_record = []
#             surface_cased_sentence_dict = []
#             for item in predicate_clause_2dim_list:
#                 if isinstance(item, list):
#                     # surface_case = '<'+tag_list[item[-1]]['surface_case']+'格'+'>'
#                     surface_case = add_surfaceOrDeep_case.add_surface_case(
#                         tag_list, item[-1])
#                     for elem in item:
#                         midasi = tag_list[elem]['midasi']
#                         surface_cased_sentence_record.append(midasi)
#                     surface_cased_sentence_record.append(surface_case)
#                 else:
#                     midasi = tag_list[item]['midasi']
#                     surface_cased_sentence_record.append(midasi)
#                     # surface_case = '<'+tag_list[item]['surface_case']+'格'+'>'
#                     surface_case = add_surfaceOrDeep_case.add_surface_case(
#                         tag_list, item)
#                     surface_cased_sentence_record.append(surface_case)
#             print(surface_cased_sentence_record)
#             result = ''.join(surface_cased_sentence_record)
#             surface_cased_sentence_dict.append(result)
#             surface_cased_sentence_dicts.append(surface_cased_sentence_dict)
#             print(surface_cased_sentence_dicts)

#     return surface_cased_sentence_dicts

def parseByknp(text, KNP):
    print("----------文節----------")
    parsed_text = bunsetsuParser.parse_text2bunsetsu(text)  # 文節ごとにリストで返される
    print(parsed_text)

    print("----------基本句----------")
    # 渡された各文節に対して表層格を埋め込んでいく

    surface_cased_sentence_dicts = []
    for bnst in parsed_text:
        parsed_result = KNP.parse(bnst)
        pre_tag_list = []
        tag_list = []
        for tag in parsed_result.tag_list():  # 各基本句へのアクセス
            print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親基本句ID:%d, 素性:%s"
                  % (tag.tag_id, "".join(mrph.midasi for mrph in tag.mrph_list()), tag.dpndtype, tag.parent_id, tag.fstring))

            # pattern_kaisekikaku = r'<解析格:(.*?)>'
            pattern_kaisekikaku = r'<解析格:([^ァ-ヶー]+)>'
            match_kaisekikaku = re.search(pattern_kaisekikaku, tag.fstring)
            pattern_kakari = r'<係:([ァ-ヶー]+)格>'
            match_kakari = re.search(pattern_kakari, tag.fstring)
            pattern_joshi_1 = r'<([ァ-ヶー]+)><助詞>'
            match_joshi_1 = re.search(pattern_joshi_1, tag.fstring)
            # pattern_joshi_2 = r'<([^<>]+)><助詞>'
            pattern_joshi_2 = r'([ァ-ヶー]+)[^ァ-ン]*<助詞>'
            match_joshi_2 = re.search(pattern_joshi_2, tag.fstring)
            pattern_judoutai = r'<態:受動>'
            match_judoutai = re.search(pattern_judoutai, tag.fstring)
            if match_kaisekikaku:
                tag_record = {'id': tag.tag_id, 'midasi': "".join(
                    mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': match_kaisekikaku.group(1), 'fstring': tag.fstring}
            elif match_kakari:
                tag_record = {'id': tag.tag_id, 'midasi': "".join(
                    mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': match_kakari.group(1), 'fstring': tag.fstring}
            elif match_joshi_1:
                tag_record = {'id': tag.tag_id, 'midasi': "".join(
                    mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': match_joshi_1.group(1), 'fstring': tag.fstring}
            elif match_joshi_2:
                tag_record = {'id': tag.tag_id, 'midasi': "".join(
                    mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': match_joshi_2.group(1), 'fstring': tag.fstring}
            elif match_judoutai:
                tag_record = {'id': tag.tag_id, 'midasi': "".join(
                    mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': '受動態', 'fstring': tag.fstring}
            else:
                tag_record = {'id': tag.tag_id, 'midasi': "".join(
                    mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': 'none', 'fstring': tag.fstring}

            pre_tag_list.append(tag_record)

        for tag_record in pre_tag_list:  # 並列構造があった場合にparent_idを-1に変換する

            if tag_record['parent_id'] == -1:
                tag_record_after = {
                    'id': tag_record['id'], 'midasi': tag_record['midasi'], 'surface_case': tag_record['surface_case'], 'parent_id': tag_record['parent_id'], 'is_verb': 'verb', 'fstring': tag_record['fstring']}
                tag_list.append(tag_record_after)
            else:
                tag_record_after = {
                    'id': tag_record['id'], 'midasi': tag_record['midasi'], 'surface_case': tag_record['surface_case'], 'parent_id': tag_record['parent_id'], 'is_verb': 'no_verb', 'fstring': tag_record['fstring']}
                tag_list.append(tag_record_after)

        print('----------tag_list----------')
        print(tag_list)

        print('----------result----------')
        # 係り受けの階層構造を辞書型で定義する
        result, hierarchy = make_hierarchy.build_hierarchy(tag_list)
        print(result)
        print(hierarchy)  # 係り受けの階層構造辞書

        print('----------predicate_clause----------')
        # 係り受けの階層構造辞書をリストに変換
        nested_hierarchy_list = make_hierarchy.hierarchy_to_list(hierarchy)
        hierarchy_list = make_two_dimensional_array.make(nested_hierarchy_list)
        print(hierarchy_list)

        print('----------predicate_clause_with_surface_case----------')

        # {’phrase’: ,’surfaceCase’: ,’imisByJuman’: ,’imisByKnp’: ,’symple_phrase’: True or False}
        # ’symple_phrase’: Falseは述語に直接係らない名詞が’phrase’に含まれる事を表す
        # ’imisByJuman’の追加はmain()内で行う
        for predicate_clause_2dim_list in hierarchy_list:
            surface_cased_sentence_record = []
            surface_cased_sentence_dict = []
            for item in predicate_clause_2dim_list:
                # 述語に直接係らない名詞をスタック
                no_surfaceCase_phrases = []
                imisByKnp_list = []
                if isinstance(item, list):
                    surface_case = add_surfaceOrDeep_case.add_surface_case(
                        tag_list, item[-1])
                    for elem in item:
                        midasi = tag_list[elem]['midasi']
                        no_surfaceCase_phrases.append(midasi)
                        imisByKnp = f'fstring:,{tag_list[elem]['fstring']}'
                        imisByKnp_list.append(imisByKnp)
                        imisByKnp = ''.join(imisByKnp_list)
                    no_surfaceCase_phrases = ''.join(no_surfaceCase_phrases)
                    surface_cased_sentence_record = {
                        'phrase': no_surfaceCase_phrases, 'surfaceCase': surface_case, 'imisByKnp': imisByKnp, 'symple_phrase': False}
                    surface_cased_sentence_dict.append(
                        surface_cased_sentence_record)
                else:
                    surface_case = add_surfaceOrDeep_case.add_surface_case(
                        tag_list, item)
                    midasi = tag_list[item]['midasi']
                    imisByKnp = f'fstring:,{tag_list[item]['fstring']}'
                    imisByKnp_list.append(imisByKnp)
                    imisByKnp = ''.join(imisByKnp_list)
                    surface_cased_sentence_record = {
                        'phrase': midasi, 'surfaceCase': surface_case, 'imisByKnp': imisByKnp, 'symple_phrase': True}
                    surface_cased_sentence_dict.append(
                        surface_cased_sentence_record)

        surface_cased_sentence_dicts.append(surface_cased_sentence_dict)
        # print(surface_cased_sentence_dicts)
        print('\n')

    surfaceCased_phrases_for_print_list = []
    for surface_cased_sentence_dict in surface_cased_sentence_dicts:
        for surface_cased_sentence in surface_cased_sentence_dict:
            surfaceCased_phrases_for_print_list.append(
                surface_cased_sentence['phrase'])
            surfaceCased_phrases_for_print_list.append(
                surface_cased_sentence['surfaceCase'])
    surfaceCased_phrases_for_print = ''.join(
        surfaceCased_phrases_for_print_list)
    print(surfaceCased_phrases_for_print)
    print('\n')

    return surface_cased_sentence_dicts


def main():
    # text = '南海トラフ地震の臨時情報（巨大地震注意）発表を受け、日本を旅行中の外国人に戸惑いが広がっている。'
    # text = '総裁になれば所属する麻生派を離脱する考えも示し、長老や派閥が閣僚・党役員の人事に影響を及ぼす旧来型の自民党政治からの脱却を誓った。'
    # text = '日本銀行は19日・20日に行われた金融政策決定会合で、政策金利を現在の0.25％に据え置くことを全会一致で決めました。'
    # text = '台風5号は、10日(土)午後3時には日本の東にあって、1時間におよそ20キロの速さで北へ進んでいる。'
    text = '消火栓が道端に設置がされています。'
    text = 'テディベアを座らせて置いてあります。'
    text = 'テニスラケットとシューズの間に、ボールがあります。'
    # text = 'クルーザーの浮かぶ湖で、サギが海岸に止まっています。'

    knp = KNP()     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)
    surface_cased_sentence_dicts = parseByknp(text, KNP=knp)

    predicate_clauses = []
    surface_cased_dicts = []

    print('surface_cased_sentence_dicts:', surface_cased_sentence_dicts)
    print('\n')

    # 平文をjumanに投入し、意味情報を得る
    jumanpp = Juman()

    for a_predicate_term in surface_cased_sentence_dicts:
        predicate_clauses.append(
            utile.parse_text_to_dict_lists(a_predicate_term, jumanpp=jumanpp))
    predicate_clause_record = {'predicate_clauses': predicate_clauses}
    surface_cased_dicts.append(predicate_clause_record)

    # JSON形式の文字列に変換
    json_data = json.dumps(surface_cased_dicts, ensure_ascii=False, indent=4)

    # ファイルに書き出す
    with open('../../../data/debug/surfaceCased_sentences.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


# def main():
#     text = '南海トラフ地震の臨時情報（巨大地震注意）発表を受け、日本を旅行中の外国人に戸惑いが広がっている。'
#     # text = '総裁になれば所属する麻生派を離脱する考えも示し、長老や派閥が閣僚・党役員の人事に影響を及ぼす旧来型の自民党政治からの脱却を誓った。'
#     # text = '日本銀行は19日・20日に行われた金融政策決定会合で、政策金利を現在の0.25％に据え置くことを全会一致で決めました。'
#     # text = '台風5号は、10日(土)午後3時には日本の東にあって、1時間におよそ20キロの速さで北へ進んでいる。'
#     # text = '私には度胸がありません。'
#     # text = '東日本大震災から13年が経った'
#     # text = '私は彼より背が高い'
#     # text = '象は鼻が長い'
#     # text = '読書が彼は好きだ'
#     # text = '子供が学校へ行く'
#     # text = '江戸から大阪まで歩く'
#     # text = '田んぼに柵を作る'
#     # text = '猫が伸びをする'
#     # text = '消火栓が道端に設置がされています。'
#     surface_cased_sentence_dicts = parseByknp(text)
#     predicate_clauses = []
#     surface_cased_dicts = []

#     print('surface_cased_sentence_dicts:', surface_cased_sentence_dicts)

#     # 平文をjumanに投入し、意味情報を得る
#     jumanpp = Juman()

#     for sentence in surface_cased_sentence_dicts:
#         predicate_clauses.append(
#             utile.parse_text_to_dict_lists(sentence[0], jumanpp=jumanpp))
#     predicate_clause_record = {'predicate_clauses': predicate_clauses}
#     surface_cased_dicts.append(predicate_clause_record)

#     # JSON形式の文字列に変換
#     json_data = json.dumps(surface_cased_dicts, ensure_ascii=False, indent=4)

#     # ファイルに書き出す
#     with open('../../../data/debug/surfaceCased_sentences.json', 'w', encoding='utf-8') as f:
#         f.write(json_data)


if __name__ == "__main__":
    main()
