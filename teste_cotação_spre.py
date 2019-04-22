
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Regras de Cotação").sheet1
list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)
pp = pprint.PrettyPrinter()
pp.pprint(list_of_hashes)

# for line in list_of_hashes:
#     print(line)
#     for att in line:
#         print(att)
#         if att == 

# 
# pp.pprint(list_of_hashes)


# result = sheet.row_values(6)
# pp.pprint(result)

# result = sheet.col_values(6)
# pp.pprint(result)

# result = sheet.cell(6,11)
# pp.pprint(result)

### Update data
# sheet.update_cell(6,11,'9999999')
# result = sheet.cell(6,11).value
# pp.pprint(result)
