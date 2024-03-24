import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages

def compare_countries_defsurplus_gdp():
    defsur = pd.read_csv('PROJECT/data/gov_deficit_surplus.csv')
    gdp = pd.read_csv('PROJECT/data/gdp.csv')

    exclude_values = ['EA19', 'EA20', 'EU27_2020']
    defsur = defsur[~defsur['geo'].isin(exclude_values)]    

    # only want gdp values with unit of measure millions of euros
    'UNIT' == 'CP_MEUR'
    gdp = gdp[gdp['unit'] == 'CP_MEUR']

    abbreviation_to_country = {
    'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CY': 'Cyprus', 'CZ': 'Czech Republic',
    'DE': 'Germany', 'DK': 'Denmark', 'EE': 'Estonia', 'EL': 'Greece', 'ES': 'Spain',
    'FI': 'Finland', 'FR': 'France', 'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland',
    'IT': 'Italy', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'MT': 'Malta',
    'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania', 'SE': 'Sweden',
    'SI': 'Slovenia', 'SK': 'Slovakia'}

    # merge the two datasets based on year and country
    merged_df = pd.merge(defsur, gdp, on=['TIME_PERIOD', 'geo'])

    # only keep the relevant columns
    merged_df = merged_df[['OBS_VALUE_x', 'OBS_VALUE_y', 'TIME_PERIOD', 'geo']]
    print(merged_df.head())

    # give them better names
    merged_df.columns = ['Deficit/Surplus', 'GDP_per_capita', 'Year', 'Country']

    # calculate deficit/surplus as a percentage of gdp
    merged_df['Deficit/Surplus_%_GDP'] = (merged_df['Deficit/Surplus'] / merged_df['GDP_per_capita']) * 100

    # change country name abbreviations to full names
    merged_df['Country'] = merged_df['Country'].map(abbreviation_to_country)

    # calculate average over all the years for each country
    average_deficit_surplus_gdp = merged_df.groupby('Country')['Deficit/Surplus_%_GDP'].mean().reset_index()

    # sort in ascending order
    average_deficit_surplus_gdp_sorted = average_deficit_surplus_gdp.sort_values(by='Deficit/Surplus_%_GDP')

    colors = ['red' if x < 0 else 'green' for x in average_deficit_surplus_gdp_sorted['Deficit/Surplus_%_GDP']]

    with PdfPages('./PROJECT/figures/comparison_countries_gdp.pdf') as pdf:
        plt.figure(figsize=(12,8))
        plt.barh(average_deficit_surplus_gdp_sorted['Country'], average_deficit_surplus_gdp_sorted['Deficit/Surplus_%_GDP'], color=colors)
        plt.xlabel('Average Deficit/Surplus as % of GDP')
        plt.ylabel('Country')
        plt.title('Average Deficit/Surplus as % of GDP by Country (Ascending Order)')
        plt.grid(axis='x')
        pdf.savefig(bbox_inches='tight')
        plt.close()


compare_countries_defsurplus_gdp()