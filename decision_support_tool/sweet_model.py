import xlwings as xw
import pandas as pd 
import datetime as dt
import time

# Boolean operators for using excel values vs for loops
project_composting_year = True
user_selected_compost_percents = True
excel_file_gas_capture = False

# Location of the SWEET model that python will interact with
filepath_workbook = 'C:\\Users\\andre.scheinwald\\Downloads\\SWEET_Version4.0.2_7.8.22.xlsm'

# Get workbook ready
xl = xw.App(visible = False)

# Seeing how long it takes to open the workbook
start_time = time.time()
wb = xw.Book(filepath_workbook)
print(f'Opening the workbook took {round(time.time() - start_time, 2)} seconds')


# Opening the file that contains the data that will go into SWEET
def load_excel():
    df = pd.read_excel(r'C:\\Users\\andre.scheinwald\\Documents\\sweet_data_inputs_mockup.xlsx')
    return df


# Retrieves the default waste composition breakdown by region from SWEET
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


# Retrieves the default waste generation by region
def retrieve_gen_vals():
    ls = wb.sheets['Default Values'].range("G30:H50").value
    df = pd.DataFrame(ls)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)
    return df


# Takes data from the data spreadsheet and inserts it into the SWEET spreadsheet.
# Specifically inserts into the "General Information" tab in the "General", "Climate", "Waste Generation & Collection Rates", and "Average Composition of Collected Waste" sections.
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


