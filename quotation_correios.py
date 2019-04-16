# http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?nCdEmpresa=16050401&sDsSenha=r6J95&sCepOrigem=90220060&sCepDestino=04547000&nVlPeso=1&nCdFormato=1&nVlComprimento=26&nVlAltura=16&nVlLargura=16&sCdMaoPropria=n&nVlValorDeclarado=69.90&sCdAvisoRecebimento=n&nCdServico=04669&nVlDiametro=0&StrRetorno=xml&nIndicaCalculo=3
#https://www.youtube.com/watch?v=FqDenKN5y1s
import json

import requests
import xmltodict


def quotation_correios(quotation):
    url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx"
    nCdEmpresa = '16050401'
    sDsSenha = 'r6J95'
    sCepOrigem = quotation['sCepOrigem']
    sCepDestino = quotation['sCepDestino']
    nVlPeso = quotation['nVlPeso']
    nCdFormato = quotation['nCdFormato']
    nVlComprimento = quotation['nVlComprimento']
    nVlAltura = quotation['nVlAltura']
    nVlLargura = quotation['nVlLargura']
    nVlValorDeclarado = quotation['nVlValorDeclarado']
    # nCdEmpresa = '16050401'
    # sDsSenha = 'r6J95'
    # sCepOrigem = "90220060"
    # sCepDestino = "04547000"
    # nVlPeso = "1",
    # nCdFormato = "1",
    # nVlComprimento = "26",
    # nVlAltura = "16",
    # nVlLargura = "16",
    # nVlValorDeclarado = "69.90",
    # nCdServico = "04669",

    nCdServico = "04669",
    querystring = {"nCdEmpresa": nCdEmpresa, "sDsSenha": sDsSenha, "sCepOrigem": sCepOrigem, "sCepDestino": sCepDestino,
                   "nVlPeso": nVlPeso, "nCdFormato": nCdFormato, "nVlComprimento": nVlComprimento,
                   "nVlAltura": nVlAltura, "nVlLargura": nVlLargura,
                   "sCdMaoPropria": "n", "nVlValorDeclarado": nVlValorDeclarado, "sCdAvisoRecebimento": "n",
                   "nCdServico": nCdServico,
                   "nVlDiametro": "0", "StrRetorno": "xml", "nIndicaCalculo": "3"}
    headers = {'Accept': 'application/json'}
    response = requests.request("GET", url, headers=headers, params=querystring)
    correios_response = response.text
    a = xmltodict.parse(correios_response)
    b = json.dumps(a)
    c = json.loads(b)
    print(c)
    correios_price = float((c['Servicos']['cServico']['ValorSemAdicionais']).replace(",",
                                                                                     "."))  # Verificar para não retornar custo zero quando der merda
    correios_delivery_time = c['Servicos']['cServico']['PrazoEntrega']
    print("Preço PAC: " + str(correios_price) + " - Prazo PAC:  " + correios_delivery_time)

    nCdServico = "04162",
    querystring = {"nCdEmpresa": nCdEmpresa, "sDsSenha": sDsSenha, "sCepOrigem": sCepOrigem, "sCepDestino": sCepDestino,
                   "nVlPeso": nVlPeso, "nCdFormato": nCdFormato, "nVlComprimento": nVlComprimento,
                   "nVlAltura": nVlAltura, "nVlLargura": nVlLargura,
                   "sCdMaoPropria": "n", "nVlValorDeclarado": nVlValorDeclarado, "sCdAvisoRecebimento": "n",
                   "nCdServico": nCdServico,
                   "nVlDiametro": "0", "StrRetorno": "xml", "nIndicaCalculo": "3"}
    headers = {'Accept': 'application/json'}
    response = requests.request("GET", url, headers=headers, params=querystring)
    correios_response = response.text
    a = xmltodict.parse(correios_response)
    b = json.dumps(a)
    c = json.loads(b)
    print(c)
    correios_price = float((c['Servicos']['cServico']['ValorSemAdicionais']).replace(",",
                                                                                     "."))  # Verificar para não retornar custo zero quando der merda
    correios_delivery_time = c['Servicos']['cServico']['PrazoEntrega']
    print("Preço SEDEX: " + str(correios_price) + " - Prazo SEDEX:  " + correios_delivery_time)
    # SEGURO SÓ SE APLICA SE NF/VOLUME FOR MAIOR QUE INDENIZAÇÃO AUTOMATICA DE R$18,50


def lambda_handler(event, context):
    for quotation in event['Records']:
        quotation_correios(json.loads(quotation['body']))


lambda_handler({
    "Records": [
        {
            "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
            "receiptHandle": "MessageReceiptHandle",
            "body": "{\"nCdEmpresa\":\"16050401\",\"sDsSenha\":\"r6J95\",\"sCepOrigem\":\"90220060\",\"sCepDestino\":\"28015420\",\"nVlPeso\":\"2,85\",\"nCdFormato\":\"1\",\"nVlComprimento\":\"20\",\"nVlAltura\":\"30\",\"nVlLargura\":\"38\",\"nVlValorDeclarado\":\"69.90\"}",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1523232000000",
                "SenderId": "123456789012",
                "ApproximateFirstReceiveTimestamp": "1523232000001"
            },
            "messageAttributes": {},
            "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
            "awsRegion": "us-east-1"
        }
    ]
}, "")
