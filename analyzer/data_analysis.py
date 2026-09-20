""" Структура всех данных должна соотвествовать шаблону: {id_школы: {внутренний_id: { ДАННЫЕ } } """

from datetime import datetime


from .math_def import calculate_mean_grade, calculate_sum_dict, percent_complet
from .utils_def import sorter_tuple_in_list, append_list_in_list, shakedown_dict


# Используеться при работе со всеми школами
def filter_full_schools(big_dict):
    sort_in_scools = {id_schools: {} for id_schools in range(1,28)}
    for key, value in big_dict.items():
        id_school = value['id_school']
        sort_in_scools[id_school][key] = value
        # print(sort_in_scools[id_school][key])

    return sort_in_scools

# Используеться при работе с одной школой
def filter_one_school(big_dict, id_school):
    sort_in_scools = {id_school: {}}
    for key in big_dict:
        if big_dict[key]['id_school'] == id_school:
            sort_in_scools[id_school][key] = big_dict[key]

    return sort_in_scools

# Узнать кол-во просмотров вне завсимости от того сколько значений в списке. За исключением dict['ключь'] в этом случае счет идет не верно.
def sum_chek(sum_look_dict):
    sum_dict = {}
    for key in sum_look_dict:
        key_sum = len(sum_look_dict[key].keys())
        sum_dict[key] = key_sum
    return sum_dict


def datatime_filter(filter_dict, data_start, data_end):
    filtered_dict = {}
    data_start = datetime.strptime(data_start,'%Y-%m-%d')
    data_end = datetime.strptime(data_end,'%Y-%m-%d')
    for key in filter_dict:
        for key in filter_dict:
            filtered_dict[key] = {}
            for item in filter_dict[key]:
                try:
                    if data_start <= filter_dict[key][item]['data_training'] <= data_end:
                        filtered_dict[key][item] = filter_dict[key][item]
                except TypeError:
                    print(f"Нет даты в строке с id: {item}")

        return filtered_dict


def filter_by_coach_in_school(filter_dict, create_over_rank_coach_sort = False):
    filtered_dict = {}

    for key in filter_dict:
        filtered_dict[key] = {}

        for item in filter_dict[key]:
            coach_name = filter_dict[key][item]['name_coach']
            list_in_dict = list(filter_dict[key][item].keys())

            questions_sum = list_in_dict[17:-3]
            questions_dict = {"questions":{}}
            for question in questions_sum:
                result_quest = filter_dict[key][item][question]
                questions_dict["questions"][question] = result_quest

            mean_questions = filter_dict[key][item]['Баллы за занятие']
            date_training = filter_dict[key][item]['data_training']
            date_mean_tuple = (date_training, mean_questions)

            count = filter_dict[key][item]['count']

            coach_data = filtered_dict[key].get(coach_name)

            if coach_data is None:
                filtered_dict[key][coach_name] = {
                    "questions": questions_dict["questions"],
                    "general_info": {
                        "mean_questions": mean_questions,
                        "count_sum": count,
                    },
                    "grade": [date_mean_tuple]
                }
            else:
                filtered_dict[key][coach_name]["questions"] = calculate_sum_dict(filtered_dict[key][coach_name]["questions"], questions_dict["questions"])
                filtered_dict[key][coach_name]["general_info"]['count_sum'] += 1
                filtered_dict[key][coach_name]["grade"]


                filtered_dict[key][coach_name]["grade"].append(date_mean_tuple)

                new_grade_list = []
                for item in filtered_dict[key][coach_name]["grade"]:
                    new_grade_list.append(item[1])
                filtered_dict[key][coach_name]["general_info"]['mean_questions'] = calculate_mean_grade(new_grade_list)


    if create_over_rank_coach_sort is True:
        over_rank_coach_sort_dict = {}
        for key in filtered_dict:
            for name, val in filtered_dict[key].items():
                over_rank_coach_sort_dict[name] = filtered_dict[key][name]['general_info']

        over_rank_coach_sort_dict = dict(sorted(over_rank_coach_sort_dict.items(), key=lambda item: item[1]['mean_questions'], reverse=True))
        for name, val in over_rank_coach_sort_dict.items():
            over_rank_coach_sort_dict[name]['position'] = list(over_rank_coach_sort_dict.keys()).index(name) + 1

        return filtered_dict, over_rank_coach_sort_dict

    return filtered_dict


def sort_rank_school(filtered_dict):
    school_dict = {}
    for key in filtered_dict:

        if filtered_dict[key] == {}:
            continue

        school_dict[key] = {
            "general_info": {
                "mean_questions": 0,
                "count_sum": 0,
                'over_look': []
            },
            'questions': {}
        }

        for name in filtered_dict[key]:
            school_dict[key]['general_info']['count_sum'] += filtered_dict[key][name]['general_info']['count_sum']

            school_dict[key]['general_info']['over_look'] = append_list_in_list(school_dict[key]['general_info']['over_look'], filtered_dict[key][name]['grade'])

            school_dict[key]['questions'] = shakedown_dict(school_dict[key]['questions'], filtered_dict[key][name]['questions'])


        new_over_look = []
        for item in school_dict[key]['general_info']['over_look']:
            new_over_look.append(item[1])


        school_dict[key]['general_info']['mean_questions'] = calculate_mean_grade(new_over_look)

        school_dict[key]['general_info']['over_look'] = sorter_tuple_in_list(school_dict[key]["general_info"]['over_look'])


    school_dict = dict(sorted(school_dict.items(), key=lambda item: item[1]['general_info']['mean_questions'], reverse=True))
    for name, val in school_dict.items():
        school_dict[name]['position'] = list(school_dict.keys()).index(name) + 1


    return school_dict
