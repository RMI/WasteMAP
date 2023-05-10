import xlwings as xw
import pandas as pd 
import datetime as dt

filepath_workbook = 'C:\\Users\\andre.scheinwald\\Downloads\\SWEET_Version4.0.2_7.8.22.xlsm'

# Get workbook ready
xl = xw.App(visible=False)
wb = xw.Book(filepath_workbook)

def create_general_inputs(city: str, country: str, global_region: str, pop_in_col: int, pop_out_col: int):
    ls = wb.sheets['Default Values'].range("C13:V13").value
    if global_region in ls:
        pass
    else:
        print(f'Error: {global_region} is not an accepted parameter.  Please use the options found in {ls}')
    city = city
    country = country
    global_region = global_region
    pop_in_col = pop_in_col
    pop_out_col = pop_out_col
    current_year = dt.datetime.today().year
    return city, country, global_region, pop_in_col, pop_out_col, current_year
    
def create_climate_inputs(avg_annual_precip, avg_annual_temp):
    avg_annual_precip = avg_annual_precip
    avg_annual_temp = avg_annual_temp
    return avg_annual_precip, avg_annual_temp
    
def waste_generation_inputs(waste_gen_out_zone, hist_avg_annual, proj_avg_annual, perc_waste_gen_in, perc_waste_gen_out):
    waste_gen_out_zone = waste_gen_out_zone
    hist_avg_annual = hist_avg_annual
    proj_avg_annual = proj_avg_annual
    perc_waste_gen_in = perc_waste_gen_in
    perc_waste_gen_out = perc_waste_gen_out
    return waste_gen_out_zone, hist_avg_annual, proj_avg_annual, perc_waste_gen_in, perc_waste_gen_out
    

# Default waste percent function
def retrieve_waste_vals(exclude_totals: bool):
    ls = wb.sheets['Default Values'].range("B13:V24").value
    df = pd.DataFrame(ls)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)
    df = df.rename(columns = {'Region' : 'Type'})
    if exclude_totals:
       df = df.query("Type!='Total'")
    else:
        pass
    return df

def retrieve_gen_vals():
    ls = wb.sheets['Default Values'].range("G30:H50").value
    df = pd.DataFrame(ls)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)
    return df


def insert_general_data():
    wb.sheets["General Information"].range("C4").value = city
    wb.sheets["General Information"].range("C5").value = country
    wb.sheets["General Information"].range("C6").value = global_region
    wb.sheets["General Information"].range("C7").value = pop_in_col
    wb.sheets["General Information"].range("C8").value = pop_out_col
    wb.sheets["General Information"].range("C9").value = current_year
    wb.sheets["General Information"].range("C12").value = avg_annual_precip
    wb.sheets["General Information"].range("C13").value = avg_annual_temp
    wb.sheets["General Information"].range("C16").options(index=None, header=None).value = waste_gen_rate[waste_gen_rate['Region']==global_region]['Value']
    wb.sheets["General Information"].range("C17").value = waste_gen_out_zone
    wb.sheets["General Information"].range("C18").value = hist_avg_annual
    wb.sheets["General Information"].range("C19").value = proj_avg_annual
    wb.sheets["General Information"].range("C20").value = perc_waste_gen_in
    wb.sheets["General Information"].range("C21").value = perc_waste_gen_out
    wb.sheets["General Information"].range("C29:C38").options(pd.DataFrame, header=False, index=False).value = waste_values[[global_region]]


