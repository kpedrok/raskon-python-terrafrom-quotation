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
    erro = event
    event = json.loads(event['body'], parse_float=decimal.Decimal)
    try:
        # variaveis de entrada
        cep_final = event['cep_final']
        uf_final = event['uf_final']
        cep_inicial = event['cep_inicial']
        uf_incial = event['uf_incial']
        grupo_venda = event['grupo_venda']
        grupo_sku = event['grupo_sku']
        grupo_cliente = event['grupo_cliente']
        peso_real = event['peso_real']
        comprimento = event['comprimento']
        largura = event['largura']
        altura = event['altura']
        valor_nota_fiscal = event['valor_nota_fiscal']

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
        print(e, erro)
        return {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": str(e),
        }


# lambda_handler({'resource': '/quote', 'path': '/quote', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7', 'cache-control': 'no-cache', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-Country': 'BR', 'content-type': 'application/json', 'Host': 'f1a6f3s2ec.execute-api.us-east-1.amazonaws.com', 'origin': 'chrome-extension://aicmkgpgakddgnaphhhpliifpcfhicfo', 'postman-token': 'fab09b4f-0559-6522-14d4-c2c2f45cba1c', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Via': '2.0 cc6f1d15450acb34cdcc811502bdb02d.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'E2r3WfH33lEArtSMi23k--cPP6Rhm48Nuw6fpgI4r6rUrhHYxzWjFw==', 'X-Amzn-Trace-Id': 'Root=1-5cf55581-62ea5c3cb29f56947433046a', 'X-Forwarded-For': '179.219.72.166, 52.46.43.164', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https', 'x-postman-interceptor-id': '8c263389-2beb-b3d6-9b58-cd55bb44b367'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate, br'], 'Accept-Language': ['pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'], 'cache-control': ['no-cache'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-Country': ['BR'], 'content-type': ['application/json'], 'Host': ['f1a6f3s2ec.execute-api.us-east-1.amazonaws.com'], 'origin': ['chrome-extension://aicmkgpgakddgnaphhhpliifpcfhicfo'], 'postman-token': ['fab09b4f-0559-6522-14d4-c2c2f45cba1c'], 'User-Agent': [
#                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'], 'Via': ['2.0 cc6f1d15450acb34cdcc811502bdb02d.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['E2r3WfH33lEArtSMi23k--cPP6Rhm48Nuw6fpgI4r6rUrhHYxzWjFw=='], 'X-Amzn-Trace-Id': ['Root=1-5cf55581-62ea5c3cb29f56947433046a'], 'X-Forwarded-For': ['179.219.72.166, 52.46.43.164'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https'], 'x-postman-interceptor-id': ['8c263389-2beb-b3d6-9b58-cd55bb44b367']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'j9k0mk', 'resourcePath': '/quote', 'httpMethod': 'POST', 'extendedRequestId': 'atpMQHgkoAMF_lQ=', 'requestTime': '03/Jun/2019:17:14:41 +0000', 'path': '/prod/quote', 'accountId': '301587852292', 'protocol': 'HTTP/1.1', 'stage': 'prod', 'domainPrefix': 'f1a6f3s2ec', 'requestTimeEpoch': 1559582081680, 'requestId': '134531ff-8623-11e9-a31d-d98698306811', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '179.219.72.166', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'user': None}, 'domainName': 'f1a6f3s2ec.execute-api.us-east-1.amazonaws.com', 'apiId': 'f1a6f3s2ec'},
#                'body': '{\n "cep_final": "90480200",\n "uf_final": "SP",\n "uf_incial": "RS",\n "cep_inicial": "90220-060",\n "grupo_cliente": "padrao",\n "grupo_sku": "padrao",\n "grupo_venda": "curadoria",\n "comprimento": "20.6",\n "largura": "30.3",\n "altura": "30.2",\n "peso_real": "0.8",\n "valor_nota_fiscal": "64.90"\n}', 'isBase64Encoded': False}, "")
