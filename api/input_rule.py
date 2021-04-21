import decimal
import json
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
tabela = os.getenv('RULES_TABLE', 'raskon-dev-rules')
table = dynamodb.Table(tabela)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def create_rule(rules):
    global create_rule_ids
    create_rule_ids = []
    for rule in rules:
        id = (str(rule['tenant_id'])+str(rule['order']))
        tenant_id = rule['tenant_id']
        order = rule['order']
        description = rule['description']
        action = rule['action']
        conditions = rule['conditions']

        print("Adding rule:", id, tenant_id, order,
              description, action, conditions)

        table.put_item(
            Item={
                'id': id,
                'tenant_id': tenant_id,
                'order': order,
                'description': description,
                'action': action,
                'conditions': conditions,
            }
        )
        create_rule_ids.append(id)


def read_rule(rules):
    global read_rules_ids
    read_rules_ids = []
    for rule in rules:
        try:
            response = table.get_item(
                Key={
                    'id': rule['id'],
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response['Item']
            read_rules_ids.append(response['Item'])


def update_rule(rules):
    global update_rule_ids
    update_rule_ids = []
    # json_file = str(input_rule)
    # rules = json.loads(json_file, parse_float=decimal.Decimal)
    # rules = rules['payload']
    # for rule in rules:
    #     print(rule)
    #     response = table.update_item(
    #         Key={
    #             'id': rule['id'],
    #         },
    #         UpdateExpression="set tenant_id = :tenant_id, description = :description, conditions = :conditions, rule_action = :rule_action, rule_order= :rule_order",
    #         ExpressionAttributeValues={
    #             # ':tenant_id': rule['tenant_id'],
    #             # ':rule_action': rule['action'],
    #             # ':description': rule['description'],
    #             # ':conditions': rule['conditions'],
    #             # ':rule_order': rule['order'],
    #             ':tenant_id': "rule['tenant_id']",
    #             ':rule_action': "rule['action']",
    #             ':description': "rule['description']",
    #             ':conditions': "rule['conditions']",
    #             ':rule_order': "rule['order']",
    #         },
    #         # ExpressionAttributeNames={
    #         #     "rule_action": "action"
    #         # },
    #         ReturnValues="UPDATED_NEW")
    #     print("UpdateItem succeeded:", rule['id'])
    #     # print(json.dumps(response, indent=4, cls=DecimalEncoder))
    for rule in rules:
        response = table.delete_item(
            Key={
                'id': rule['id'],
            },
        )

        id = (str(rule['tenant_id'])+str(rule['order']))
        tenant_id = rule['tenant_id']
        order = rule['order']
        description = rule['description']
        action = rule['action']
        conditions = rule['conditions']
        # id = rule['id']
        # tenant_id = "rule['tenant_id']"
        # order = "rule['order']"
        # description = "rule['description']"
        # action =" rule['action']"
        # conditions = "rule['conditions']"

        print("Update rule:", id, tenant_id, order,
              description, action, conditions)

        table.put_item(
            Item={
                'id': id,
                'tenant_id': tenant_id,
                'order': order,
                'description': description,
                'action': action,
                'conditions': conditions,
            }
        )
        print(id)
        update_rule_ids.append(id)


def delete_rule(rules):
    global delete_rule_ids
    delete_rule_ids = []
    for rule in rules:
        try:
            response = table.delete_item(
                Key={
                    'id': rule['id'],
                },
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            print("DeleteItem succeeded:", rule['id'])
            # print(json.dumps(response, indent=4, cls=DecimalEncoder))
            delete_rule_ids.append(rule['id'])
            # print(delete_rule_ids)


def scan_rules():
    global scan_rules_json
    scan_rules_json = []
    result = table.query(
        IndexName='tenant-index',
        KeyConditionExpression=Key('tenant_id').eq('123'), ScanIndexForward=True)
    print(result)
    print(result['Items'])
    scan_rules_json.append(result['Items'])


def lambda_handler(event, context):
    try:
        rules = json.loads(event['body'], parse_float=decimal.Decimal)
        operation = rules['operation']
        print(operation)

        if operation == "create":
            create_rule(rules['payload'])
            print(create_rule_ids)
            return {
                "statusCode": 200,
                "body": json.dumps(create_rule_ids, indent=4, cls=DecimalEncoder, ensure_ascii=False)
            }
        elif operation == "read":
            read_rule(rules['payload'])
            print(read_rules_ids)
            return {
                "statusCode": 200,
                "body": json.dumps(read_rules_ids, indent=4, cls=DecimalEncoder, ensure_ascii=False)
            }

        elif operation == "update":
            update_rule(rules['payload'])
            print(update_rule_ids)
            return {
                "statusCode": 200,
                "body": json.dumps(update_rule_ids, indent=4, cls=DecimalEncoder, ensure_ascii=False)
            }

        elif operation == "delete":
            delete_rule(rules['payload'])
            print(delete_rule_ids)
            return {
                "statusCode": 200,
                "body": json.dumps(delete_rule_ids, indent=4, cls=DecimalEncoder, ensure_ascii=False)
            }

        elif operation == "scan":
            scan_rules()
            print("OK")
            print(scan_rules_json)
            return {
                "statusCode": 200,
                "body": json.dumps(scan_rules_json, indent=4, cls=DecimalEncoder, ensure_ascii=False)
            }

        else:
            operation = rules['operation']
            return {
                "statusCode": 200,
                "body": json.dumps(f'Unknown operation: {operation}')}
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps(f'Unknown operation: {operation}, {str(e)}')}


lambda_handler({'resource': '/input_rule', 'path': '/input_rule', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7', 'cache-control': 'no-cache', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-Country': 'BR', 'content-type': 'application/json', 'Host': 'f1a6f3s2ec.execute-api.us-east-1.amazonaws.com', 'origin': 'chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Via': '2.0 387e6dddd12d03a0823f688d58241359.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'KqIGakz4kDCv2fUfdas_5uknpGCnrmFhaW5q9MbVALSE4JViy8DwGQ==', 'X-Amzn-Trace-Id': 'Root=1-5ceed36c-48ac7e740778f3fe710bc7da', 'X-Forwarded-For': '187.44.92.103, 70.132.44.142', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate, br'], 'Accept-Language': ['pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'], 'cache-control': ['no-cache'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-Country': ['BR'], 'content-type': ['application/json'], 'Host': ['f1a6f3s2ec.execute-api.us-east-1.amazonaws.com'], 'origin': ['chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop']], 'User-Agent': ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'], 'Via': ['2.0 387e6dddd12d03a0823f688d58241359.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['KqIGakz4kDCv2fUfdas_5uknpGCnrmFhaW5q9MbVALSE4JViy8DwGQ=='], 'X-Amzn-Trace-Id': ['Root=1-5ceed36c-48ac7e740778f3fe710bc7da'], 'X-Forwarded-For': ['187.44.92.103, 70.132.44.142'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {
               'resourceId': '8430gb', 'resourcePath': '/input_rule', 'httpMethod': 'POST', 'extendedRequestId': 'adX44FSQoAMFZVA=', 'requestTime': '29/May/2019:18:46:04 +0000', 'path': '/prod/input_rule', 'accountId': '301587852292', 'protocol': 'HTTP/1.1', 'stage': 'prod', 'domainPrefix': 'f1a6f3s2ec', 'requestTimeEpoch': 1559155564083, 'requestId': '02f8e87d-8242-11e9-b928-e98fc921eb68', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '187.44.92.103', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'user': None}, 'domainName': 'f1a6f3s2ec.execute-api.us-east-1.amazonaws.com', 'apiId': 'f1a6f3s2ec'},
    'body': '{\r\n "operation": "scan",\r\n "tableName": "lambda-apigateway",\r\n "payload": [\r\n {\r\n "id": "1235",\r\n "tenant_id": "123",\r\n "order": 5,\r\n "description": "Curadoria/Inéditos - Loggi - Excluir - RS e MG",\r\n "action": {\r\n "type": "quotation_exclude_carrier_method"\r\n },\r\n "conditions": [\r\n {\r\n "operation": "IN",\r\n "property": "metodo",\r\n "values": [\r\n "Loggi Standard"\r\n ]\r\n },\r\n {\r\n "operation": "IN",\r\n "property": "uf",\r\n "values": [\r\n "RS",\r\n "MG",\r\n "DF",\r\n "GO"\r\n ]\r\n }\r\n ]\r\n },\r\n {\r\n "id": "1232",\r\n "tenant_id": "123",\r\n "order": 2,\r\n "description": "(ALTERADO ADICIONA 2 PILA) Curadoria/Inéditos - Impresso - Fixar P - R$14,00 - NE",\r\n "action": {\r\n "type": "quotation_increase_price",\r\n "value": 1.7\r\n },\r\n "conditions": [\r\n {\r\n "operation": "IN",\r\n "property": "metodo",\r\n "values": [\r\n "Impresso Econômico"\r\n ]\r\n },\r\n {\r\n "operation": "IN",\r\n "property": "uf",\r\n "values": [\r\n "AL",\r\n "BA",\r\n "CE",\r\n "MA",\r\n "PB",\r\n "PE",\r\n "PI",\r\n "RN",\r\n "SE"\r\n ]\r\n },\r\n {\r\n "operation": "IN",\r\n "property": "sales_channel",\r\n "values": [\r\n "curadoria",\r\n "ineditos"\r\n ]\r\n }\r\n ]\r\n },\r\n {\r\n "id": "1233",\r\n "tenant_id": "123",\r\n "order": 3,\r\n "description": "Curadoria/Inéditos - Impresso - Fixar P - R$12,00 - SE e S",\r\n "action": {\r\n "type": "quotation_set_price",\r\n "value": 12\r\n },\r\n "conditions": [\r\n {\r\n "operation": "IN",\r\n "property": "metodo",\r\n "values": [\r\n "Impresso Econômico"\r\n ]\r\n },\r\n {\r\n "operation": "IN",\r\n "property": "uf",\r\n "values": [\r\n "ES",\r\n "MG",\r\n "RJ",\r\n "SP",\r\n "PR",\r\n "RS",\r\n "SC"\r\n ]\r\n }\r\n ]\r\n }\r\n ]\r\n}', 'isBase64Encoded': False}, "")
