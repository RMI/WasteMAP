#%%

import pandas as pd

waste_fraction_defaults = {'Australia and New Zealand' : [0.259, 0.122, 0.065, 0.12, 0.029, 0.083, 0.018, 0.028, 0.0000001, 0.276, 1.0000001],
                            'Caribbean' : [0.469, 0.0000001, 0.024, 0.17, 0.051, 0.099, 0.05, 0.057, 0.019, 0.035, 0.9740001],
                            'Central America' : [0.627, 0, 0.003, 0.126, 0.022, 0.103, 0.027, 0.033, 0, 0.06, 1.001],
                            'Eastern Africa' : [0.444, 0.069, 0.005, 0.104, 0.03, 0.08, 0.026, 0.021, 0.004, 0.217, 1],
                            'Eastern Asia' : [0.403, 0, 0.021, 0.204, 0.01, 0.065, 0.027, 0.043, 0, 0.229, 1.002],
                            'Eastern Europe' : [0.318, 0.024, 0.025, 0.171, 0.031, 0.046, 0.007, 0.018, 0.005, 0.354, 0.999],
                            'Middle Africa' : [0.284, 0, 0, 0.08, 0.013, 0.071, 0.014, 0.011, 0.0000001, 0.527, 1.0000001],
                            "North America" : [0.202, 0.068, 0.041, 0.233, 0.039, 0.158, 0.064, 0.042, 0.016, 0.14, 1.003],
                            "Northern Africa" : [0.504, 0, 0, 0.121, 0.058, 0.138, 0.044, 0.033, 0.0000001, 0.105, 1.0030001],
                            "Northern Europe" : [0.303, 0.052, 0.018, 0.138, 0.032, 0.049, 0.014, 0.043, 0, 0.352, 1.001],
                            "Rest of Oceania" : [0.675, 0.0000001, 0.025, 0.06, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.7600007],
                            "South America" : [0.541, 0.033, 0, 0.124, 0.017, 0.137, 0.02, 0.03, 0.006, 0.091, 0.999],
                            "Central Asia" : [0.3, 0.014, 0.025, 0.247, 0.035, 0.084, 0.008, 0.059, 0, 0.23, 1.002],
                            "South-Eastern Asia" : [0.499, 0.01, 0.008, 0.112, 0.004, 0.102, 0.042, 0.037, 0, 0.186, 1],
                            "Southern Africa" : [0.24, 0, 0, 0.145, 0.055, 0.265, 0.065, 0.09, 0, 0.14, 1],
                            "Southern Europe" : [0.358, 0.014, 0.012, 0.214, 0.028, 0.141, 0.02, 0.035, 0.002, 0.178, 1.002],
                            "Western Africa" : [0.539, 0, 0, 0.075, 0.019, 0.064, 0.027, 0.013, 0, 0.265, 1.002],
                            "Western Asia" : [0.422, 0.032, 0.008, 0.153, 0.03, 0.172, 0.025, 0.034, 0.003, 0.122, 1.001],
                            "Western Europe" : [0.332, 0.027, 0.023, 0.172, 0.059, 0.205, 0.015, 0.014, 0, 0.153, 1],
                            "Southern Asia" : [0.661, 0, 0, 0.092, 0.012, 0.07, 0.009, 0.015, 0.004, 0.139, 1.002]}

waste_fraction_defaults = pd.DataFrame(waste_fraction_defaults).T
waste_fraction_defaults.columns = ['food', 'green', 'wood', 'paper_cardboard', 'textiles', 'plastic', 'metal', 'glass', 'rubber', 'other', 'total']
waste_fraction_defaults.head()
#waste_fraction_defaults = waste_fraction_defaults.T.to_dict()

