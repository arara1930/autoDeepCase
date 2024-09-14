from pyknp import KNP
import re
from utiles import make_two_dimensional_array, make_hierarchy, bunsetsuParser


# result = knp.parse("台風5号は、10日(土)午後3時には日本の東にあって、1時間におよそ20キロの速さで北へ進んでいる。
# 南海トラフ地震の臨時情報（巨大地震注意）発表を受け、日本を旅行中の外国人に戸惑いが広がっている。
# 総裁になれば所属する麻生派を離脱する考えも示し、長老や派閥が閣僚・党役員の人事に影響を及ぼす旧来型の自民党政治からの脱却を誓った。")
# parsed_result = knp.parse(
#     "日本を旅行中の外国人に戸惑いが広がっている。")
text = '台風5号は、10日(土)午後3時には日本の東にあって、1時間におよそ20キロの速さで北へ進んでいる。'

print("----------文節----------")
parsed_text = bunsetsuParser.parse_text2bunsetsu(text)  # 文節ごとにリストで返される
print(parsed_text)


print("----------基本句----------")
# 渡された各文節に対して表層格を埋め込んでいく
knp = KNP()     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)
for bnst in parsed_text:
    parsed_result = knp.parse(bnst)
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
        pattern_judoutai = r'<態:受動>'
        match_judoutai = re.search(pattern_judoutai, tag.fstring)
        if match_kaisekikaku:
            tag_record = {'id': tag.tag_id, 'midasi': "".join(
                mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': match_kaisekikaku.group(1), 'fstring': tag.fstring}
        elif match_kakari:
            tag_record = {'id': tag.tag_id, 'midasi': "".join(
                mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': match_kakari.group(1), 'fstring': tag.fstring}
        elif match_judoutai:
            tag_record = {'id': tag.tag_id, 'midasi': "".join(
                mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': '受動態', 'fstring': tag.fstring}
        else:
            tag_record = {'id': tag.tag_id, 'midasi': "".join(
                mrph.midasi for mrph in tag.mrph_list()), '係り受けタイプ': tag.dpndtype, 'parent_id': tag.parent_id, 'surface_case': 'none', 'fstring': tag.fstring}

        pre_tag_list.append(tag_record)

    for tag_record in pre_tag_list:  # 並列構造があった場合にparent_idを-1に変換する

        pattern_kakukaiseki = r'<格解析結果:'
        match_kakukaiseki = re.search(
            pattern_kakukaiseki, tag_record['fstring'])

        if match_kakukaiseki:
            tag_record_after = {
                'id': tag_record['id'], 'midasi': tag_record['midasi'], 'surface_case': tag_record['surface_case'], 'parent_id': -1, 'is_verb': 'verb'}
            tag_list.append(tag_record_after)
        elif tag_record['parent_id'] == -1:
            tag_record_after = {
                'id': tag_record['id'], 'midasi': tag_record['midasi'], 'surface_case': tag_record['surface_case'], 'parent_id': tag_record['parent_id'], 'is_verb': 'verb'}
            tag_list.append(tag_record_after)
        else:
            tag_record_after = {
                'id': tag_record['id'], 'midasi': tag_record['midasi'], 'surface_case': tag_record['surface_case'], 'parent_id': tag_record['parent_id'], 'is_verb': 'no_verb'}
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

    for predicate_clause_2dim_list in hierarchy_list:
        predicate_clause_with_surface_case = []
        for item in predicate_clause_2dim_list:
            if isinstance(item, list):
                surface_case = '<'+tag_list[item[-1]]['surface_case']+'格'+'>'
                for elem in item:
                    midasi = tag_list[elem]['midasi']
                    predicate_clause_with_surface_case.append(midasi)
                predicate_clause_with_surface_case.append(surface_case)
            else:
                midasi = tag_list[item]['midasi']
                predicate_clause_with_surface_case.append(midasi)
                surface_case = '<'+tag_list[item]['surface_case']+'格'+'>'
                predicate_clause_with_surface_case.append(surface_case)
        print(predicate_clause_with_surface_case)
        result = ''.join(predicate_clause_with_surface_case)
        print(result)
