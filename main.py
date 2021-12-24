import sys

import payments_detail
import parse_json

if __name__ == '__main__':
    if len(sys.argv) < 2:
        message: str = 'При спользовании скрипта укажите пожалуйста следующие позиционные параметры:' \
                       '\n[1] - [test] - номер тестового задания (1 - парсинг json файлов в электронную таблицу, '\
                       '2 - получение платежной информации запросами)' \
                       '\n пример: python main.py 1'
        print(message)
        sys.exit(-1)
    if sys.argv[1] not in ['1', '2']:
        print(f'Указанный тест {sys.argv[1]} не существует')
        sys.exit(-1)

    if sys.argv[1] == '2':
        for i in range(10):
            print(payments_detail.get_payee_details('7840', '40913000'))
    if sys.argv[1] == '1':
        files = ['test1.json', 'test2.json', 'test3.json']
        for file in files:
            parse_json.parse_json(file)
