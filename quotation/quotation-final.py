import datetime
import decimal
import json
import os

import boto3
from boto3.dynamodb.conditions import Key

from quotation_rules import quotation_rules

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('raskon-master-rules')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def get_coverage(cep):
    global abrang_tranps
    with open('coverage.json', encoding='utf-8') as f:
        cep = int(cep)
        data = json.load(f)
        j = 0
        abrang_tranps = []
        for i in data:
            j = j+1
            if int(i['cep_inicial']) <= cep <= int(i['cep_final']):
                abrang_tranps.append(i)


def get_costs(event, peso_real):
    event['peso'] = float(peso_real)
    custo_peso = []
    try:
        with open('costs.json', encoding='utf-8') as f:
            data = json.load(f)
            j = 0
            custos = []
            for i in data:
                j = j+1
                if i['transportadora'].upper() == event['transportadora'].upper() and i['metodo'].upper() == event['metodo'].upper() and i['uf'].upper() == event['uf'].upper() and i['tarifa'].upper() == event['tarifa'].upper() and float(i['peso']) >= float(event['peso']):
                    i['prazo'] = event['prazo']
                    custos.append(i)
            sort_custos = sorted(custos, key=lambda d: float(d["peso"]))
            custo_peso = sort_custos[0]
            custos_totais.append(custo_peso)
    except:
        pass


def lambda_handler(event, context):
    cep = event['queryStringParameters']['cep']
    peso_real = event['queryStringParameters']['peso']
    cep = str(cep).replace("-", "").replace(".", "")
    peso_real = str(peso_real).replace("-", "").replace(",", ".")
    get_coverage(cep)
    global custos_totais
    custos_totais = []
    for event in abrang_tranps:
        get_costs(event, peso_real)
    # values = {
    #     "cep": cep,
    # }
    # custos_totais['cep'] = cep
    # custos_totais['peso_real'] = peso_real
    # custos_totais['timestamp'] = datetime.datetime.utcnow()
    custos_totais = sorted(custos_totais, key=lambda v: float(v["valor"]))
    print(cep, event['peso'])
    # print(json.dumps(custos_totais, sort_keys=False, indent=4, ensure_ascii=False))

    result = (quotation_rules({
        "queryStringParameters": {
            "tenant_id": "123"},
        "body": (json.dumps(custos_totais, sort_keys=False, indent=4, ensure_ascii=False)),
    }, ""))

    print(json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False))

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(result, sort_keys=True,  ensure_ascii=False, indent=4, cls=DecimalEncoder),
    }
