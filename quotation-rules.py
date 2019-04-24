def quotation_exclude_carrier_method(event):
    event['removed_by_quote_rules'] = "True"


def quotation_increase_price(event):
    event['price'] = event['price'] + 10


def lambda_handler(event, context):
    for events in event:
        rule_number = 0
        events['rule_applied'] = ""
        print("\n")
        for rule in rules:
            rule_number = rule_number + 1
            print(events['transportadora'], rule_number)
            regra_se_aplica = False
            line_number = 0
            rule_apply = 0
            for line in rule['input'].values():
                line_number = line_number + 1
                b = eval(line)
                print(line_number, line, b)
                if b == True:
                    rule_apply = rule_apply + 1
                if rule_apply == len(rule['input']):
                    rule_funciotion_name = rule['output']['out']
                    apply_function = (f'{rule_funciotion_name}(events)')
                    eval(apply_function)
                    events['rule_applied'] = (
                        str(events['rule_applied']) + str(rule_funciotion_name) + " - ")
                    print("Rule Applied")

    print("\n", event)


# rules = [
#     {
#         "i1": '''events['metodo'] in {"Impresso Econômico"}''',
#         "i2": '''events['uf'] in {"RS", "SC"}''',
#     },
#     {
#         "i2": '''events['uf'] in {"SE"}''',
#     },
#     {
#         "i2": '''events['tarifa'] in {"CAP"}''',
#     },
# ]

rules = [
    {
        "input": {
            "i1": '''events['metodo'] in {"Impresso Econômico"}''',
            "i2": '''events['uf'] in {"RS", "SC"}''',
        },
        "output": {
            "out": "quotation_exclude_carrier_method",
        }
    },
    {
        "input": {
            "i1": '''events['uf'] in {"SE"}''',
        },
        "output": {
            "out": "quotation_exclude_carrier_method",
        }
    },
    {
        "input": {
            "i1": '''events['tarifa'] in {"CAP"}''',
        },
        "output": {
            "out": "quotation_increase_price",
        }
    },
    {
        "input": {
            "i1": '''events['metodo'] in {"Transfolha Terrestre"}''',
        },
        "output": {
            "out": "quotation_exclude_carrier_method",
        }
    },
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
