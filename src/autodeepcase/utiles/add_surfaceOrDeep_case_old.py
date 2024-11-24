import re


def add_surface_case(tag_list, id):
    if tag_list[id]['surface_case'] == '受動態':
        surface_case = '<'+'受動態'+'>'
    elif tag_list[id]['surface_case'] == '時間':
        surface_case = '<'+'時間格'+'>'
    # elif tag_list[id]['surface_case'] == 'none' and tag_list[id]['is_verb'] == 'verb':
    elif tag_list[id]['is_verb'] == 'verb':
        surface_case = '<'+'述語動詞'+'>'
    elif tag_list[id]['surface_case'] == 'none':
        surface_case = ''
    else:
        surface_case = katakana_to_rome(tag_list[id]['surface_case'])

    return surface_case


def katakana_to_rome(text):
    if text == 'ハ' or text == 'ガ':
        surface_case = '<'+'ga'+'>'
    elif text == 'ヲ':
        surface_case = '<'+'wo'+'>'
    elif text == '二' or text == 'ニ':
        surface_case = '<'+'ni'+'>'
    elif text == 'デ':
        surface_case = '<'+'de'+'>'
    elif text == 'ニテ':
        surface_case = '<'+'de'+'>'
    elif text == 'ト':
        surface_case = '<'+'to'+'>'
    elif text == 'カラ':
        surface_case = '<'+'kara'+'>'
    elif text == 'ヨリ':
        surface_case = '<'+'yori'+'>'
    elif text == 'ヘ':
        surface_case = '<'+'he'+'>'
    elif text == 'マデ':
        surface_case = '<'+'made'+'>'
    # モ格は便宜上ガ格とする
    elif text == 'モ':
        surface_case = '<'+'mo'+'>'
    else:
        surface_case = '<'+'unk'+'>'

    return surface_case


