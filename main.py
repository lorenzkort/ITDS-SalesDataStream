from monsterboard import check_monsterboard
from careerguide import check_careerguide

# datakwaliteit
kws = ['Data Stewardship', 'Data Steward', 'Datakwaliteit']
for kw in kws:
    check_monsterboard(kw, chat_id='-459671235')
    check_careerguide(kw, chat_id='-459671235')

# customer due diligence
kws = ['CDD' , 'KYC', 'Transactiemonitoring']
for kw in kws:
    check_monsterboard(kw, '-487901102')
    check_careerguide(kw, '-487901102')