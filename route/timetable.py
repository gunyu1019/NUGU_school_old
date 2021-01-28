import json

from sanic import response

from module.request import requests
from module.check_date import check_date
from module.get_error import get_error, forbidden

from config import parser

base = "https://open.neis.go.kr/hub/"
neis_token = parser.get('TOKEN', 'token')
type_list = {"초등학교": "els", "중학교": "mis", "고등학교": "his", "특수학교": "sps"}

async def timetable(request):
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

    school_name = params['timetable_name']['value']
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
    type_nm = school_info[0]['SCHUL_KND_SC_NM']

    date, date_answer = check_date(params=params['timetable_day']['value'])
    if date is None:
        return response.json(get_error("day_not_found", version), status=200)

    header2 = {
        "Type": "json",
        "KEY": neis_token,
        "ATPT_OFCDC_SC_CODE": sc_code,
        "SD_SCHUL_CODE": sd_code,
        "GRADE": params['grade']['value'].replace('학년',''),
        "CLASS_NM": params['class']['value'].replace('반',''),
        "ALL_TI_YMD": date.strftime('%Y%m%d')
    }
    resp2 = await requests("GET", f"{base}{type_list[type_nm]}Timetable", params=header2)
    if type(resp2.data) == str:
        json2 = json.loads(resp2.data)
    else:
        json2 = resp2.data

    if 'RESULT' in json2.keys():
        if 'CODE' in json2['RESULT'].keys():
            ercode = json2['RESULT']['CODE']
            if ercode == 'INFO-200':
                return response.json(get_error("timetable_not_found", version), status=200)

    data = json2[f'{type_list[type_nm]}Timetable'][1]['row']
    data_count = len(data)
    table = ["" for col in range(data_count)]

    for i in data:
        perio = int(i['PERIO'])-1
        table[perio] = i['ITRT_CNTNT']

    answer = ""
    count = 1
    for i in table:
        answer += f", {count}교시 {i}"
        count += 1

    data = {
        "version": version,
        "resultCode": "OK",
        "output": {
            "timetable_status": answer.replace(",","",1),
            "timetable_date": date_answer
        }
    }
    return response.json(data)
