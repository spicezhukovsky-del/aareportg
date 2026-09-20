import pandas as pd

from connection.google_sheet import questions, data_list_chek, school_name
from connection.transformation import create_dict, data_transform
from analyzer.data_analysis import (
    filter_full_schools,
    filter_one_school,
    sum_chek,
    datatime_filter,
    filter_by_coach_in_school,
    sort_rank_school,
)
from test_def.tests import test_cake, test_look
from typewriter.writer import over_coach_block, sh_block

from docx import Document
from docx.shared import Cm, Pt


work_in_dict = create_dict(data_list_chek, questions)
transformed_dict = data_transform(work_in_dict)

# Тут все отфильтровалось по id школы
filterest_all_sh = filter_full_schools(transformed_dict)



def currunt_month(data_dict, data_start, data_end):
    # Тут отфильтрованны все просмотры до дате
    # Эта переменная будет хранить актуальный месяц
    currunt_month = datatime_filter(data_dict, data_start, data_end)

    # Тут мы создаем словарь со данными по каждому тренеру и рейтинг
    coach_data_currunt_month, coach_rank_currunt_month = filter_by_coach_in_school(currunt_month, create_over_rank_coach_sort=True)

    # Тут мы создаем отсортированный рейтинг с общими данными по школе
    sort_currunt_month = sort_rank_school(coach_data_currunt_month)

    return sort_currunt_month, coach_data_currunt_month, coach_rank_currunt_month


def past_month(data_dict, data_start, data_end):
    # Тут отфильтрованны все просмотры до дате
    # Эта переменная будет хранить прошлый месяц
    past_month = datatime_filter(data_dict, data_start, data_end)

    # Тут мы создаем словарь со данными по каждому тренеру и рейтинг
    coach_data_past_month, coach_rank_past_month = filter_by_coach_in_school(past_month, create_over_rank_coach_sort=True)

    # Тут мы создаем отсортированный рейтинг с общими данными по школе
    sort_past_month = sort_rank_school(coach_data_past_month)

    return sort_past_month, coach_data_past_month, coach_rank_past_month


def create_all_sh_raport(name_doc, name_dict: dict, data_dict: dict, data_start: str, data_end_current_month: str, data_end_past_month: str):
    for id, name in name_dict.items():

        rank_all_sh_sort, coach_data_currunt_month, coach_rank_currunt_month = currunt_month(data_dict, data_start, data_end_current_month)
        rank_all_sh_sort_past, coach_data_past_month, coach_rank_past_month = past_month(data_dict, data_start, data_end_past_month)

        try:
            dict_one_sh = rank_all_sh_sort[id]
            coach_one_sh = coach_data_currunt_month[id]
        except KeyError:
            continue

        name_doc = Document()
        section = name_doc.sections[0]
        section.footer_distance = Cm(0.2)

        section.left_margin = Cm(1.5)
        section.right_margin = Cm(1.5)
        section.top_margin = Cm(1)
        section.bottom_margin = Cm(1)

        style = name_doc.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(14)

        try:
            sh_block(name_doc, dict_one_sh, rank_all_sh_sort, name, id, name_dict, rank_all_sh_sort_past)
        except KeyError:
            sh_block(name_doc, dict_one_sh, rank_all_sh_sort, name, id, name_dict)

        over_coach_block(name_doc, coach_one_sh, coach_rank_currunt_month, name)


        name_doc.save(f'ОТЧЕТ_МОНИТОРИНГ {name}.docx')
        print(f'ОТЧЕТ_МОНИТОРИНГ {name}.docx')


create_all_sh_raport("raport_biha", school_name, filterest_all_sh, "2023-09-01", "2024-03-01", "2024-02-01")