# Checks if the inserted data will be user defined by for loops or defined by pre-determined data.  The latter still requires work.  The outer elifs are off.
# If user defined it uses the for loops to insert data on the "General Information" tab, "Waste Flow - Business As Usual (BAU)" section for composting and anaerobic digestion.
def insert_compost_ad(row, year_variable, percent_diverted, percent_compost_composted):
    if project_composting_year and user_selected_compost_percents:
        if percent_compost_composted == 0:
            wb.sheets["General Information"].range("C53:C54").clear_contents()
            wb.sheets["General Information"].range("C59:C62").clear_contents()
            total_waste = wb.sheets['General Information'].range("C22").value
            wb.sheets["General Information"].range("D53").value = dt.datetime.today().year + year_variable
            df = waste_values[['Type', row['global_region']]]
            df = df[df['Type'].isin(['Food Waste', 'Garden Waste', 'Wood', 'Paper/Cardboard'])]
            wb.sheets["General Information"].range("D54").value = percent_diverted * (1 - percent_compost_composted) * sum(df.iloc[:, 1]) * total_waste
            #df['weight'] = total_waste * df.iloc[:, 1] * percent_compost_composted
            df['ad_percent_total'] = df.iloc[:, 1] / sum(df.iloc[:, 1])
            wb.sheets["General Information"].range("D59:D62").options(pd.DataFrame, header=False, index=False).value = df[['ad_percent_total']]
        elif percent_compost_composted == 1:
            wb.sheets["General Information"].range("D53:D54").clear_contents()
            wb.sheets["General Information"].range("D59:D62").clear_contents()
            total_waste = wb.sheets['General Information'].range("C22").value
            wb.sheets["General Information"].range("C53").value = dt.datetime.today().year + year_variable
            df = waste_values[['Type', row['global_region']]]
            df = df[df['Type'].isin(['Food Waste', 'Garden Waste', 'Wood', 'Paper/Cardboard'])]
            wb.sheets["General Information"].range("C54").value = percent_diverted * percent_compost_composted * sum(df.iloc[:, 1]) * total_waste
            #df['weight'] = total_waste * df.iloc[:, 1] * percent_compost_composted
            df['compost_percent_total'] = df.iloc[:, 1] / sum(df.iloc[:, 1])
            wb.sheets["General Information"].range("C59:C62").options(pd.DataFrame, header=False, index=False).value = df[['compost_percent_total']]      
        else:
            total_waste = wb.sheets['General Information'].range("C22").value
            wb.sheets["General Information"].range("C53").value = dt.datetime.today().year + year_variable
            wb.sheets["General Information"].range("D53").value = dt.datetime.today().year + year_variable
            df = waste_values[['Type', row['global_region']]]
            df = df[df['Type'].isin(['Food Waste', 'Garden Waste', 'Wood', 'Paper/Cardboard'])]
            wb.sheets["General Information"].range("C54").value = percent_diverted * percent_compost_composted * sum(df.iloc[:, 1]) * total_waste
            wb.sheets["General Information"].range("D54").value = percent_diverted * (1-percent_compost_composted) * sum(df.iloc[:, 1]) * total_waste
            #df['weight'] = total_waste * df.iloc[:, 1] * percent_compost_composted
            df['diversion_percent_total'] = df.iloc[:, 1] / sum(df.iloc[:, 1])
            wb.sheets["General Information"].range("C59:C62").options(pd.DataFrame, header=False, index=False).value = df[['diversion_percent_total']]
            wb.sheets["General Information"].range("D59:D62").options(pd.DataFrame, header=False, index=False).value = df[['diversion_percent_total']]
    elif pd.isnull(row['composting_diversion_scenario_start_year']):
        wb.sheets["General Information"].range("C53:C54").clear_contents()
        wb.sheets["General Information"].range("C59:C62").clear_contents()
    elif pd.isnull(row['anaerobic_diversion_scenario_start_year']):
        wb.sheets["General Information"].range("D53:D54").clear_contents()
        wb.sheets["General Information"].range("D59:D62").clear_contents()
    else:
        wb.sheets["General Information"].range("C53").value = row['composting_diversion_scenario_start_year']
        wb.sheets["General Information"].range("C54").value = row['metric_tons_of_waste_delivered_to_composting_facility_per_year']
        wb.sheets["General Information"].range("C59").value = row['percent_of_composting_waste_targeted_for_diversion_food_waste']
        wb.sheets["General Information"].range("C60").value = row['percent_of_composting_waste_targeted_for_diversion_green']
        wb.sheets["General Information"].range("C61").value = row['percent_of_composting_waste_targeted_for_diversion_wood']
        wb.sheets["General Information"].range("C62").value = row['percent_of_composting_waste_targeted_for_diversion_paper_cardboard']
        wb.sheets["General Information"].range("D53").value = row['anaerobic_diversion_scenario_start_year']
        wb.sheets["General Information"].range("D54").value = row['metric_tons_of_waste_delivered_to_anaerobic_facility_per_year']
        wb.sheets["General Information"].range("D59").value = row['percent_of_anaerobic_waste_targeted_for_diversion_food_waste']
        wb.sheets["General Information"].range("D60").value = row['percent_of_anaerobic_waste_targeted_for_diversion_green']
        wb.sheets["General Information"].range("D61").value = row['percent_of_anaerobic_waste_targeted_for_diversion_wood']
        wb.sheets["General Information"].range("D62").value = row['percent_of_anaerobic_waste_targeted_for_diversion_paper_cardboard']
        

# Insert data into the SWEET "Landfills and Dumpsites" tab.  By default the first half of the function pulls from the excel.
# The nested if else checks what to do for the rest.  If excel_file_gas_capture is True then it uses the excel file to insert more data.
# Otherwise it clears out the capture and extraction related fields and insert_gas_capture() does the rest.
def insert_landfill(row):
    wb.sheets["Landfills and Dumpsites"].range("B7").value = 1
    wb.sheets["Landfills and Dumpsites"].range("C13").value = row['landfill_name']
    wb.sheets["Landfills and Dumpsites"].range("C14").value = row['site_opening_year']
    wb.sheets["Landfills and Dumpsites"].range("C15").value = row['site_closure_year']
    wb.sheets["Landfills and Dumpsites"].range("C16").value = row['most_recent_year_annual_disposal']
    #wb.sheets["Landfills and Dumpsites"].range("C17").value = row['landfill_or_dumpsite']
    wb.sheets["Landfills and Dumpsites"].range("C19").value = row['average_waste_depth']
    if excel_file_gas_capture:
        if row['existing_or_planned_gas_extraction']=='Yes':
            wb.sheets["Landfills and Dumpsites"].range("C20").value = row['existing_or_planned_gas_extraction']
            wb.sheets["Landfills and Dumpsites"].range("C21").value = row['gas_extraction_or_flaring_start_year']
            wb.sheets["Landfills and Dumpsites"].range("C22").value = row['existing_or_planned_gas_to_energy_project']
            wb.sheets["Landfills and Dumpsites"].range("C24").value = row['methane_recovery']
            wb.sheets["Landfills and Dumpsites"].range("C25").value = row['methane_recovery_data_year']
        else:
            wb.sheets["Landfills and Dumpsites"].range("C21").clear_contents()
            wb.sheets["Landfills and Dumpsites"].range("C24:C25").clear_contents()
    else:
        pass


