from pyknp import KNP
import re
from utiles import make_two_dimensional_array, make_hierarchy


def parse_text2bunsetsu(text):
    knp = KNP()     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)

    parsed_result = knp.parse(text)

    # print("----------文節----------")
    pre_bnst_list = []
    bnst_list = []
    parent_id_is_root_list = []
    for bnst in parsed_result.bnst_list():  # 各文節へのアクセス
        print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%d, 素性:%s"
              % (bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id, bnst.fstring))

        # 例：{'id': 0, 'midasi': '総裁に', '係り受けタイプ': 'D', 'parent_id': 1, 'fstring': '~~~'}
        bnst_record = {'id': bnst.bnst_id, 'midasi': "".join(
            mrph.midasi for mrph in bnst.mrph_list()), 'kakariuketype': bnst.dpndtype, 'parent_id': bnst.parent_id, 'fstring': bnst.fstring}
        pre_bnst_list.append(bnst_record)

        if bnst.parent_id == -1:
            parent_id_is_root_list.append(bnst.bnst_id)

    # print(pre_bnst_list)

    # 親の親のIDが-1の時かつ(素性に'<並キ:述'がある、かつ、素性に<用言:動>がある)場合、親IDを強制的に-1にする
    for bnst in pre_bnst_list:
        pattern_yougen = r'<用言:動>'
        match_yougen = re.search(pattern_yougen, bnst['fstring'])
        pattern_heiretsu = r'<並キ:述'
        match_heiretsu = re.search(pattern_heiretsu, bnst['fstring'])
        if bnst['parent_id'] in parent_id_is_root_list and (match_yougen and match_heiretsu):
            bnst_record = {'id': bnst['id'], 'midasi': bnst['midasi'],
                           'kakariuketype': bnst['kakariuketype'], 'parent_id': -1}
        else:
            bnst_record = {'id': bnst['id'], 'midasi': bnst['midasi'],
                           'kakariuketype': bnst['kakariuketype'], 'parent_id': bnst['parent_id']}
        bnst_list.append(bnst_record)
    # print(bnst_list)

    # 係り受けの階層構造を辞書型で定義する
    result, hierarchy = make_hierarchy.build_hierarchy(bnst_list)
    # print(result)
    # print(hierarchy)  # 係り受けの階層構造辞書
    # 係り受けの階層構造辞書をリストに変換
    nested_hierarchy_list = make_hierarchy.hierarchy_to_list(hierarchy)
    hierarchy_list = make_two_dimensional_array.make(nested_hierarchy_list)
    # print(hierarchy_list)

    parsed_bunsetsu_list = []
    for two_dim_list in hierarchy_list:
        parsed_bunsetsu = []
        for item in two_dim_list:
            if isinstance(item, list):
                for elem in item:
                    midasi = bnst_list[elem]['midasi']
                    parsed_bunsetsu.append(midasi)
            else:
                midasi = bnst_list[item]['midasi']
                parsed_bunsetsu.append(midasi)
        # print(parsed_bunsetsu)
        result = ''.join(parsed_bunsetsu)
        # print(result)
        parsed_bunsetsu_list.append(result)
    # print(parsed_bunsetsu_list)

    return parsed_bunsetsu_list
