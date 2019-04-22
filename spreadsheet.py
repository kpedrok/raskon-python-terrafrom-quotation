# https: // www.youtube.com/watch?v = vISRn5qFrkM

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

# use creds to create a client to interact with the Google Drive API

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
# sheet = client.open("Cópia de Legislators 2017").sheet1
sheet = client.open("Regras de Cotação").sheet1


# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)

# pp = pprint.PrettyPrinter()
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


