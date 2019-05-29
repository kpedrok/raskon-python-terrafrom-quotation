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


def handle_action(action, quotation):
    if action["type"] == "quotation_exclude_carrier_method":
        quotation["deleted"] = True
        return quotation
    elif action["type"] == "quotation_increase_price":
        quotation["price"] = quotation["price"] + action["value"]
        return quotation
    else:
        raise Exception("Invalid action " + action["type"])

def handle_condition(condition, quotation):
    if condition["operation"] == "IN":
        return quotation[condition["property"]] in condition["values"]
    elif condition["operation"] == ">":
        # Convert to number
        return quotation[condition["property"]] > condition["values"][0]
    else:
        raise Exception("Invalid condition " + condition["operation"])

def handle_conditions(conditions, quotation):
    result = True
    for condition in conditions:
        result = result and handle_condition(condition, quotation)
    return result

def handle_rules(rules, quotations):
    for quotation in quotations:
        for rule in rules:
            if handle_conditions(rule['conditions'], quotation):
                quotation = handle_action(rule['action'], quotation)
    result = []
    for quotation in quotations:
        try:
            if quotation['deleted'] == False:
                result.append(quotation)
        except:
            result.append(quotation)
    return result

rules_new = [
    {
        "id":"",
        "cnpj":"",
        "order": 1,
        "conditions": [
            {
                "property": "metodo",
                "operation": "IN",
                "values": ["Impresso Econômico"]
            },
            {
                "property": "uf",
                "operation": "IN",
                "values": ["RS"]
            }
        ],
        "action": {
            "type": "quotation_exclude_carrier_method"
        }
    },
        {
        "conditions": [
            {
                "property": "uf",
                "operation": "IN",
                "values": ["RS", "SC"]
            }
        ],
        "action": {
            "type": "quotation_increase_price",
            "value": 5
        }
    },
]

# print(handle_action(rules_new[0]['action'],{}))
# print(handle_condition(rules_new[0]['conditions'][0], { "metodo": "Impresso Econômico" }))
# print(handle_condition(rules_new[0]['conditions'][0], { "metodo": "Correios" }))
# print(handle_condition(rules_new[0]['conditions'][1], { "uf": "RS" }))
# print(handle_conditions(rules_new[0]['conditions'], { "metodo": "Impresso Econômico", "uf": "RS" }))
# print(handle_action(rules_new[1]['action'],{ "price": 10 }))

result = handle_rules(
        rules_new,
    [{
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
    ])
for res in result:
    print(res)

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
