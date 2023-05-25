import xlwings as xw
import pandas as pd 
import datetime as dt
import time

# Look into containerizing this
# batch!

filepath_workbook = 'C:\\Users\\andre.scheinwald\\Downloads\\SWEET_Version4.0.2_7.8.22.xlsm'

# Get workbook ready
xl = xw.App(visible=False)

start_time = time.time()
wb = xw.Book(filepath_workbook)
print(f'Opening the workbook took {round(time.time() - start_time, 2)} seconds')

def load_csv():
    df = pd.read_excel(r'C:\\Users\\andre.scheinwald\\Documents\\sweet_data_inputs_mockup_v2.xlsx')
    return df
    
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

def insert_general_data(row):
    ls = wb.sheets['Default Values'].range("C13:V13").value
    if row['global_region'] in ls:
        wb.sheets["General Information"].range("C4").value = row['city']
        wb.sheets["General Information"].range("C5").value = row['country']
        wb.sheets["General Information"].range("C6").value = row['global_region']
        wb.sheets["General Information"].range("C7").value = row['population_in_formal_collection_zones']
        wb.sheets["General Information"].range("C8").value = row['population_outside_formal_collection_zones']
        wb.sheets["General Information"].range("C9").value = dt.datetime.today().year
        wb.sheets["General Information"].range("C12").value = row['average_annual_precipitation']
        wb.sheets["General Information"].range("C13").value = row['mean_annual_temperature']
        wb.sheets["General Information"].range("C16").options(index=None, header=None).value = waste_gen_rate[waste_gen_rate['Region']==row['global_region']]['Value']
        wb.sheets["General Information"].range("C17").value = row['per_capita_waste_generation_rate_outside_collection_zone']
        wb.sheets["General Information"].range("C18").value = row['historical_average_annual_percent_growth_rate_quantity_waste_collected']
        wb.sheets["General Information"].range("C19").value = row['projected_average_annual_percent_growth_rate_quantity_waste_collected']
        wb.sheets["General Information"].range("C20").value = row['percent_waste_generated_inside_collection_zone']
        wb.sheets["General Information"].range("C21").value = row['percent_waste_generated_outside_collection_zone']
        wb.sheets["General Information"].range("C29:C38").options(pd.DataFrame, header=False, index=False).value = waste_values[[row['global_region']]]
    else:
        print(f'Error: {row["global_region"]} is not an accepted parameter.  Please use the options found in {ls}')
            
def insert_diversion(row):
      if pd.isnull(row['composting_diversion_scenario_start_year']):
          wb.sheets["General Information"].range("C53:C54").clear_contents()
          wb.sheets["General Information"].range("C59:C62").clear_contents()
          
      else:
          wb.sheets["General Information"].range("C53").value = row['composting_diversion_scenario_start_year']
          wb.sheets["General Information"].range("C54").value = row['metric_tons_of_waste_delivered_to_composting_facility_per_year']
          wb.sheets["General Information"].range("C59").value = row['percent_of_composting_waste_targeted_for_diversion_food_waste']
          wb.sheets["General Information"].range("C60").value = row['percent_of_composting_waste_targeted_for_diversion_green']
          wb.sheets["General Information"].range("C61").value = row['percent_of_composting_waste_targeted_for_diversion_wood']
          wb.sheets["General Information"].range("C62").value = row['percent_of_composting_waste_targeted_for_diversion_paper_cardboard']



def insert_landfill(row):
          wb.sheets["Landfills and Dumpsites"].range("B7").value = 1
          wb.sheets["Landfills and Dumpsites"].range("C13").value = row['landfill_name']
          wb.sheets["Landfills and Dumpsites"].range("C14").value = row['site_opening_year']
          wb.sheets["Landfills and Dumpsites"].range("C15").value = row['site_closure_year']
          wb.sheets["Landfills and Dumpsites"].range("C16").value = row['most_recent_year_annual_disposal']
          wb.sheets["Landfills and Dumpsites"].range("C17").value = row['landfill_or_dumpsite']
          wb.sheets["Landfills and Dumpsites"].range("C19").value = row['average_waste_depth']
          wb.sheets["Landfills and Dumpsites"].range("C20").value = row['existing_or_planned_gas_extraction']
          if row['existing_or_planned_gas_extraction']=='Yes':
                  wb.sheets["Landfills and Dumpsites"].range("C21").value = row['gas_extraction_or_flaring_start_year']
                  wb.sheets["Landfills and Dumpsites"].range("C22").value = row['existing_or_planned_gas_to_energy_project']
                  wb.sheets["Landfills and Dumpsites"].range("C24").value = row['methane_recovery']
                  wb.sheets["Landfills and Dumpsites"].range("C25").value = row['methane_recovery_data_year']
          else:
                  wb.sheets["Landfills and Dumpsites"].range("C21").clear_contents()
                  wb.sheets["Landfills and Dumpsites"].range("C24:C25").clear_contents()
    
def summary_extraction(end_year):
    lower_row = dt.datetime.today().year - 1949
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

if __name__ == "__main__":
    data = load_csv()
    
waste_values = retrieve_waste_vals(exclude_totals = True)

waste_gen_rate = retrieve_gen_vals()

appended_data = []

counter = 0

start_time = time.time()

for index, row in data.iterrows():
    counter += 1
    insert_general_data(row)
    insert_diversion(row)
    insert_landfill(row)
    df = summary_extraction(2050)
    df['city'] = row['city']
    df['country'] = row['country']
    df['loop_iteration'] = counter
    appended_data.append(df)
    
final_df = pd.concat(appended_data)

print(f'The for loop took {round(time.time() - start_time, 2)} seconds to do {counter} iterations')

close_workbook(save_changes = False)