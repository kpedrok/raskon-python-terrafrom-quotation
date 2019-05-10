import json


def lambda_handler(event, context):
    print(event)
    print(event[0]['transportadora'])
    with open('quotation-costs\costs.json', encoding='utf-8') as f:
        data = json.load(f)
        j = 0
        custos = []
        for i in data:
            j = j+1
            if i['transportadora'].upper() == event[0]['transportadora'].upper() and i['metodo'].upper() == event[0]['metodo'].upper() and i['uf'].upper() == event[0]['uf'].upper() and i['tarifa'].upper() == event[0]['tarifa'].upper() and float(i['peso']) >= float(event[0]['peso']):
                custos.append(i)
        # print(json.dumps(custos, sort_keys=False, indent=4, ensure_ascii=False))
        sort_custos = sorted(custos, key=lambda d: float(d["peso"]))
        # print(json.dumps(sort_custos, sort_keys=False,indent=4, ensure_ascii=False))
        custo_peso = sort_custos[0]
        print(event[0]['peso'], custo_peso)


lambda_handler([
    {
        "transportadora": "Transfolha",
        "metodo": "Transfolha Terrestre",
        "uf": "RS",
        "cidade": "PORTO ALEGRE",
        "cep_inicial": 90091000,
        "cep_final": 90842969,
        "tarifa": "CAP",
        "prazo": 5,
        "peso": 1.49
    }
], "")
