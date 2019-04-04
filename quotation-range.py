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


ARQUIVO_TRANSPORTADORA_CSV = 'abrangencia.csv'

batches = {
    'Azul Cargo': [],
    'Correios': [],
    'Dialogo Logistica': [],
    'GolLog': [],
    'Jadlog': [],
    'Loggi': [],
    'Nowlog': [],
    'Speedlog': [],
    'SPLog': [],
    'Transfolha': [],
}


def quotation_range(ceps):
    textfile = io.open(ARQUIVO_TRANSPORTADORA_CSV, 'r',
                       newline='', encoding='utf-8')
    linhas_transportadora = textfile.readlines()
    for indice_cep in range(0, len(ceps)):
        cep = ceps[indice_cep]
        cep_por_transportadora = cep.zfill(8)
        for indice_linha_transportadora in range(1, len(linhas_transportadora)):
            try:
                # 0 - Transportadora; 1 - Método de Envio; 2 - UF; 3 - Cidade; 4 - CEP Inicial; 5 - CEP Final; 6 - Tarifa; 7 - Prazo de Entrega;
                cep_transportadora = linhas_transportadora[indice_linha_transportadora].split(
                    ';')
                tokens = [token for token in cep_transportadora]
                transportadora = tokens[0]
                metodo_envio = tokens[1]
                uf = tokens[2]
                # cidade = tokens[3]
                cep_inicial = tokens[4]
                cep_final = tokens[5]
                tarifa = tokens[6]
                prazo = tokens[7]
                if int(cep_inicial) <= int(ceps[indice_cep]) <= int(cep_final) and transportadora not in cep_por_transportadora:
                    batches[transportadora].append({
                        "cep": int(ceps[indice_cep]),
                        "transportadora": transportadora,
                        "metodo": metodo_envio,
                        "tarifa": tarifa,
                        "uf": uf,
                        'prazo': int(prazo.replace("\r\n", "")),
                        'chave': transportadora + metodo_envio + uf + tarifa
                    })

            except Exception as e:
                mensagem_erro = "Erro na linha {}; {}".format(
                    indice_linha_transportadora, e)
                print(mensagem_erro)
    quotation = []
    for transportadora in batches:
        if batches[transportadora] != []:
            quotation.append(batches[transportadora])
            print(batches[transportadora])
        else:
            pass
    # print (quotation)
    # print(json.dumps(quotation, indent=4, ensure_ascii=False, separators=(',', ': ')))

    # print(json.dumps(batches, indent=4, ensure_ascii=False, separators=(',', ': ')))
    print(batches)


def lambda_handler(event, context):
    print(event)
    linhas_cep = [event['queryStringParameters']['cep']]
    quotation_range(linhas_cep)


lambda_handler({
    'queryStringParameters': {
        'cep': '90480200',
        'invoice_cost': '69,90',
        'weight': '600',
    }
}, '')
