import json


def search_costs(event):
    global custo_peso
    event['peso'] = 3
    try:
        with open('quotation-costs\costs.json', encoding='utf-8') as f:
            data = json.load(f)
            j = 0
            custos = []
            for i in data:
                j = j+1
                if i['transportadora'].upper() == event['transportadora'].upper() and i['metodo'].upper() == event['metodo'].upper() and i['uf'].upper() == event['uf'].upper() and i['tarifa'].upper() == event['tarifa'].upper() and float(i['peso']) >= float(event['peso']):
                    custos.append(i)
            sort_custos = sorted(custos, key=lambda d: float(d["peso"]))
            custo_peso = sort_custos[0]
    except:
        print(event['transportadora'], "Preço não cadastrado")


def lambda_handler(event, context):
    abragencias = event
    custos_totais = []
    for event in abragencias:
        search_costs(event)
        try:
            custos_totais.append(custo_peso)
        except:
            continue
    print(json.dumps(custos_totais, sort_keys=False, indent=4, ensure_ascii=False))


lambda_handler([
    {
        "transportadora": "Azul Cargo",
        "metodo": "Azul Cargo Express",
        "uf": "SP",
        "cidade": "SAO PAULO",
        "cep_inicial": 1300000,
        "cep_final": 1432050,
        "tarifa": "Interestadual - Capital",
        "prazo": 5
    },
    {
        "transportadora": "Correios",
        "metodo": "Impresso Econômico",
        "uf": "SP",
        "cidade": "-",
        "cep_inicial": 1000000,
        "cep_final": 19999999,
        "tarifa": "Módico",
        "prazo": 9
    },
    {
        "transportadora": "GolLog",
        "metodo": "GolLog DOC",
        "uf": "NA",
        "cidade": "NA",
        "cep_inicial": 1001000,
        "cep_final": 1599999,
        "tarifa": "DOC",
        "prazo": 3
    },
    {
        "transportadora": "Jadlog",
        "metodo": "Jadlog Rodoviario",
        "uf": "SP",
        "cidade": "SAO PAULO",
        "cep_inicial": 1300000,
        "cep_final": 1399999,
        "tarifa": "Capital",
        "prazo": 2
    },
    {
        "transportadora": "Loggi",
        "metodo": "Loggi Standard",
        "uf": "SP",
        "cidade": "São Paulo",
        "cep_inicial": 1311000,
        "cep_final": 1311959,
        "tarifa": "SP Zona 1",
        "prazo": 1
    },
    {
        "transportadora": "Speedlog",
        "metodo": "Speedlog - Standard",
        "uf": "SP",
        "cidade": "SAO PAULO",
        "cep_inicial": 1310000,
        "cep_final": 1314900,
        "tarifa": "Capital",
        "prazo": 3
    },
    {
        "transportadora": "Transfolha",
        "metodo": "Transfolha Terrestre",
        "uf": "SP",
        "cidade": "SAO PAULO",
        "cep_inicial": 1000000,
        "cep_final": 1599969,
        "tarifa": "GSP 2",
        "prazo": 2
    }
], "")
