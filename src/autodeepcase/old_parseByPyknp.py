from pyknp import KNP
import re
import make_two_dimensional_array


def build_hierarchy(data):
    hierarchy = {}

    # 親子関係を構築
    for item in data:
        parent_id = item['parent_id']
        child_id = item['id']

        if parent_id not in hierarchy:
            hierarchy[parent_id] = []
        hierarchy[parent_id].append(child_id)

    # 結果のリストを作成
    result = []
    for parent_id, children_ids in hierarchy.items():
        # 親IDが-1でない場合にのみ追加
        if parent_id != -1:
            # 親の親IDが―1(すなわち親が動詞)だった場合
            if parent_id in hierarchy[-1]:
                result.append({
                    'parent_id': parent_id,
                    'children_id': children_ids,
                    'is_verb': 'verb'
                })
            else:
                result.append({
                    'parent_id': parent_id,
                    'children_id': children_ids,
                    'is_verb': 'no_verb'
                })

    return result, hierarchy


def hierarchy_to_list(hierarchy):
    def collect_group(parent, hierarchy):
        group = []
        if parent in hierarchy:
            for child in hierarchy[parent]:
                if child in hierarchy:
                    group.append(collect_group(child, hierarchy))
                else:
                    group.append(child)
        return [parent] + group

    def regroup_hierarchy(hierarchy):
        result = []
        for top_parent in hierarchy.get(-1, []):
            result.append(collect_group(top_parent, hierarchy))
        return result

    def flatten_nested_list(lst):
        flattened = []
        for item in lst:
            if isinstance(item, list) and len(item) > 0 and isinstance(item[0], int):
                flattened.extend(flatten_nested_list(item))
            else:
                flattened.append(item)
        return flattened

    nested_list = regroup_hierarchy(hierarchy)
    # print(nested_list)
    return nested_list


knp = KNP()     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)
# result = knp.parse("台風5号は、10日(土)午後3時には日本の東にあって、1時間におよそ20キロの速さで北へ進んでいる。南海トラフ地震の臨時情報（巨大地震注意）発表を受け、日本を旅行中の外国人に戸惑いが広がっている。総裁になれば所属する麻生派を離脱する考えも示し、長老や派閥が閣僚・党役員の人事に影響を及ぼす旧来型の自民党政治からの脱却を誓った。")
parsed_result = knp.parse(
    "南海トラフ地震の臨時情報（巨大地震注意）発表を受け、日本を旅行中の外国人に戸惑いが広がっている。")

print("----------文節----------")
for bnst in parsed_result.bnst_list():  # 各文節へのアクセス
    print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%d, 素性:%s"
          % (bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id, bnst.fstring))

print("----------基本句----------")
pre_tag_list = []
tag_list = []
for tag in parsed_result.tag_list():  # 各基本句へのアクセス
    print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親基本句ID:%d, 素性:%s"
          % (tag.tag_id, "".join(mrph.midasi for mrph in tag.mrph_list()), tag.dpndtype, tag.parent_id, tag.fstring))

    pattern_kaisekikaku = r'<解析格:(.*?)>'
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


is_verb_true_list = []
for record in pre_tag_list:
    if record['parent_id'] == -1:
        is_verb_true_list.append(record['id'])


for tag_record in pre_tag_list:  # 並列構造があった場合にparent_idを-1に変換する

    pattern_kakukaiseki = r'<格解析結果:'
    match_kakukaiseki = re.search(pattern_kakukaiseki, tag_record['fstring'])

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
result, hierarchy = build_hierarchy(tag_list)
print(result)
print(hierarchy)  # 係り受けの階層構造辞書

print('----------predicate_clause----------')
# 係り受けの階層構造辞書をリストに変換
nested_hierarchy_list = hierarchy_to_list(hierarchy)
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