# Function to change the landfill variable that is 100% dependent on the for loop. Extra work required if we want to switch back and forth between excel vs loop.
def insert_land_or_dump(landfill_variable):
    wb.sheets["Landfills and Dumpsites"].range("C17").value = landfill_variable


# Function to change the landfill gas caoture variable that is 100% dependent on the for loop. Extra work required if we want to switch back and forth between excel vs loop.
def insert_gas_capture(capture_variable):
    wb.sheets["Landfills and Dumpsites"].range("C20").value = capture_variable


# Extract the final output data from the "Summary - Emissions" tab "Table 2..." table from "Year" to "CH4" columns 
def summary_extraction(end_year):
    """
    The end_year variable is expressed as calendar year.
    end_year can be changed to retrieve less or more of the time series.
    Note that SWEET goes out to 2120.
    """
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
    data = load_excel()

# Create df of default waste composition for all global regions
waste_values = retrieve_waste_vals(exclude_totals = True)

# Create df of default waste generation rate for all global regions
waste_gen_rate = retrieve_gen_vals()

# Create empty list
appended_data = []

# Create list of landfill types
landfill_type = ['Controlled Dumpsite','Dumpsite','Landfill']

# Create list of diversion percent scenarios
diversion_percent = [0, 0.2, 0.4, 0.6]

# Create list of compost percent scenarios
composting_percent = [0, 0.2, 0.4, 0.6, 0.8, 1]

# Create list of years out composting should start from
#compost_year_variable = [1, 2, 3, 4, 5]
compost_year_variable = [0]

# Create list of methane capture scenarios
methane_capture = ['Yes', 'No']

# Create counter variable used in for loops
counter = 0

# Start time tracker for how efficient code is / isn't
start_time = time.time()

# The heavy lifting!
for index, row in data.iterrows():   
    insert_general_data(row)
    insert_landfill(row)
    if project_composting_year and user_selected_compost_percents:
        for diversion_perc in diversion_percent:
            for compost_perc in composting_percent:
                for year_var in compost_year_variable:
                    if diversion_perc == 0 and compost_perc > 0:
                        pass
                    else:
                        insert_compost_ad(row, year_var, diversion_perc, compost_perc)
                        for types in landfill_type:
                            for capture in methane_capture:
                                counter += 1
                                insert_land_or_dump(types)
                                insert_gas_capture(capture)
                                if diversion_perc == 0 and compost_perc > 0:
                                    pass
                                else:
                                    df = summary_extraction(2050)
                                    df['city'] = row['city']
                                    df['country'] = row['country']
                                    df['landfill_type'] = types
                                    df['diversion_percent'] = diversion_perc
                                    df['compost_percent'] = compost_perc
                                    df['compost_start_year'] = dt.datetime.today().year + year_var
                                    df['methane_capture'] = capture
                                    df['landfill_name'] = row['landfill_name']
                                    df['loop_iteration'] = counter
                                    appended_data.append(df)

# Create dataframe from appended_data list
final_df = pd.concat(appended_data)

# End time tracker kind of
print(f'The for loop took {round(time.time() - start_time, 2)} seconds to do {counter} iterations')

# Close workbook and don't save SWEET model excel file
close_workbook(save_changes = False)

# Output results to csv
final_df.to_csv("C:\\Users\\andre.scheinwald\\Documents\\sweet_output.csv", index=False)