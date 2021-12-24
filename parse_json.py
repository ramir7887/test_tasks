import os
import json
import pandas as pd
from typing import List, Dict, Union


def parse_json(path: str, out_file: str = 'test_parse_json.xlsx'):
    with open(path, 'rb') as file:
        try:
            json_data: Union[List, Dict] = json.load(file)
        except json.JSONDecodeError:
            print('Ошибка десереализации json')

    headers: List = json_data.get('headers')
    values: List = json_data.get('values')
    headers_with_key: Dict = dict([(h.get('properties').get('QuickInfo'), h.get('properties').get('X')) for h in headers])
    table: Dict = {}

    for name, position_x in headers_with_key.items():
        filter_values: List = filter(lambda x: x.get('properties', {}).get('X') == position_x, values)
        for value in filter_values:
            position_y = value.get('properties', {}).get('Y')
            text = value.get('properties', {}).get('Text')
            if position_y not in table.keys():
                table[position_y] = dict.fromkeys(headers_with_key.keys())
            table[position_y][name] = text
    df = pd.DataFrame(table.values())
    df = df.rename(columns={'Сумма во ВВ': 'Сумма по ВВ'})
    print(path)
    print(df)
    print(f'Запись в {out_file} лист {path}\n')

    if os.path.exists(out_file):
        with pd.ExcelWriter(out_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=path, index=False)
    else:
        with pd.ExcelWriter(out_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=path, index=False)