def add_deepCase(dict_data):
    def process_gakaku(data):
        # 'case'が'ガ格'の要素をカウント
        count_gakaku = sum(
            1 for item in data if item['surface_case'] == '<ga>')
        count_nikaku = sum(
            1 for item in data if item['surface_case'] == '<ni>')
        # ガ格が時間的な表現の場合に対応
        pattern_time = r'カテゴリ:時間'
        count_gakaku_time = sum(
            1 for item in data if item['surface_case'] == '<ga>' and re.search(
                pattern_time, item['imis']))

        # ガ格と二格が共存している場合に対応
        if count_gakaku > 0 and count_nikaku > 0:
            # 最初に二格に「カテゴリ:人 」があるかどうかを判定して、以下のガ格二格共存ループに入るかどうかを決める
            bool_match_hito = False
            pattern_hito = r'カテゴリ:人 '
            for item in data:
                if item['surface_case'] == '<ni>':
                    match_hito = re.search(
                        pattern_hito, item['imis'])
                    if match_hito:
                        bool_match_hito = True
                        break

            if bool_match_hito:
                for item in data:
                    match_hito = re.search(
                        pattern_hito, item['imis'])
                    match_time = re.search(
                        pattern_time, item['imis'])
                    # ガ格が時間的な表現の場合に対応
                    if item['surface_case'] == '<ga>' and match_time:
                        item['deep_case'] = '<時間格>'
                    elif item['surface_case'] == '<ga>':
                        item['deep_case'] = '<対象格>'
                    elif item['surface_case'] == '<ni>':
                        item['deep_case'] = '<主格>'

        # ガ格が１つの場合とガ格が二つある場合に対応
        if count_gakaku == 0:
            pass
        elif count_gakaku == 1:
            for item in data:
                match_time = re.search(
                    pattern_time, item['imis'])
                # ガ格が時間的な表現の場合に対応
                if item['surface_case'] == '<ga>' and match_time:
                    item['deep_case'] = '<時間格>'
                elif item['surface_case'] == '<ga>' and item['deep_case'] == 'none':
                    item['deep_case'] = '<主格>'
        elif count_gakaku == 2:
            pattern_hito = r'カテゴリ:人 '
            pattern_animal = r'カテゴリ:動物 '
            pattern_quantity = r'カテゴリ:数量'
            for item in data:
                match_time = re.search(
                    pattern_time, item['imis'])
                match_hito = re.search(
                    pattern_hito, item['imis'])
                match_animal = re.search(
                    pattern_animal, item['imis'])
                match_quantity = re.search(
                    pattern_quantity, item['imis'])

                # ガ格が時間的な表現の場合、通常のルールを適用
                # そうでない場合、ガ格2つあるルールを適用
                if count_gakaku_time > 0:
                    if item['surface_case'] == '<ga>' and match_time:
                        item['deep_case'] = '<時間格>'
                    elif item['surface_case'] == '<ga>':
                        item['deep_case'] = '<主格>'
                else:
                    if item['surface_case'] == '<ga>' and (match_hito or match_animal):
                        item['deep_case'] = '<主格>'
                    elif item['surface_case'] == '<ga>' and match_quantity:
                        item['deep_case'] = '<数量格>'
                    elif item['surface_case'] == '<ga>':
                        item['deep_case'] = '<対象格>'

    def process_wokaku(data):
        for item in data:
            if item['surface_case'] == '<wo>':
                item['deep_case'] = '<対象格>'

    def process_nikaku(data):
        # 'surface_case'がga格,ni格,wo格の要素をカウント
        count_gakaku = sum(
            1 for item in data if item['surface_case'] == '<ga>')
        count_nikaku = sum(
            1 for item in data if item['surface_case'] == '<ni>')
        count_wokaku = sum(
            1 for item in data if item['surface_case'] == '<wo>')

        for item in data:
            if item['surface_case'] == '<ni>':

                # 二格が場所的な表現の場合に対応
                pattern_place1 = r'地名'
                match_place1 = re.search(
                    pattern_place1, item['imis'])
                pattern_place2 = r'場所'
                match_place2 = re.search(
                    pattern_place2, item['imis'])
                pattern_animal_plase = r'動物-部位'
                match_animal_place = re.search(
                    pattern_animal_plase, item['imis'])
                # 二格が時間的な表現の場合に対応
                pattern_time = r'カテゴリ:時間'
                match_time = re.search(
                    pattern_time, item['imis'])
                # 二格が人的な表現の場合に対応
                # 後ろの空白文字も必要
                pattern_hito = r'カテゴリ:人  '
                match_hito = re.search(
                    pattern_hito, item['imis'])

                # 二格が場所的な表現のみを含む場合に対応
                if match_animal_place and not match_hito:
                    item['deep_case'] = '<場所-動物-部位格>'
                # 例：日本を旅行中の外国人に→これは人的な表現として扱いたい
                elif (match_place1 or match_place2) and not match_hito:
                    item['deep_case'] = '<場所格>'
                # 二格が時間的な表現の場合に対応
                elif match_time:
                    item['deep_case'] = '<時間格>'
                # ni格とwo格が共存している場合に対応
                elif count_nikaku > 0 and count_wokaku > 0:
                    if item['surface_case'] == '<ni>':
                        item['deep_case'] = '<受け手格>'
                    elif item['surface_case'] == '<wo>':
                        item['deep_case'] = '<対象格>'
                # 二格が人的な表現の場合に対応
                # ガ格の判定と競合するため
                elif not (match_hito and count_gakaku > 0):
                    item['deep_case'] = '<対象格>'

    def process_dekaku(data):

        pattern_animal_plase = r'動物-部位'
        pattern_place = r'場所'
        pattern_place2 = r'地名'
        pattern_abstract_object = r'カテゴリ:(.*?)抽象物'
        pattern_quantity = r'カテゴリ:数量'

        # 'surface_case'がni格＆素性が動物-部位の要素をカウント
        count_nikaku_animal_place = sum(
            1 for item in data if item['surface_case'] == '<ni>' and re.search(pattern_animal_plase, item['imis']))

        for item in data:
            match_animal_place = re.search(
                pattern_animal_plase, item['imis'])
            match_place = re.search(
                pattern_place, item['imis'])
            match_place2 = re.search(
                pattern_place2, item['imis'])
            match_abstract_object = re.search(
                pattern_abstract_object, item['imis'])
            match_quantity = re.search(
                pattern_quantity, item['imis'])
            if item['surface_case'] == '<de>' and match_animal_place:
                if not count_nikaku_animal_place != 0:
                    item['deep_case'] = '<場所-動物-部位格>'
                else:
                    item['deep_case'] = '<手段・道具格>'
            elif item['surface_case'] == '<de>' and (match_place or match_place2):
                item['deep_case'] = '<場所格>'
            elif item['surface_case'] == '<de>' and match_abstract_object:
                item['deep_case'] = '<場格>'
            elif item['surface_case'] == '<de>' and match_quantity:
                item['deep_case'] = '<数量格>'
            elif item['surface_case'] == '<de>':
                item['deep_case'] = '<手段・道具格>'

    def process_tokaku(data):
        for item in data:
            if item['surface_case'] == '<to>':
                item['deep_case'] = '<相手格>'

    def process_karakaku(data):
        pattern_hito = r'カテゴリ:人 '
        for item in data:
            match_hito = re.search(
                pattern_hito, item['imis'])
            if item['surface_case'] == '<kara>' and match_hito:
                item['deep_case'] = '<主格>'
            elif item['surface_case'] == '<kara>':
                item['deep_case'] = '<起点格>'

    def process_yorikaku(data):
        for item in data:
            if item['surface_case'] == '<yori>':
                item['deep_case'] = '<起点格>'

    def process_hekaku(data):
        for item in data:
            if item['surface_case'] == '<he>':
                item['deep_case'] = '<場所格>'

    def process_madekaku(data):
        for item in data:
            if item['surface_case'] == '<made>':
                item['deep_case'] = '<終状態格>'

    def process_mokaku(data):
        # 'deep_case'が主格の要素をカウント
        count_shukaku = sum(
            1 for item in data if item['deep_case'] == '<主格>')
        if count_shukaku == 0:
            for item in data:
                if item['surface_case'] == '<mo>':
                    item['deep_case'] = '<主格>'

        else:
            for item in data:
                if item['surface_case'] == '<mo>':
                    item['deep_case'] = ''

    def process_unk(data):
        pattern_quantity = r'カテゴリ:数量'
        for item in data:
            match_quantity = re.search(
                pattern_quantity, item['imis'])
            if item['surface_case'] == '<unk>' and match_quantity:
                item['deep_case'] = '<数量格>'
            elif item['surface_case'] == '<unk>':
                item['deep_case'] = ''

    process_gakaku(dict_data)
    process_wokaku(dict_data)
    process_nikaku(dict_data)
    process_dekaku(dict_data)
    process_tokaku(dict_data)
    process_karakaku(dict_data)
    process_yorikaku(dict_data)
    process_hekaku(dict_data)
    process_madekaku(dict_data)
    process_mokaku(dict_data)
    process_unk(dict_data)

    return dict_data
