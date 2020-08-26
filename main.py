from monsterboard import check_monsterboard
from careerguide import check_careerguide

kws = ['Data Stewardship', 'Data Steward', 'Datakwaliteit']
for kw in kws:
    check_monsterboard(kw)
    check_careerguide(kw)