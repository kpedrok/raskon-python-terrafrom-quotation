import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def get_coverage(cep):
    with open('quotation-coverage\coverage.json', encoding='utf-8') as f:
        cep = int(cep)
        data = json.load(f)
        j = 0
        abrang_tranps = []
        for i in data:
            j = j+1
            if int(i['cep_inicial']) <= cep <= int(i['cep_final']):
                abrang_tranps.append(i)
        print(json.dumps(abrang_tranps, sort_keys=False,
                         indent=4, ensure_ascii=False))
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(abrang_tranps, sort_keys=True,  ensure_ascii=False, indent=4, cls=DecimalEncoder),
    }


def lambda_handler(event, context):
    cep = event['queryStringParameters']['cep']
    cep = str(cep).replace("-", "").replace(".", "")
    get_coverage(cep)


lambda_handler({
    "queryStringParameters": {
        "cep": "90480200"
    }
}, "")
