import datetime
import decimal
import json
import os

import boto3
from boto3.dynamodb.conditions import Key

from quotation_rules import quotation_rules


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
    try:
        # variaveis de entrada
        cep_final = event['queryStringParameters']['cep_final']
        uf_final = event['queryStringParameters']['uf_final']
        cep_inicial = event['queryStringParameters']['cep_inicial']
        uf_incial = event['queryStringParameters']['uf_incial']
        grupo_venda = event['queryStringParameters']['grupo_venda']
        grupo_sku = event['queryStringParameters']['grupo_sku']
        grupo_cliente = event['queryStringParameters']['grupo_cliente']
        peso_real = event['queryStringParameters']['peso_real']
        comprimento = event['queryStringParameters']['comprimento']
        largura = event['queryStringParameters']['largura']
        altura = event['queryStringParameters']['altura']
        valor_nota_fiscal = event['queryStringParameters']['valor_nota_fiscal']

        # calculo do peso final
        fator_peso = {
            'aereo': 166.7,
            'rodoviario': 300,
            'maritmo': 1000,
        }

        peso_cubado = float(comprimento) * float(largura) * \
            float(altura) * fator_peso['aereo'] / 1000000
        if float(peso_cubado) > float(peso_real):
            peso_final = peso_cubado
        else:
            peso_final = peso_real

        # formatar cep
        cep = str(cep_final).replace("-", "").replace(".", "")

        # buscar transportadoras que atendem o cep
        get_coverage(cep)

        # buscar custos
        global custos_totais
        custos_totais = []
        for event in abrang_tranps:
            get_costs(event, peso_final)
        custos_totais = sorted(custos_totais, key=lambda v: float(v["valor"]))

        # Aplicar regras de cotação
        result = (quotation_rules({
            "queryStringParameters": {
                "tenant_id": "123"},
            "body": (json.dumps(custos_totais, sort_keys=False, indent=4, ensure_ascii=False)),
        }, ""))

        # Imprimir input e resultados
        print(cep, event['peso'])
        print(json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False))

        # Retornar API
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(result, sort_keys=True,  ensure_ascii=False, indent=4, cls=DecimalEncoder),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": str(e),
        }


lambda_handler({
    "queryStringParameters": {
        "cep_final": "90480200",
        "uf_final": "SP",
        "uf_incial": "RS",
        "cep_inicial": "90220-060",
        "grupo_cliente": "padrao",
        "grupo_sku": "padrao",
        "grupo_venda": "curadoria",
        "comprimento": "20.6",
        "largura": "30.3",
        "altura": "30.2",
        "peso_real": "0.8",
        "valor_nota_fiscal": "64.90"
    }
}, "")