def landfill(total_sites: int, name, open_year, close_year, annual_disposal, site_type,
               avg_waste_depth, gas_system, gas_system_year = None, gas_project = None,
               methane_recovered = None, methane_recovered_year = None):
    wb.sheets["Landfills and Dumpsites"].range("B7").value = total_sites
    wb.sheets["Landfills and Dumpsites"].range("C13").value = name
    wb.sheets["Landfills and Dumpsites"].range("C14").value = open_year
    wb.sheets["Landfills and Dumpsites"].range("C15").value = close_year
    wb.sheets["Landfills and Dumpsites"].range("C16").value = annual_disposal
    wb.sheets["Landfills and Dumpsites"].range("C17").value = site_type
    wb.sheets["Landfills and Dumpsites"].range("C19").value = avg_waste_depth
    wb.sheets["Landfills and Dumpsites"].range("C20").value = gas_system
    if gas_system:
        wb.sheets["Landfills and Dumpsites"].range("C21").value = gas_system_year
        wb.sheets["Landfills and Dumpsites"].range("C22").value = gas_project
        wb.sheets["Landfills and Dumpsites"].range("C24").value = methane_recovered
        wb.sheets["Landfills and Dumpsites"].range("C25").value = methane_recovered_year
    else:
        pass
    
def summary_extraction(end_year):
    lower_row = current_year - 1949
    upper_row = end_year - 1949
    ls = wb.sheets['Summary - Emissions'].range(f'I{lower_row}:T{upper_row}').value
    column_names = ['year', 'waste_collection_and_transport', 'waste_burning', 'landfills_and_lfg_combustion' ,'organics_management',
                    'waste_handling_equipment',	'waste_combustion',	'total', 'total_metric_tons_ch4', 'total_metric_tons_sox',
                    'total_metric_tons_pm_2_5', 'total_metric_tons_pm_10']
    df = pd.DataFrame(ls, columns = column_names)
    return df

# close the workbook
def close_workbook(save_changes: bool):
    if save_changes:
        wb.save()
    else:
        pass
    wb.close()
    xl.quit()
    
city, country, global_region, pop_in_col, pop_out_col, current_year = create_general_inputs("Providence", 'United States', 'North America', 1100000, 0)

avg_annual_precip, avg_annual_temp = create_climate_inputs(1117.6, 9.72)

waste_gen_out_zone, hist_avg_annual, proj_avg_annual, perc_waste_gen_in, perc_waste_gen_out = waste_generation_inputs(0, 
                                                                                                                      0.03,
                                                                                                                      0.05,
                                                                                                                      1,
                                                                                                                      0)

waste_values = retrieve_waste_vals(exclude_totals = True)

waste_gen_rate = retrieve_gen_vals()

insert_general_data()

landfill(total_sites = 1, name = 'test', open_year = 2021, close_year = 2030,
         annual_disposal = 200000, site_type = 'Landfill', avg_waste_depth = 120, gas_system = 'No')

df = summary_extraction(2050)

close_workbook(save_changes = False)


# This only works when the workbook is open.
# def use_presets():
#     #'''This function just pushes the "Reset Per Capita Waste Generation Rate button"'''
#     ExcelMacro = wb.macro('ResetWasteGen')
#     ExcelMacro()

# stopping this function dev for now b/c it's kinda ridic.  Superficially not bad but then selecting yes/no changes the number of required inputs
# how can I use itertools when the size of the lists will change and the corresponding information between lists will get mismatched?
# def landfills(total_sites: int, name, open_year, close_year, annual_disposal, site_type,
#               avg_waste_depth, gas_system: bool, gas_system_year, gas_project: bool,
#               methane_recovered, methane_recovered_year):
#     wb.sheets["Landfills and Dumpsites"].range("B7").value = total_sites
#     upper = total_sites+1
#     for i in range(1, upper):
#         for (a,b,c,d,e,f,g,h,i,j,k) in itertools.zip_longest(name, open_year, close_year, annual_disposal, site_type,
#                                                              avg_waste_depth, gas_system, gas_system_year, gas_project,
#                                                              methane_recovered, methane_recovered_year):
#             wb.sheets["Landfills and Dumpsites"].range("B7").value = total_sites


# default_values = waste_values[[region]]



# #Practice retreaiving values
# my_value = wb.sheets["Inputs"].range("A2").value
# my_value_2 = wb.sheets["Inputs"].range("A2:A6").value
# my_value_3 = wb.sheets["Functions"].range("A2:B6").value
# print(my_value)


