import json

# nliの形式に対応できるよう、sentence_1とsentence_2の両方に対して処理を行う


def json2deepCasedTxt_for_nli(deep_cased_dicts):
    sentence_pair_dicts = []
    for item in deep_cased_dicts:
        sentence_1 = []
        sentence_2 = []
        # sentence_1に対する処理
        for predicate_term in item['sentence_1']:
            for phrase_dict in predicate_term:
                text = phrase_dict['text']
                deep_case = phrase_dict['deep_case']
                sentence_1.append(text)
                sentence_1.append(deep_case)
        # sentence_2に対する処理
        for predicate_term in item['sentence_2']:
            for phrase_dict in predicate_term:
                text = phrase_dict['text']
                deep_case = phrase_dict['deep_case']
                sentence_2.append(text)
                sentence_2.append(deep_case)
        string_sentence_1 = ''.join(sentence_1)
        string_sentence_2 = ''.join(sentence_2)
        sentence_pair_dict = {'sentence_pair_id': item['sentence_pair_id'], 'sentence_1': string_sentence_1,
                              'sentence_2': string_sentence_2, 'label': item['label']}
        sentence_pair_dicts.append(sentence_pair_dict)
    return sentence_pair_dicts


def json2deepCasedTxt(deep_cased_dicts):
    sentence = []
    # sentenceに対する処理
    for phrase_dict in deep_cased_dicts:
        text = phrase_dict['text']
        deep_case = phrase_dict['deep_case']
        sentence.append(text)
        sentence.append(deep_case)

    string_sentence = ''.join(sentence)
    return string_sentence


def main():
    with open('../../data/deepCased_sentences.json', 'r', encoding='utf-8') as f:
        deep_cased_dicts = json.load(f)

    sentence_pair_dicts = json2deepCasedTxt_for_nli(deep_cased_dicts)

    # JSON形式の文字列に変換
    json_data = json.dumps(sentence_pair_dicts, ensure_ascii=False, indent=4)

    # ファイルに書き出す
    with open('../../data/text_deepCased_sentences.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


if __name__ == "__main__":
    main()
