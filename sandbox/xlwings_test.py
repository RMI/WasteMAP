import xlwings as xw
import pandas as pd 
import numpy as np

#Puth the local path to the RMI Sharepoint Documents folder here
#local_path = 'Testbook.xlsx'
#'/Users/atecza/Library/CloudStorage/OneDrive-RMI/Documents/'

#filepath_workbook = f'{local_path}WasteMap/Sandbox/Testbook'
filepath_workbook = 'C:\\Users\\andre.scheinwald\\Downloads\\Testbook.xlsx'

#open workbook
xl = xw.App(visible=False)
wb = xw.Book(filepath_workbook)

#Practice retreaiving values
my_value = wb.sheets["Inputs"].range("A2").value
my_value_2 = wb.sheets["Inputs"].range("A2:A6").value
my_value_3 = wb.sheets["Functions"].range("A2:B6").value
print(my_value)

#Play around here. Practice with setting and removing values
wb.sheets["Outputs"].range("A3").value = 100
wb.sheets["Outputs"].range("A6").value = 200


# Testing out a for loop to input a value down a column
for i in range(1,10):
    cell = f'A{i+1}'
    print(cell)
    wb.sheets["Retrieval"].range(cell).value = i
    
# Retrieving the results from the next column over
my_value_4 = wb.sheets["Retrieval"].range("A1:B10").value

df = pd.DataFrame(my_value_4)

df = df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)


# close the workbook
wb.save()
wb.close()
xl.quit()
del xl