import requests
import json
import decimal
import os


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


url = "https://api.master.raskon.com.br/rules_quotation"

querystring = {"tenant_id": "123"}
payload = json.dumps([
    {
        "cep": 90480200,
        "transportadora": "Correios",
        "metodo": "Impresso Econômico",
        "tarifa": "Módico",
        "uf": "PE",
        "prazo": 8,
        "chave": "CorreiosImpresso EconômicoRSMódico",
        "price": 13.2,
        "sales_channel": "curadoria"
    },
    {
        "cep": 90480200,
        "transportadora": "Correios",
        "metodo": "Impresso Econômico",
        "tarifa": "Módico",
        "uf": "RS",
        "prazo": 8,
        "chave": "CorreiosImpresso EconômicoRSMódico",
        "price": 13.2,
        "sales_channel": "curadoria"
    },
    {
        "cep": 90480200,
        "transportadora": "Dialogo Logistica",
        "metodo": "Dialogo Standard",
        "tarifa": "CAPITAL",
        "uf": "RS",
        "prazo": 3,
        "chave": "Dialogo LogisticaDialogo StandardRSCAPITAL",
        "price": 4.66,
        "sales_channel": "curadoria"
    },
    {
        "cep": 90480200,
        "transportadora": "GolLog",
        "metodo": "GolLog DOC",
        "tarifa": "DOC",
        "uf": "NA",
        "prazo": 2,
        "chave": "GolLogGolLog DOCNADOC",
        "price": 12.98,
        "sales_channel": "curadoria"
    },
    {
        "cep": 90480200,
        "transportadora": "Jadlog",
        "metodo": "Jadlog Rodoviario",
        "tarifa": "Capital",
        "uf": "RS",
        "prazo": 2,
        "chave": "JadlogJadlog RodoviarioRSCapital",
        "price": 10.5,
        "sales_channel": "curadoria"
    },
    {
        "cep": 90480200,
        "transportadora": "Loggi",
        "metodo": "Loggi Standard",
        "tarifa": "RS Zona 1",
        "uf": "RS",
        "prazo": 3,
        "chave": "LoggiLoggi StandardRSRS Zona 1",
        "price": 14.24,
        "sales_channel": "curadoria"
    },
    {
        "cep": 90480200,
        "transportadora": "SPLog",
        "metodo": "SPLog Standard",
        "tarifa": "RS",
        "uf": "RS",
        "prazo": 15,
        "chave": "SPLogSPLog StandardRSRS",
        "price": 11.22,
        "sales_channel": "curadoria"
    },
    {
        "cep": 90480200,
        "transportadora": "Transfolha",
        "metodo": "Transfolha Terrestre",
        "tarifa": "CAP",
        "uf": "RS",
        "prazo": 4,
        "chave": "TransfolhaTransfolha TerrestreRSCAP",
        "price": 10.16,
        "sales_channel": "curadoria"
    }]
)


headers = {
    'content-type': "application/json; charset=utf-8",
    'x-api-key': "dZMXo39dF9aSGjNcxRdDY6e6lRDgvzp56M510JWs",
    'cache-control': "no-cache",
}

response = requests.request(
    "POST", url, data=payload, headers=headers, params=querystring)

print(response.text)

# json.dumps(response['Item'], sort_keys=True,
#            ensure_ascii=False, indent=4, cls=DecimalEncoder),


# response = requests.post(url, data=json.dumps(payload), headers=headers, params=querystring)
# print(response.text)
