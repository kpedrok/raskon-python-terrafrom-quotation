import pandas as pd

# ### Unificar planilhas já com vlookup
# df1 = pd.read_excel('vlookup_pandas.xlsx', sheet_name='Table1')
# df2 = pd.read_excel('vlookup_pandas.xlsx', sheet_name='Table2')
# results = df2.merge(df1, on='Name')
# print (df1)
# print (df2)
# print (results)
# print (results[results["Name"]=='Tom Brady'].head())


# ######Filtrar Linha e depois filtrar coluna
# df = pd.read_excel('consolidado.xlsx', sheet_name='costs')
# df2 = df[df['Chave']=='CorreiosImpresso EconômicoSPMódico'].head()
# print (df[df['Chave']=='CorreiosImpresso EconômicoSPMódico'].head())
# peso = 1
# df3 = df2[[peso]]
# print (df3) 

# ####### Encontrar preço a partir do peso e do método
# peso = 0.75
# df = pd.read_excel('consolidado.xlsx', sheet_name='costs')
# df2 = df.set_index("Chave", drop = False)
# price = df2.loc["CorreiosImpresso EconômicoSPMódico",peso]
# print (price) 


####### Cotação total - Excel 
# df1 = pd.read_excel('consolidado.xlsx', sheet_name='costs')
# df2 = pd.read_excel('consolidado.xlsx', sheet_name='range')
# results = df2.merge(df1, on='Chave')
# cep = 90480200
# cotacao = results[(results['CEP Final'] >= cep) & (results['CEP Inicial'] <= cep)].head(n=100)
# print (cotacao)


####### Exportaçaõ do Resultado
# cotacao.to_excel('out.xlsx')

#Verificar o tipo do header
# print (df.dtypes)