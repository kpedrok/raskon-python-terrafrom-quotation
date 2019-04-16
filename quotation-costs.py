import pandas as pd

full_quotation = []


def quotation_cost(quotation_range):
    # print(quotation_range)
    key = quotation_range['transportadora'] + quotation_range['metodo'] + \
        quotation_range['uf'] + quotation_range['tarifa']
    # print(key)
    peso = 2
    df = pd.read_excel('consolidado.xlsx', sheet_name='costs')
    df2 = df.set_index("Chave", drop=False)
    price = df2.loc[key, peso]
    # print(price)

    quotation_range['price'] = price
    print(quotation_range)
    full_quotation.append(quotation_range)


def lambda_handler(event, context):
    event = event['queryStringParameters']
    for events in event:
        # print(events)
        if event[events] != []:
            # print(event)
            quotation_cost(event[events][0])
        else:
            pass
    print(full_quotation)

    minPricedItem = min(full_quotation, key=lambda x: x['price'])
    print("Menor preço:")
    print(minPricedItem)
    mindDeliveryItem = min(full_quotation, key=lambda x: x['prazo'])
    print("Mais rápido:")
    print(mindDeliveryItem)


lambda_handler({
    'queryStringParameters': {'Azul Cargo': [], 'Correios': [{'cep': 90480200, 'transportadora': 'Correios', 'metodo': 'Impresso Econômico', 'tarifa': 'Módico', 'uf': 'RS', 'prazo': 8, 'chave': 'CorreiosImpresso EconômicoRSMódico'}], 'Dialogo Logistica': [{'cep': 90480200, 'transportadora': 'Dialogo Logistica', 'metodo': 'Dialogo Standard', 'tarifa': 'CAPITAL', 'uf': 'RS', 'prazo': 3, 'chave': 'Dialogo LogisticaDialogo StandardRSCAPITAL'}], 'GolLog': [{'cep': 90480200, 'transportadora': 'GolLog', 'metodo': 'GolLog DOC', 'tarifa': 'DOC', 'uf': 'NA', 'prazo': 2, 'chave': 'GolLogGolLog DOCNADOC'}], 'Jadlog': [{'cep': 90480200, 'transportadora': 'Jadlog', 'metodo': 'Jadlog Rodoviario', 'tarifa': 'Capital', 'uf': 'RS', 'prazo': 2, 'chave': 'JadlogJadlog RodoviarioRSCapital'}], 'Loggi': [{'cep': 90480200, 'transportadora': 'Loggi', 'metodo': 'Loggi Standard', 'tarifa': 'RS Zona 1', 'uf': 'RS', 'prazo': 3, 'chave': 'LoggiLoggi StandardRSRS Zona 1'}], 'Nowlog': [], 'Speedlog': [], 'SPLog': [{'cep': 90480200, 'transportadora': 'SPLog', 'metodo': 'SPLog Standard', 'tarifa': 'RS', 'uf': 'RS', 'prazo': 15, 'chave': 'SPLogSPLog StandardRSRS'}], 'Transfolha':
                              [{'cep': 90480200, 'transportadora': 'Transfolha', 'metodo': 'Transfolha Terrestre', 'tarifa': 'CAP', 'uf': 'RS', 'prazo': 4, 'chave': 'TransfolhaTransfolha TerrestreRSCAP'}]}}, '')