region_lookup = {'China': 'Eastern Asia',
                 'Japan': 'Eastern Asia',
                 'Republic of Korea': 'Eastern Asia',
                 'Mongolia': 'Central Asia',
                 'Democratic People\'s Republic of Korea': 'Eastern Asia',
                 'Bangladesh': 'Southern Asia',
                 'India': 'Southern Asia',
                 'Nepal': 'Southern Asia',
                 'Sri Lanka': 'Southern Asia',
                 'Pakistan': 'Southern Asia',
                 'Brunei Darussalam': 'South-Eastern Asia',
                 'Cambodia': 'South-Eastern Asia',
                 'Indonesia': 'South-Eastern Asia',
                 'Lao People\'s Democratic Republic': 'South-Eastern Asia',
                 'Malaysia': 'South-Eastern Asia',
                 'Myanmar': 'South-Eastern Asia',
                 'Philippines': 'South-Eastern Asia',
                 'Singapore': 'South-Eastern Asia',
                 'Thailand': 'South-Eastern Asia',
                 'Vietnam ': 'South-Eastern Asia',
                 'Afghanistan': 'Central Asia',
                 'Kazakhstan': 'Central Asia',
                 'Tajikistan': 'Central Asia',
                 'Turkmenistan': 'Central Asia',
                 'Kyrgyzstan': 'Central Asia',
                 'Uzbekistan': 'Central Asia',
                 'Armenia': 'Western Asia',
                 'Georgia': 'Western Asia',
                 'Azerbaijan': 'Western Asia',
                 'Saudi Arabia': 'Western Asia',
                 'Iran': 'Western Asia',
                 'Iraq': 'Western Asia',
                 'Syrian Arab Republic': 'Western Asia',
                 'Lebanon': 'Western Asia',
                 'Israel': 'Western Asia',
                 'Kuwait': 'Western Asia',
                 'Jordan': 'Western Asia',
                 'Yemen': 'Western Asia',
                 'Oman': 'Western Asia',
                 'United Arab Emirates': 'Western Asia',
                 'Qatar': 'Western Asia',
                 'Bahrain': 'Western Asia',
                 'Egypt': 'Northern Africa',
                 'Libya': 'Northern Africa',
                 'Tunisia': 'Northern Africa',
                 'Algeria': 'Northern Africa',
                 'Morocco': 'Northern Africa',
                 'Sudan': 'Northern Africa',
                 'South Sudan': 'Northern Africa',
                 'Western Sahara': 'Northern Africa',
                 'Eritrea': 'Eastern Africa',
                 'Ethiopia': 'Eastern Africa',
                 'Somalia': 'Eastern Africa',
                 'Djibouti': 'Eastern Africa',
                 'Uganda': 'Eastern Africa',
                 'Kenya': 'Eastern Africa',
                 'Rwanda': 'Eastern Africa',
                 'Burundi': 'Eastern Africa',
                 'Tanzaia': 'Eastern Africa',
                 'Mauritanina': 'Western Africa',
                 'Senegal': 'Western Africa',
                 'The Gambia': 'Western Africa',
                 'Guinne-Bissau': 'Western Africa',
                 'Guinea': 'Western Africa',
                 'Sierra Leone': 'Western Africa',
                 'Liberia': 'Western Africa',
                 'Cote d\'Ivoire': 'Western Africa',
                 'Ghana': 'Western Africa',
                 'Togo': 'Western Africa',
                 'Benin': 'Western Africa',
                 'Nigeria': 'Western Africa',
                 'Mali': 'Middle Africa',
                 'Burkina Faso': 'Middle Africa',
                 'Niger': 'Middle Africa',
                 'Chad': 'Middle Africa',
                 'Central African Republic': 'Middle Africa',
                 'Cameroon': 'Middle Africa',
                 'Republic of Congo': 'Middle Africa',
                 'Democratic Republic of Congo': 'Middle Africa',
                 'Angola': 'Middle Africa',
                 'Zambia': 'Middle Africa',
                 'Gabon': 'Middle Africa',
                 'Malawi': 'Middle Africa',
                 'Namibia': 'Southern Africa',
                 'Botswana': 'Southern Africa',
                 'Zimbabwe': 'Southern Africa',
                 'Mozambique': 'Southern Africa',
                 'Madagascar': 'Southern Africa',
                 'South Africa': 'Southern Africa',
                 'Lesotho': 'Southern Africa',
                 'Eswatini': 'Southern Africa',
                 'Comoros': 'Southern Africa',
                 'Bulgaria': 'Eastern Europe',
                 'Croatioa': 'Eastern Europe',
                 'Serbia': 'Eastern Europe',
                 'Montenegro': 'Eastern Europe',
                 'Kosovo': 'Eastern Europe',
                 'Bosnia and Herzegovina': 'Eastern Europe',
                 'Albania': 'Eastern Europe',
                 'Czechia': 'Eastern Europe',
                 'Slovakia': 'Eastern Europe',
                 'Slovenia': 'Eastern Europe',
                 'Romania': 'Eastern Europe',
                 'Russian Federation': 'Eastern Europe',
                 'Ukraine': 'Eastern Europe',
                 'Belarus': 'Eastern Europe',
                 'Latvia': 'Eastern Europe',
                 'Lithuania': 'Eastern Europe',
                 'Estonia': 'Eastern Europe',
                 'Poland': 'Eastern Europe',
                 'Hungary': 'Eastern Europe',
                 'Republic of Moldova': 'Eastern Europe',
                 'Denmark': 'Northern Europe',
                 'Finland': 'Northern Europe',
                 'Sweden': 'Northern Europe',
                 'Norway': 'Northern Europe',
                 'Iceland': 'Northern Europe',
                 'Cyprus': 'Southern Europe',
                 'Greece': 'Southern Europe',
                 'Italy': 'Southern Europe',
                 'Malta': 'Southern Europe',
                 'Spain': 'Southern Europe',
                 'Portugal': 'Southern Europe',
                 'Turkey': 'Southern Europe',
                 'Austria': 'Western Europe',
                 'Belgium': 'Western Europe',
                 'Netherlands': 'Western Europe',
                 'France': 'Western Europe',
                 'Germany': 'Western Europe',
                 'Ireland': 'Western Europe',
                 'Luxembourg': 'Western Europe',
                 'Switzerland': 'Western Europe',
                 'United Kingdom': 'Western Europe',
                 'Bahamas': 'Caribbean',
                 'Cuba': 'Caribbean',
                 'Dominican Republic': 'Caribbean',
                 'St. Lucia': 'Caribbean',
                 'Costa Rica': 'Central America',
                 'Guatemala': 'Central America',
                 'Hondruas': 'Central America',
                 'Nicarauga': 'Central America',
                 'Belize': 'Central America',
                 'Panama': 'Central America',
                 'El Salvador': 'Central America',
                 'Argentina': 'South America',
                 'Bolivia': 'South America',
                 'Brazil': 'South America',
                 'Chile': 'South America',
                 'Colombia': 'South America',
                 'Ecuador': 'South America',
                 'Paraguay': 'South America',
                 'Peru': 'South America',
                 'Uruguay': 'South America',
                 'Venezuela': 'South America',
                 'Canada': 'North America',
                 'Mexico': 'North America',
                 'United States of America': 'North America',
                 'American Samoa': 'North America',
                 'Australia': 'Australia and New Zealand',
                 'New Zealand': 'Australia and New Zealand',
                 'Fiji': 'Rest of Oceania',
                 'Papua New Guinea': 'Rest of Oceania',
                 'Bhutan': 'Southern Asia',
                 'Côte d’Ivoire': 'Western Africa',
                 'Congo, Dem. Rep.': 'Middle Africa',
                 'Congo, Rep.': 'Middle Africa',
                 'Czech Republic': 'Eastern Europe',
                 'Egypt, Arab Rep.': 'Northern Africa',
                 'Micronesia, Fed. Sts.': 'Rest of Oceania',
                 'Gambia, The': 'Western Africa',
                 'Equatorial Guinea': 'Middle Africa',
                 'Honduras': 'Central America',
                 'Croatia': 'Eastern Europe',
                 'Haiti': 'Caribbean',
                 'Isle of Man': 'Western Europe',
                 'Iran, Islamic Rep.': 'Western Asia',
                 'Kyrgyz Republic': 'Central Asia',
                 'Kiribati': 'Rest of Oceania',
                 'Korea, Rep.': 'Eastern Asia',
                 'Lao PDR': 'South-Eastern Asia',
                 'Moldova': 'Eastern Europe',
                 'Maldives': 'Southern Asia',
                 'Marshall Islands': 'Rest of Oceania',
                 'Macedonia, FYR': 'Eastern Europe',
                 'Northern Mariana Islands': 'Rest of Oceania',
                 'Mauritania': 'Western Africa',
                 'Nicaragua': 'Central America',
                 'Palau': 'Rest of Oceania',
                 'West Bank and Gaza': 'Western Asia',
                 'Solomon Islands': 'Rest of Oceania',
                 'Slovak Republic': 'Eastern Europe',
                 'Timor-Leste': 'South-Eastern Asia',
                 'Tonga': 'Rest of Oceania',
                 'Tuvalu': 'Rest of Oceania',
                 'Tanzania': 'Eastern Africa',
                 'United States': 'North America',
                 'Venezuela, RB': 'South America',
                 'Vietnam': 'South-Eastern Asia',
                 'Vanuatu': 'Rest of Oceania',
                 'Samoa': 'Rest of Oceania',
                 'Yemen, Rep.': 'Western Asia',
                }


