def sorter_tuple_in_list(tuples_list):
    return sorted(tuples_list, key=lambda x: x[0])

def append_list_in_list(list_in, list_work):
    for item in list_work:
        list_in.append(item)
    return list_in


def shakedown_dict(shake_dict, to_dict):

    for key, value in to_dict.items():
        check_dict = shake_dict.get(key)
        if check_dict is None or value is None:
            shake_dict[key] = value
        else:
            shake_dict[key] += value

    return shake_dict
