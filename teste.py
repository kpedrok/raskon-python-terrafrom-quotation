def quotation_exclude_carrier_method(event, carrier_method):
    if event['metodo'] == carrier_method:
        event['removed_by_quote_rules'] = "True"


def quotation_exclude_uf(event, uf):
    if event['uf'] == uf:
        event['removed_by_quote_rules'] = "True"


# rules_function_list = {
#     'quotation_exclude_carrier_method': quotation_exclude_carrier_method,
#     'quotation_exclude_uf': quotation_exclude_uf,
# }


def lambda_handler(event, context):
    for events in event:
        for rule in rules:
            for line in rule:
                a = (f'{line}(events,rule[line])')
                eval(a)
                # regra = rules_function_list.get(line)
                # regra(events, rule[line])
    print(event)


rules = [
    {
        "quotation_exclude_carrier_method": 'Dialogo Standard',
        "quotation_exclude_uf": "RS",
    },
    {
        "quotation_exclude_carrier_method": "GolLog DOC",
    }
]


lambda_handler([
    {
        "cep": 90480200,
        "transportadora": "Correios",
        "metodo": "Impresso Econômico",
        "tarifa": "Módico",
        "uf": "RS",
        "prazo": 8,
        "chave": "CorreiosImpresso EconômicoRSMódico",
        "price": 13.2
    },
    {
        "cep": 90480200,
        "transportadora": "Dialogo Logistica",
        "metodo": "Dialogo Standard",
        "tarifa": "CAPITAL",
        "uf": "RS",
        "prazo": 3,
        "chave": "Dialogo LogisticaDialogo StandardRSCAPITAL",
        "price": 4.66
    },
    {
        "cep": 90480200,
        "transportadora": "GolLog",
        "metodo": "GolLog DOC",
        "tarifa": "DOC",
        "uf": "NA",
        "prazo": 2,
        "chave": "GolLogGolLog DOCNADOC",
        "price": 12.98
    },
    {
        "cep": 90480200,
        "transportadora": "Jadlog",
        "metodo": "Jadlog Rodoviario",
        "tarifa": "Capital",
        "uf": "RS",
        "prazo": 2,
        "chave": "JadlogJadlog RodoviarioRSCapital",
        "price": 10.5
    },
    {
        "cep": 90480200,
        "transportadora": "Loggi",
        "metodo": "Loggi Standard",
        "tarifa": "RS Zona 1",
        "uf": "RS",
        "prazo": 3,
        "chave": "LoggiLoggi StandardRSRS Zona 1",
        "price": 14.24
    },
    {
        "cep": 90480200,
        "transportadora": "SPLog",
        "metodo": "SPLog Standard",
        "tarifa": "RS",
        "uf": "RS",
        "prazo": 15,
        "chave": "SPLogSPLog StandardRSRS",
        "price": 11.22
    },
    {
        "cep": 90480200,
        "transportadora": "Transfolha",
        "metodo": "Transfolha Terrestre",
        "tarifa": "CAP",
        "uf": "RS",
        "prazo": 4,
        "chave": "TransfolhaTransfolha TerrestreRSCAP",
        "price": 10.16
    }
], "")
