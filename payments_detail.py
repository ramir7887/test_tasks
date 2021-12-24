import requests
import json
from typing import List, Dict


def req_addrno_proc(url:str, data:Dict)-> Dict:
    r: requests.Response = requests.post(url, data=data)
    if r.status_code != requests.codes.ok:
        print(f'Ошибка выполнения запроса. Код ответа: {r.status_code}')
        return None
    try:
        json_data: Dict = r.json()
    except json.JSONDecodeError:
        print('Ошибка десереализации json')
        return None
    return json_data


def get_payee_details(code_ifns: str, code_oktmo: str) -> List:
    out_list_order = [
        'payeeName',
        'payeeInn',
        'payeeKpp',
        'bankName',
        'bankBic',
        'payeeAcc'
    ]
    url: str = 'https://service.nalog.ru/addrno-proc.json'
    form_data: Dict = {
        'c': 'getOktmmf',
        'ifns': code_ifns,
        'okatom': None,
    }
    json_data: Dict = req_addrno_proc(url, form_data)
    if not json_data:
        return []
    oktmo_list: Dict = json_data.get('oktmmfList', dict())
    if code_oktmo not in oktmo_list.keys():
        print(f'Код ОКТМО {code_oktmo} не принадлежит ИФНС с кодом {code_ifns}')
        return []

    form_data = {
        'c': 'next',
        'step': '1',
        'npKind': 'fl',
        'objectAddr': None,
        'objectAddr_zip': None,
        'objectAddr_ifns': None,
        'objectAddr_okatom': None,
        'ifns': code_ifns,
        'oktmmf': code_oktmo,
        'PreventChromeAutocomplete': None,
    }
    json_data = req_addrno_proc(url, form_data)
    if not json_data:
        return []
    payee_details: Dict = json_data.get('payeeDetails', dict())
    out: List = []
    for key in out_list_order:
        out.append(payee_details.get(key, None))
    return out
