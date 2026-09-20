import gspread
from datetime import datetime
from pathlib import Path


CON_DIR = Path(__file__).parent.parent.parent / "connections_file"
GOOGLE_API = CON_DIR / "connecter.json"

gc = gspread.service_account(filename = GOOGLE_API)



sh = gc.open("My db chek train")
work_sheet = sh.get_worksheet(0)
anozer_sheet = sh.get_worksheet(4)
sysy_full_name_sheet = sh.get_worksheet(3)
questions = sh.get_worksheet(0)


data_list_chek = work_sheet.get("A2:AW6815")
anozer_diert_data_frame = anozer_sheet.get("G2:H362")
school_full_name = sysy_full_name_sheet.get("C2:C28")

school_name = {}
for id in range(len(school_full_name)):
    school_name[id+1] = school_full_name[id][0]

questions = questions.get("A1:AW1")[0]


if __name__ == "__main__":
    print('Тут нечего запускать, лучше обратись к другому файлу.')
