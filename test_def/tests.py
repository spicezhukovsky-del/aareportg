def test_cake(test_dict, name_data = None):
    for key in test_dict:
        print(f'Первый слой фильтрации: {key}')
        list_val = []
        for value in test_dict[key]:
            list_val.append(value)
        if name_data is None:
            print(f'\tВторой слой фильтрации содержит ({len(list_val)} элементов): {list_val} \n')
        else:
            print(f'\tВторой слой фильтрации содержит: {list_val}')
            for item in test_dict[key][value]:
                print(f'\t\tСодержание второго слоя: {item[name_data]}')

    return f'Тест на слоеный торт ЗАВЕРШОН'

def test_look(test_dict):
    for key, value in test_dict.items():
        print(f'id школы: {key}')
        id_num = 1
        for name, val in value.items():
            print(f'\t{id_num}) {name}:\n\t\tСредний балл за все просмотры: {val['general_info']['mean_questions']}\n\t\tВсего просмотров: {val['general_info']['count_sum']}')
            id_num += 1

    return f'Тест по обьемности данных ЗАВЕРШЕН!!'