msw_per_capita_defaults = {'Australia and New Zealand' : 1.643835616438360,
                           'Caribbean' : 2.136986301369860,
                           'Central America' : 1.589041095890410,
                           'Central Asia' : 0.931506849315068,
                           'Eastern Africa' : 0.794520547945205,
                           'Eastern Asia' : 1.315068493150680,
                           'Eastern Europe' : 1.013698630136990,
                           'Middle Africa' : 0.520547945205479,
                           'North America' : 2.630136986301370,
                           "Northern Africa" : 1.123287671232880,
                           "Northern Europe" : 1.315068493150680,
                           "Rest of Oceania" : 0.931506849315068,
                           "South America" : 1.178082191780820,
                           "South-Eastern Asia" : 1.260273972602740,
                           "Southern Africa" : 0.904109589041096,
                           "Southern Asia" : 1.369863013698630,
                           "Southern Europe" : 1.287671232876710,
                           "Western Africa" : 0.493150684931507,
                           "Western Asia" : 1.890410958904110,
                           "Western Europe" : 1.616438356164380,
                            }

k_defaults = {'Dry':            {'food': .1,  'diapers': .1,  'green': .05, 'paper_cardboard': .02,  'textiles': .02,  'wood': .01,  'rubber': .01},
              'Moderately Dry': {'food': .18, 'diapers': .18, 'green': .09, 'paper_cardboard': .036, 'textiles': .036, 'wood': .018, 'rubber': .018},
              'Moderately Wet': {'food': .26, 'diapers': .26, 'green': .12, 'paper_cardboard': .048, 'textiles': .048, 'wood': .024, 'rubber': .024},
              'Wet':            {'food': .34, 'diapers': .34, 'green': .15, 'paper_cardboard': .06,  'textiles': .06,  'wood': .03,  'rubber': .03},
              'Very Wet':       {'food': .4,  'diapers': .4,  'green': .17, 'paper_cardboard': .07,  'textiles': .07,  'wood': .035, 'rubber': .035}
             }

