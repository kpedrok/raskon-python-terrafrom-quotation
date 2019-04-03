import decimal
import io
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


abrangencia_csv = 'abrangencia.csv'

batches = {
    'jadlog rodoviario': [],
    'flash_courier': [],
    'dialogo': [],
    'correios': [],
    'transfolha': [],
    'loggi': [],
    'speedlog': [],
    'nowlog': [],
    'shippify': [],

}


def _comparar_cep_transportadora(ceps):
    textfile = io.open(abrangencia_csv, 'rt', newline='', encoding='utf-8')
    linhas_transportadora = textfile.readlines()
    for indice_cep in range(0, len(ceps)):
        cep = ceps[indice_cep]
        cep_por_transportadora = cep.zfill(8)
        for indice_linha_transportadora in range(1, len(linhas_transportadora)):
            try:
                cep_transportadora = linhas_transportadora[indice_linha_transportadora].split(';')
                tokens = [token for token in cep_transportadora]
#0-Transportadora;1-Método de Envio;2-UF;3-Cidade;4-CEP Inicial;5-CEP Final;6-Tarifa;7-Prazo de Entrega
                transportadora = tokens[0]
                metodo_envio = tokens[1]
                uf = tokens[2]
                cidade = tokens[3]
                cep_inicial = tokens[4]
                cep_final = tokens[5]
                tarifa = tokens[6]
                prazo = tokens[7]
                if int(cep_inicial) <= int(ceps[indice_cep]) <= int(
                        cep_final) and metodo_envio not in cep_por_transportadora:
                    batches[metodo_envio].append({
                        "cep": str(ceps[indice_cep]),
                        "metodo": metodo_envio,
                        "tarifa": tarifa,
                        'prazo': prazo.replace("\r\n", ""),

                    })

            except Exception as e:
                mensagem_erro = "Erro na linha {}; {}".format(indice_linha_transportadora, e)
                print(mensagem_erro)
    print(json.dumps(batches, indent=4, ensure_ascii=False, separators=(',', ': ')))


def lambda_handler(event, context):
    linhas_cep = [event['queryStringParameters']['cep']]
    print (linhas_cep)
    _comparar_cep_transportadora(linhas_cep)


lambda_handler({'queryStringParameters': {'cep': '90480200'}}, "")