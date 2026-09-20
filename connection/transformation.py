from datetime import datetime


def create_dict(data_list: list, header_list: list):
    big_dict = {}
    for one_meaning in data_list:
        big_dict[int(one_meaning[0])] = {name: val for name, val in zip(header_list[1:], one_meaning[1:])}
        big_dict[int(one_meaning[0])]['count'] = 1

    return big_dict

def data_transform(data: dict):
    transform_dict = {}
    for id_recornt, inner_dict in data.items():
        transform_dict[id_recornt] = {}
        for key, val in inner_dict.items():
            if val == '':
                val = None
                transform_dict[id_recornt][key] = val
                continue
            try:
                val = int(val)
                transform_dict[id_recornt][key] = val
                continue
            except ValueError:
                pass
            try:
                val = float(val)
                transform_dict[id_recornt][key] = val
                continue
            except ValueError:
                pass
            try:
                val = datetime.strptime(val, '%Y-%m-%d')
                transform_dict[id_recornt][key] = val
                continue
            except ValueError:
                try:
                    val = datetime.strptime(val, '%H:%M:%S')
                    transform_dict[id_recornt][key] = val
                    continue
                except ValueError:
                    pass

            val = str(val)
            transform_dict[id_recornt][key] = val

    return transform_dict