k_defaults = pd.DataFrame(k_defaults).T

# Function to get precipitation zone from annual rainfall
def get_precipitation_zone(rainfall):
    # Unit is mm
    if rainfall < 500:
        return "Dry"
    elif rainfall < 1000:
        return "Moderately Dry"
    elif rainfall < 1500:
        return "Moderately Wet"
    elif rainfall < 2000:
        return "Wet"
    else:
        return "Very Wet"
    
L_0 = {'food': 70, 'diapers': 112, 'green': 93, 'paper_cardboard': 186, 'textiles': 112, 'wood': 200, 'rubber': 100}

oxidation_factor = {'with_lfg':{'landfill': 0.22, 'controlled_dump_site': 0.1, 'dump_site': 0, 'remediated_to_landfill': 0.18}, 
                    'without_lfg':{'landfill': 0.1, 'controlled_dump_site': 0.05, 'dump_site': 0, 'remediated_to_landfill': 0.1}}

#mef_compost = 0.005876238822222 # Unit is Mg CO2e/Mg of organic waste, wtf
mef_anaerobic = 0.000286598 # Unit is Mg CH4/Mg organic waste...wtf 

#%%

import pandas as pd
import numpy as np

runs_q = {}
runs_m = {}
organics_q = {}

# Load cities
cities = pd.read_csv('C:/Users/hughr/OneDrive/Documents/RMI/What_a_Waste/city_level_data_0_0.csv')

