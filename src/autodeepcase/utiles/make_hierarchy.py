def build_hierarchy(data):
    #data = {'id':, 'parent_id':}
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