# # Testing out a for loop to input a value down a column
# for i in range(1,10):
#     cell = f'A{i+1}'
#     print(cell)
#     wb.sheets["Retrieval"].range(cell).value = i
    
# # Retrieving the results from the next column over
# my_value_4 = wb.sheets["Retrieval"].range("A1:B10").value

# df = pd.DataFrame(my_value_4)

# df = df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)





# ExcelMacro = wb.macro('AssumptionsWasteComp')
# ExcelMacro()

# resulting_values = wb.sheets["General Information"].range("C28:D39").value

# default_waste_dictionary = {'Australia and New Zealand' : [0.259, 0.122, 0.065, 0.12, 0.029, 0.083, 0.018, 0.028, 0.0000001, 0.276, 1.0000001],
#                             'Caribbean' : [0.469, 0.0000001, 0.024, 0.17, 0.051, 0.099, 0.05, 0.057, 0.019, 0.035, 0.9740001],
#                             'Central America' : [0.627, 0, 0.003, 0.126, 0.022, 0.103, 0.027, 0.033, 0, 0.06, 1.001],
#                             'Eastern Africa' : [0.444, 0.069, 0.005, 0.104, 0.03, 0.08, 0.026, 0.021, 0.004, 0.217, 1],
#                             'Eastern Asia' : [0.403, 0, 0.021, 0.204, 0.01, 0.065, 0.027, 0.043, 0, 0.229, 1.002],
#                             'Eastern Europe' : [0.318, 0.024, 0.025, 0.171, 0.031, 0.046, 0.007, 0.018, 0.005, 0.354, 0.999],
#                             'Middle Africa' : [0.284, 0, 0, 0.08, 0.013, 0.071, 0.014, 0.011, 0.0000001, 0.527, 1.0000001],
#                             "North America" : [0.202, 0.068, 0.041, 0.233, 0.039, 0.158, 0.064, 0.042, 0.016, 0.14, 1.003],
#                             "Northern Africa" : [0.504, 0, 0, 0.121, 0.058, 0.138, 0.044, 0.033, 0.0000001, 0.105, 1.0030001],
#                             "Northern Europe" : [0.303, 0.052, 0.018, 0.138, 0.032, 0.049, 0.014, 0.043, 0, 0.352, 1.001],
#                             "Rest of Oceania" : [0.675, 0.0000001, 0.025, 0.06, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.7600007],
#                             "South America" : [0.541, 0.033, 0, 0.124, 0.017, 0.137, 0.02, 0.03, 0.006, 0.091, 0.999],
#                             "Central Asia" : [0.3, 0.014, 0.025, 0.247, 0.035, 0.084, 0.008, 0.059, 0, 0.23, 1.002],
#                             "South-Eastern Asia" : [0.499, 0.01, 0.008, 0.112, 0.004, 0.102, 0.042, 0.037, 0, 0.186, 1],
#                             "Southern Africa" : [0.24, 0, 0, 0.145, 0.055, 0.265, 0.065, 0.09, 0, 0.14, 1],
#                             "Southern Europe" : [0.358, 0.014, 0.012, 0.214, 0.028, 0.141, 0.02, 0.035, 0.002, 0.178, 1.002],
#                             "Western Africa" : [0.539, 0, 0, 0.075, 0.019, 0.064, 0.027, 0.013, 0, 0.265, 1.002],
#                             "Western Asia" : [0.422, 0.032, 0.008, 0.153, 0.03, 0.172, 0.025, 0.034, 0.003, 0.122, 1.001],
#                             "Western Europe" : [0.332, 0.027, 0.023, 0.172, 0.059, 0.205, 0.015, 0.014, 0, 0.153, 1],
#                             "Southern Asia" : [0.661, 0, 0, 0.092, 0.012, 0.07, 0.009, 0.015, 0.004, 0.139, 1.002]}

# default_waste = pd.DataFrame(default_waste_dictionary)


def testloop(number: int, test):
    upper = number+1
    for i in range(1, upper):
        print(i + 2)

        
testloop(1, "idk")