for row in cities.iterrows():
    city = row[1]['city_name']
    country = row[1]['country_name']
    region = region_lookup[country]

    # population
    population = float(row[1]['population_population_number_of_people'])
    # check if population is nan
    #if population != population:
        #print('find pop function needed')

    #growth_rate_historic = 1.03
    growth_rate = 1.03
    #years_into_past = 50
    #years_into_future = 50
    #current_year = 2023

    # waste total
    try:
        waste_total = float(row[1]['total_msw_total_msw_generated_tons_year'])
    except:
        waste_total = float(row[1]['total_msw_total_msw_generated_tons_year'].replace(',', ''))
    if waste_total != waste_total:
        # Use per capita default
        waste_per_capita = msw_per_capita_defaults[region]
        waste_total = waste_per_capita * population
    
    # waste fractions
    waste_fractions = row[1][['composition_food_organic_waste_percent', 
                         'composition_yard_garden_green_waste_percent', 
                         'composition_wood_percent',
                         'composition_paper_cardboard_percent',
                         'composition_plastic_percent',
                         'composition_metal_percent',
                         'composition_glass_percent',
                         'composition_other_percent',
                         'composition_rubber_leather_percent',
                         ]]

    waste_fractions.rename(index={'composition_food_organic_waste_percent': 'food',
                                    'composition_yard_garden_green_waste_percent': 'green',
                                    'composition_wood_percent': 'wood',
                                    'composition_paper_cardboard_percent': 'paper_cardboard',
                                    'composition_plastic_percent': 'plastic',
                                    'composition_metal_percent': 'metal',
                                    'composition_glass_percent': 'glass',
                                    'composition_other_percent': 'other',
                                    'composition_rubber_leather_percent': 'rubber'
                                    }, inplace=True)
    waste_fractions /= 100
    
    # Add zeros where there are no values unless all values are nan
    if waste_fractions.isna().all():
        waste_fractions = waste_fraction_defaults.loc[region, :]
    else:
        waste_fractions.fillna(0, inplace=True)
        waste_fractions['textiles'] = 0
    
    if (waste_fractions.sum() < .9) or (waste_fractions.sum() > 1.1):
        #print('waste fractions do not sum to 1')
        waste_fractions = waste_fraction_defaults.loc[region, :]
        continue

    waste_fractions = waste_fractions.to_dict()

    mef_compost = (0.0055 * waste_fractions['food']/(waste_fractions['food'] + waste_fractions['green']) + \
                   0.0139 * waste_fractions['green']/(waste_fractions['food'] + waste_fractions['green'])) * 1.1023 * 0.7 / 28
                   # Unit is Mg CO2e/Mg of organic waste, wtf, so convert to CH4. Mistake in sweet here
    # precipitation
    precip = 1277.8 # mm
    precip_zone = get_precipitation_zone(precip)

    # depth
    #depth = 10

    # methane correction factor
    #mcf_dump = mcf_defaults['Managed Landfill']['Deep']
    #mcf_landfill = mcf_defaults['Managed Landfill']['Deep']

    mcf_dump = .4
    mcf_landfill = 1

    # k values
    ks = k_defaults.loc[precip_zone, :].to_dict()
    
    # model components
    components = set(['food', 'green', 'wood', 'paper_cardboard', 'textiles'])
    
    # landfills
    landfill_sites = ['landfill', 'dump_site']
    mcfs = {'landfill': mcf_landfill, 'dump_site': mcf_dump}
    diversion_fractions = {'landfill': np.nan_to_num(row[1]['waste_treatment_controlled_landfill_percent'])/100,
                            'dump_site': (np.nan_to_num(row[1]['waste_treatment_open_dump_percent']) +
                                    np.nan_to_num(row[1]['waste_treatment_landfill_unspecified_percent']) +
                                    np.nan_to_num(row[1]['waste_treatment_unaccounted_for_percent']))/100}
    
    diversion_total = sum([diversion_fractions[x] for x in diversion_fractions.keys()])
    if diversion_total == 0:
        diversion_fractions = {'landfill': 0, 'dump_site': 1}
    else:
        for site in diversion_fractions.keys():
            diversion_fractions[site] /= diversion_total

    print(diversion_fractions)

    # compost
    compost_total = 0
    compost_components = set(['food', 'green', 'wood', 'paper_cardboard']) # Double check we don't want to include paper
    compost_fraction_of_total = float(row[1]['waste_treatment_compost_percent']) / 100   
    if compost_fraction_of_total != compost_fraction_of_total:
        compost_fraction_of_total = 0
    compost_total = compost_fraction_of_total * waste_total
    fraction_compostable = sum([waste_fractions[x] for x in compost_components])
    if compost_fraction_of_total != 0:
        compost_waste_fractions = {x: waste_fractions[x] / fraction_compostable for x in compost_components}
        #non_compostable_not_targeted = .1 # I don't know what this means, basically, waste that gets composted that shouldn't have been and isn't compostable?
        non_compostable_not_targeted = {'food': .1, 'green': .05, 'wood': .05, 'paper_cardboard': .1}
        non_compostable_not_targeted_total = sum([non_compostable_not_targeted[x] * compost_waste_fractions[x] for x in compost_components])
        unprocessable = {'food': .0192, 'green': .042522, 'wood': .07896, 'paper_cardboard': .12}

        compost_vol = {}
        for waste in compost_components:
            compost_vol[waste] = (
                compost_total
                * (1 - non_compostable_not_targeted_total)
                * compost_waste_fractions[waste]
                * (1 - unprocessable[waste])
                )
    else:
        compost_vol = {x: 0 for x in compost_components}

    # anaerobic digestion
    anaerobic_total = 0
    components_anaerobic = set(['food', 'green', 'wood', 'paper_cardboard'])
    anaerobic_fraction_of_total = float(row[1]['waste_treatment_anaerobic_digestion_percent']) / 100
    if anaerobic_fraction_of_total != anaerobic_fraction_of_total:
        anaerobic_fraction_of_total = 0
    if anaerobic_fraction_of_total != 0:
        anaerobic_total = anaerobic_fraction_of_total * waste_total
        #print(anaerobic_total)
        fraction_anaerobic = sum([waste_fractions[x] for x in compost_components])
        anaerobic_waste_fractions = {x: waste_fractions[x] / fraction_anaerobic for x in compost_components}
        anaerobic_vol = {x: anaerobic_total * anaerobic_waste_fractions[x] for x in components_anaerobic}
    else:
        anaerobic_vol = {x: 0 for x in components_anaerobic}

    # combustion module
    combustion_total = 0
    components_combustion = set(['food', 'green', 'wood', 'paper_cardboard', 'textiles', 'plastic', 'rubber'])
    combustion_fraction_of_total = (np.nan_to_num(row[1]['waste_treatment_incineration_percent']) + 
                                    np.nan_to_num(row[1]['waste_treatment_advanced_thermal_treatment_percent']))/ 100
    if combustion_fraction_of_total != combustion_fraction_of_total:
        combustion_fraction_of_total = 0
    if combustion_fraction_of_total != 0:
        combustion_reject_rate = 0 #.1 I think sweet has an error, the rejected from combustion stuff just disappears
        combustion_total = combustion_fraction_of_total * waste_total * (1 - combustion_reject_rate)
        # if combustion_total != combustion_total:
        #     print('break')
        #     break
        #print(combustion_total)
        combustion_vol = {x: waste_fractions[x] * combustion_fraction_of_total * (1 - combustion_reject_rate) * waste_total for x in components_combustion}
        combustion_vol_total = sum([combustion_vol[x] for x in combustion_vol.keys()])
    else:
        combustion_vol = {x: 0 for x in components_combustion}

    # recycling
    recycling_fraction_of_total = np.nan_to_num(row[1]['waste_treatment_recycling_percent']) / 100
    components_recycling = set(['wood', 'paper_cardboard', 'textiles', 'plastic', 'rubber', 'metal', 'glass', 'other'])
    fraction_recyclable = sum([waste_fractions[x] for x in components_recycling])
    recycling_reject_rates = {'wood': .8, 'paper_cardboard': .775, 'textiles': .99, 
                             'plastic': .875, 'metal': .955, 'glass': .88, 'rubber': .78, 'other': .87}
    if recycling_fraction_of_total != 0:
        recycling_vol = {x: waste_fractions[x] / fraction_recyclable * recycling_fraction_of_total * (recycling_reject_rates[x]) * waste_total for x in components_recycling}
        recycling_vol_total = sum([recycling_vol[x] for x in recycling_vol.keys()])
    else:
        recycling_vol = {x: 0 for x in components_recycling}
    
    for c in components:
        if c not in compost_vol.keys():
            compost_vol[c] = 0
        if c not in anaerobic_vol.keys():
            anaerobic_vol[c] = 0
        if c not in combustion_vol.keys():
            combustion_vol[c] = 0
        if c not in recycling_vol.keys():
            recycling_vol[c] = 0

    q = {}
    ms = {}
    mass_compost = {}
    mass_anaerobic = {}
    q_df = {}
    ms_df = {}
    organic_df = {}

    for site in landfill_sites:
        mcf = mcfs[site]
        q[mcf] = {}
        ms[mcf] = {}
        q_df[mcf] = {}
        ms_df[mcf] = {}
        for waste in components:
            ms[mcf][waste] = []
            q[mcf][waste] = {}
            mass_compost[waste] = []
            mass_anaerobic[waste] = []
            organic_df[waste] = {}
            for t in range(50):
                #if (waste in compost_components) and (waste != 'paper_cardboard'):
                    # ms[mcf][waste].append((waste_total * (1.03 ** t) * waste_fractions[waste] - 
                    #                       compost_vol[waste] * diversion_fractions[site] * (1.03 ** t) - 
                    #                       anaerobic_vol[waste] * diversion_fractions[site] * (1.03 ** t) - 
                    #                       combustion_vol[waste] * diversion_fractions[site] * (1.03 ** t) - 
                    #                       recycling_vol[waste] * diversion_fractions[site] * (1.03 ** t)) * 
                    #                       diversion
                    #                       )
                ms[mcf][waste].append((waste_total * waste_fractions[waste] - 
                                        compost_vol[waste] - 
                                        anaerobic_vol[waste] - 
                                        combustion_vol[waste] - 
                                        recycling_vol[waste]) 
                                        * diversion_fractions[site] * (1.03 ** t))
                # Only have to do these once
                if site == 'landfill':
                    mass_compost[waste].append(compost_vol[waste] * (1.03 ** t))
                    mass_anaerobic[waste].append(anaerobic_vol[waste] * (1.03 ** t))
                # else:
                #     ms[mcf][waste].append(site_waste * (1.03 ** t) * waste_fractions[waste] - 
                #                           combustion_vol[waste] * diversion_fractions[site] * (1.03 ** t) - 
                #                           recycling_vol[waste] * diversion_fractions[site] * (1.03 ** t))
                ch4 = []
                for y in range(t):
                    val = ks[waste] * L_0[waste] * ms[mcf][waste][y] * np.exp(-ks[waste] * (t - y - 0.5)) * mcf * (1 - oxidation_factor['without_lfg'][site])
                    ch4.append(val)
                #Q3[waste][t] = convert_methane_m3_to_ton(sum(ch4)) * 28
                # if sum(ch4) == 0.0:
                #     break
                q[mcf][waste][t] = sum(ch4)
                if site == 'landfill':
                    organic_df[waste][t] = mass_compost[waste][t] * mef_compost + mass_anaerobic[waste][t] * mef_anaerobic
                #Ms2[waste] = [x * np.exp(-k[waste]) for x in Ms2[waste]]
                
        
        q_df[mcf] = pd.DataFrame(q[mcf])
        q_df[mcf]['total'] = q_df[mcf].sum(axis=1)
        ms_df[mcf] = pd.DataFrame(ms[mcf])

    runs_q[city] = q_df
    runs_m[city] = ms_df
    organics_q[city] = pd.DataFrame(organic_df)

    if country == 'Argentina':
        break
    
# REMEMBER TO ADD THE UNSPECIFIED LANDFILL COLUMN

#%%
def convert_methane_m3_to_ton_co2e(volume_m3):
    density_kg_per_m3 = 0.7168
    mass_kg = volume_m3 * density_kg_per_m3
    mass_ton = mass_kg / 1000
    mass_co2e = mass_ton * 28
    return mass_co2e

runs_q_tons = {}
for city in runs_q.keys():
    run = runs_q[city]
    runs_q_tons[city] = {}
    for mcf in run.keys():
        site = run[mcf]
        runs_q_tons[city][mcf] = convert_methane_m3_to_ton_co2e(site)
        
        
#units_df = convert_methane_m3_to_ton(q_df[1]) * 28
