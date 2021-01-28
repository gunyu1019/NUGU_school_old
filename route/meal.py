import json

from sanic import response

from module.request import requests
from module.check_date import check_date
from module.get_error import get_error, forbidden

from config import parser

def read_food(food):
    food_list = food.split('<br/>')
    answer = ", ".join(food_list)
    for i in range(20, 0, -1):
        answer = answer.replace(f"{i}.", "")
    return answer

base = "https://open.neis.go.kr/hub/"
neis_token = parser.get('TOKEN', 'token')

async def meal(request):
    if request.body == b"":
        return forbidden
    parameters = json.loads(request.body.decode())
    action = parameters.get('action')
    version = parameters.get('version')

    if "parameters" in action or action is None:
        if action['parameters']['KEY']['value'] != "nugu_project_20210128":
            return forbidden
    else:
        return forbidden
    params = action['parameters']

    school_name = params['school_name']['value']
    header1 = {
        'SCHUL_NM': str(school_name),
        'Type': 'json',
        'KEY': f'{neis_token}'
    }
    resp1 = await requests("GET", f"{base}schoolInfo", params=header1)
    if type(resp1.data) == str:
        json1 = json.loads(resp1.data)
    else:
        json1 = resp1.data

    if 'RESULT' in json1.keys():
        if 'CODE' in json1['RESULT'].keys():
            ercode = json1['RESULT']['CODE']
            if ercode == 'INFO-200':
                return response.json(get_error("school_not_found", version), status=200)

    school_info = json1['schoolInfo'][1]["row"]
    sc_code = school_info[0]["ATPT_OFCDC_SC_CODE"]
    sd_code = school_info[0]["SD_SCHUL_CODE"]

    date, date_answer = check_date(params=params['day']['value'])
    if date is None:
        return response.json(get_error("day_not_found", version), status=200)
    header2 = {
        'Type': 'json',
        'KEY': f'{neis_token}',
        'ATPT_OFCDC_SC_CODE': sc_code,
        'SD_SCHUL_CODE': sd_code,
        'MLSV_YMD': date.strftime('%Y%m%d')
    }
    resp2 = await requests("GET", f"{base}mealServiceDietInfo", params=header2)
    if type(resp2.data) == str:
        json2 = json.loads(resp2.data)
    else:
        json2 = resp2.data

    if 'RESULT' in json2.keys():
        if 'CODE' in json2['RESULT'].keys():
            ercode = json2['RESULT']['CODE']
            if ercode == 'INFO-200':
                return response.json(get_error("meal_not_found1", version), status=200)

    food = None
    for i in json2['mealServiceDietInfo'][1]["row"]:
        if i['MMEAL_SC_NM'] == params['meal_type']['value']:
            food = i["DDISH_NM"]
    if food is None:
        return response.json(get_error("meal_not_found2", version), status=200)

    data = {
        "version": version,
        "resultCode": "OK",
        "output": {
            "status": read_food(food),
            "date": date_answer
        }
    }

    return response.json(data)
