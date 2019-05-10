import json


def lambda_handler(event, context):
    cep = "01311300"
    with open('quotation-coverage\coverage.json', encoding='utf-8') as f:
        cep = int(cep)
        data = json.load(f)
        j = 0
        abrang_tranps = []
        for i in data:
            j = j+1
            if int(i['cep_inicial']) <= cep <= int(i['cep_final']):
                abrang_tranps.append(i)
        print(json.dumps(abrang_tranps, sort_keys=False,
                         indent=4, ensure_ascii=False))


lambda_handler("", "")
