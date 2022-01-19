import time

import pandas as pd
xls = pd.ExcelFile(r"Перечень субмоделей.xlsx") #use r before absolute file path

sheetX = xls.parse(0) #2 is the sheet number+1 thus if the file has only 1 sheet write 0 in paranthesis
dict_submodels = dict()
engine = sheetX['Код Модели']
vins = sheetX['vin']
# print(list(engine))
# print(list(vins))
for vin in range(len(vins)):
    dict_submodels[vins[vin]] = engine[vin]

# print(dict_submodels)
#
# for vin in dict_submodels.keys():
#     # try:
#         with open(f"vin_result_{vin.replace(' ', '')}.txt", "r", encoding="cp1251") as file:
#             print(vin)
#             print(file.readline())
#     # except Exception as err:
#         # with open("errors_read_vin_.txt", "a", encoding="utf-8") as file_with_err:
#         #     file_with_err.write(f"{err}\n")


import codecs
for vin in dict_submodels.keys():
    try:
        file_to_write = codecs.open("res.txt", "a", 'utf-8', errors='ignore')
        f = codecs.open(f"vin_result_{vin.replace(' ', '')}.txt", "r", 'utf-8', errors='ignore')

        for n, item in enumerate(f):
            if n == 0:
                file_to_write.write(f"{item}")
            else:
                file_to_write.write(f"{item[:-2] + ';' + dict_submodels[vin]} \n")
            #

    except:
        continue