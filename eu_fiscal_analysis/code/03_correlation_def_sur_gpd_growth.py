import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from matplotlib.backends.backend_pdf import PdfPages

def analyze_correlation_def_sur_gdp_growth():
    abbreviation_to_country = {
    'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CY': 'Cyprus', 'CZ': 'Czech Republic',
    'DE': 'Germany', 'DK': 'Denmark', 'EE': 'Estonia', 'EL': 'Greece', 'ES': 'Spain',
    'FI': 'Finland', 'FR': 'France', 'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland',
    'IT': 'Italy', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'MT': 'Malta',
    'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania', 'SE': 'Sweden',
    'SI': 'Slovenia', 'SK': 'Slovakia'}

    # load, clean, and merge datasets
    defsur = pd.read_csv('PROJECT/data/gov_deficit_surplus.csv')
    gdp_growth = pd.read_csv('PROJECT/data/gdp_growth_rate.csv')

    exclude_values = ['EA19', 'EA20', 'EU27_2020']
    defsur = defsur[~defsur['geo'].isin(exclude_values)]

    # only want gdp growth rates as pure percentage change on previous period
    'UNIT' == 'CLV_PCH_PRE'
    gdp_growth = gdp_growth[gdp_growth['unit'] == 'CLV_PCH_PRE']

    # merge the two datasets based on year and country
    merged_df = pd.merge(defsur, gdp_growth, on=['TIME_PERIOD', 'geo'])

    # only keep the relevant columns
    merged_df = merged_df[['OBS_VALUE_x', 'OBS_VALUE_y', 'TIME_PERIOD', 'geo']]
    
    # give them better names
    merged_df.columns = ['Deficit/Surplus', 'GDP_growth_rate', 'Year', 'Country']

    # change country name abbreviations to full names
    merged_df['Country'] = merged_df['Country'].map(abbreviation_to_country)

    # compute correlation for each country
    correlation_data = {}
    for country, group in merged_df.groupby('Country'):
        correlation = group['Deficit/Surplus'].corr(group['GDP_growth_rate'])
        correlation_data[country] = correlation
    
    overall_correlation = merged_df['Deficit/Surplus'].corr(merged_df['GDP_growth_rate'])
    print(f"Overall Correlation: {overall_correlation}")

    correlation_df = pd.DataFrame(list(correlation_data.items()), columns=['Country', 'Correlation'])
    correlation_df = correlation_df.sort_values(by='Correlation')

    norm = colors.Normalize(-1, 1)
    colormap = cm.ScalarMappable(norm=norm, cmap=cm.bwr)

    with PdfPages('./PROJECT/figures/correlation_def_sur_gdp_growth.pdf') as pdf:
        # make a general plot for gdp growth rate for each country
        plt.figure(figsize=(10, 6))
        for country, data in merged_df.groupby('Country'):
            plt.plot(data['Year'], data['GDP_growth_rate'], label=country) 

        plt.xlabel('Year')
        plt.ylabel('GDP Growth Rate (%)')
        plt.title('GDP Growth Rate Over Time for Each EU Country')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xticks(rotation=45)  # rotate x-axis labels for better readability
        pdf.savefig(bbox_inches='tight')  
        plt.close() 

        plt.figure(figsize=(10,6))
        bars = plt.bar(correlation_df['Country'], correlation_df['Correlation'], color=[colormap.to_rgba(x) for x in correlation_df['Correlation']], edgecolor='black', linewidth=0.5)
        plt.bar_label(bars, labels=[f"{corr:.2f}" for corr in correlation_df['Correlation']], label_type='edge', fontsize=8)
        plt.xlabel('Country')
        plt.ylabel('Correlation Coefficient')
        plt.title('Correlation between Deficit/Surplus and GDP Growth Rate by Country')
        plt.xticks(rotation=45, ha="right")
        plt.axhline(0, color='black', linewidth=0.8)  # add a line at y=0 for reference
        pdf.savefig(bbox_inches='tight')  
        plt.close() 
        


analyze_correlation_def_sur_gdp_growth()