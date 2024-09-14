def flatten_at_depth(lst, target_depth, current_depth=0):
    # lst: 対象のリスト
    # target_depth: 平坦化したい深さ
    # current_depth: 現在のリストの深さ（初期値は0）

    if not isinstance(lst, list):
        return lst

    if current_depth == target_depth:
        # target_depthに達したら、その部分を平坦化
        return flatten_list(lst)
    else:
        # target_depthに達するまでは再帰的にリストの要素を探索
        return [flatten_at_depth(item, target_depth, current_depth + 1) for item in lst]


def flatten_list(nested_list):
    # リストを平坦化する補助関数
    result = []
    for element in nested_list:
        if isinstance(element, list):
            result.extend(flatten_list(element))
        else:
            result.append(element)
    return result


def sort_second_dimension_array(nested_list):
    # 二次元目の配列の中身をソートする
    sorted_full_list = []
    for lists in nested_list:
        sorted_list = []
        for item in lists:
            if isinstance(item, list):
                item = sorted(item)
                sorted_list.append(item)
            else:
                sorted_list.append(item)
        sorted_full_list.append(sorted_list)
    return sorted_full_list


def sort_nested_list(nested_list):
    # 二次元配列の中身をソートする
    # 二次元目の配列の代表値(最大最小)をもとにソートする
    sorted_full_list = []
    second_dim_arr_dict = {}
    before_sort_list = []

    for lists in nested_list:
        # ネストを解除し、2階層目の配列はその代表値(最大値)を使用する
        new_list = []
        for item in lists:
            if isinstance(item, list):
                item_max = max(item)
                second_dim_arr_dict[item_max] = item
                new_list.append(item_max)
            else:
                new_list.append(item)
        before_sort_list.append(new_list)

    for array in before_sort_list:
        sorted_array = []
        for item in sorted(array):
            key_to_check = item
            value = second_dim_arr_dict.get(key_to_check)
            if value is not None:
                sorted_array.append(second_dim_arr_dict[item])
            else:
                sorted_array.append(item)
        sorted_full_list.append(sorted_array)

    return sorted_full_list


# 元のリスト
# original_list = [[3, [2, 1, 0]], [1, [6, 5, 4], 7]]
# original_list = [[3, [2, [1, 0]]], [8, [6, [5, 4]], 7]]

def make(original_list):
    # 第1引数: 変換したいリスト, 第2引数: 平坦化したい部分の深さ
    # 深さはリストのトップレベルを0として数えます
    modified_list = flatten_at_depth(original_list, target_depth=2)

    # 二次元目の配列の中身をソートする
    modified_list = sort_second_dimension_array(modified_list)

    # 二次元配列の中身をソートする
    # 二次元目の配列の代表値(最大最小)をもとにソートする
    modified_list = sort_nested_list(modified_list)

    # print(modified_list)

    return modified_list
