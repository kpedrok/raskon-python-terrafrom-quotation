import decimal
import json
import os
from boto3.dynamodb.conditions import Key
import boto3

dynamodb = boto3.resource('dynamodb')

tabela = os.getenv('RULES_TABLE', 'rules')

table = dynamodb.Table(tabela)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def handle_action(action, quotation):
    if action["type"] == "quotation_exclude_carrier_method":
        quotation["deleted"] = True
        return quotation
    elif action["type"] == "quotation_increase_price":
        quotation["price"] = quotation["price"] + float(action["value"])
        return quotation
    elif action["type"] == "quotation_set_price":
        quotation["price"] = float(action["value"])
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
    a = 0
    for quotation in quotations:
        for rule in rules:
            a = a + 1
            print(a, rule)
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


def lambda_handler(event, context):
    # Paginar e ordenar pela propriedade order
    rules = table.query(
        IndexName='tenant-index',
        KeyConditionExpression=Key('tenant_id').eq(event['queryStringParameters']['tenant_id']), ScanIndexForward=True)
    result = handle_rules(
        rules['Items'],
        json.loads(event['body'])
    )
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        },
        "body": json.dumps(result, sort_keys=True,  ensure_ascii=False, indent=4, cls=DecimalEncoder),
    }
