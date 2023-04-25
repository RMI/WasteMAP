import xlwings as xw
import pandas as pd 
import numpy as np

#Puth the local path to the RMI Sharepoint Documents folder here
local_path = 'Testbook.xlsx'
#'/Users/atecza/Library/CloudStorage/OneDrive-RMI/Documents/'

filepath_workbook = f'{local_path}WasteMap/Sandbox/Testbook'

#open workbook
xl = xw.App(visible=False)
wb = xw.Book(filepath_workbook)

#Practice retreaiving values
my_value = wb.sheets["Inputs"].range("A2").value
print(my_value)

#Play around here. Practice with setting and removing values
wb.sheets["Outputs"].range("A3").value = 100
wb.sheets["Outputs"].range("A6").value = 200



# close the workbook
wb.close()
xl.quit()
del xl