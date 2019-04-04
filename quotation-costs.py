import pandas as pd


def quotation_cost(quotation_range):
    print (quotation_range)
    key = quotation_range['transportadora'] + quotation_range['metodo'] + quotation_range['uf'] + quotation_range['tarifa']
    print (key)





def lambda_handler(event, context):
    # print(event)
    event = [event['queryStringParameters']['Correios']]
    quotation_cost (event[0][0])


lambda_handler({
    'queryStringParameters': {
       'Azul Cargo': [{'cep': '01311300', 'transportadora': 'Azul Cargo', 'metodo': 'Azul Cargo Express', 'tarifa': 'Capital', 'uf': 'SP', 'prazo': '5'}], 'Correios': [{'cep': '01311300', 'transportadora': 'Correios', 'metodo': 'Impresso Econômico', 'tarifa': 'Módico', 'uf': 'SP', 'prazo': '9'}], 'Dialogo Logistica': [], 'GolLog': [{'cep': '01311300', 'transportadora': 'GolLog', 'metodo': 'GolLog DOC', 'tarifa': 'DOC', 'uf': 'NA', 'prazo': '3'}], 'Jadlog': [{'cep': '01311300', 'transportadora': 'Jadlog', 'metodo': 'Jadlog Rodoviario', 'tarifa': 'Capital', 'uf': 'SP', 'prazo': '2'}], 'Loggi': [{'cep': '01311300', 'transportadora': 'Loggi', 'metodo': 'Loggi Standard', 'tarifa': 'SP Zona 1', 'uf': 'SP', 'prazo': '1'}], 'Nowlog': [{'cep': '01311300', 'transportadora': 'Nowlog', 'metodo': 'Nowlog Standard', 'tarifa': 'CAP.01', 'uf': 'SP', 'prazo': '4'}], 'Speedlog': [{'cep': '01311300', 'transportadora': 'Speedlog', 'metodo': 'Speedlog Standard', 'tarifa': 'Capital', 'uf': 'SP', 'prazo': '3'}], 'SPLog': [{'cep': '01311300', 'transportadora': 'SPLog', 'metodo': 'SPLog Standard', 'tarifa': 'SPC', 'uf': 'SP', 'prazo': '15'}], 'Transfolha': [{'cep': '01311300', 'transportadora': 'Transfolha', 'metodo': 'Transfolha Terrestre', 'tarifa': 'GSP 2', 'uf': 'SP', 'prazo': '1'}]
    }
}, '')

