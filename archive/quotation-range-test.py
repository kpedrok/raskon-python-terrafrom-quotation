
# x = {'cep': '01311300', 'transportadora': 'Correios',
#      'metodo': 'Impresso Econômico', 'tarifa': 'Módico', 'uf': 'SP', 'prazo': '9'}

# print(isinstance(x, int))
# print(isinstance(x, float))
# print(isinstance(x, str))
# print(isinstance(x, list))
# print(isinstance(x, dict))
# print(isinstance(x, tuple))
# print(isinstance(x, bool))
# print((x is None))

# d = {320: 1, 321: 0, 322: 3}
# print (d)
# mini = min(d, key=d.get)
# print(mini)

# dict_list = [{'price': 99, 'barcode': '2342355'},
#              {'price': 88, 'barcode': '2345566'}]
# seq = [x['price'] for x in dict_list]
# print(min(seq))
# print(max(seq))

lst = [{'price': 99, 'barcode': '2342355'},
       {'price': 88, 'barcode': '2345566'}]

maxPricedItem = max(lst, key=lambda x: x['price'])
minPricedItem = min(lst, key=lambda x: x['price'])
print (maxPricedItem, minPricedItem)