def calculate_mean_grade(grades):
    try:
        return round(sum(grades) / len(grades),2)
    except ZeroDivisionError:
        return 0

def calculate_sum_dict(dict_1, dict_2):
    sum_dict = {}
    for key in dict_1:
        if dict_1[key] is None and dict_2[key] is None:
            sum_dict[key] = None
            continue
        elif dict_1[key] is None or dict_2[key] is None:
            if dict_1[key] is None:
                sum_dict[key] = dict_2[key]
            else:
                sum_dict[key] = dict_1[key]
        else:
            sum_dict[key] = dict_1[key] + dict_2[key]

    return sum_dict


def percent_complet(over_num, questions_dict):
    new_dict = {}
    for key, value in questions_dict.items():
        if value is None:
            continue
        else:
            new_dict[key] = round((value / over_num) * 100, 1)

    new_dict = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse=False))

    return new_dict
