import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.backends.backend_pdf import PdfPages

## Deficit/Surplus=Government Revenue − Government Expenditure

def calculate_regression_parameters(data):
    slope, intercept, r_value, p_value, std_err = linregress(data['TIME_PERIOD'], data['OBS_VALUE'])
    r_squared = r_value**2
    return slope, intercept, r_value, p_value, r_squared

def analyze_long_term_trends():
    df = pd.read_csv('PROJECT/data/gov_deficit_surplus.csv')

    exclude_values = ['EA19', 'EA20', 'EU27_2020']

    df = df[~df['geo'].isin(exclude_values)]

    abbreviation_to_country = {
    'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CY': 'Cyprus', 'CZ': 'Czech Republic',
    'DE': 'Germany', 'DK': 'Denmark', 'EE': 'Estonia', 'EL': 'Greece', 'ES': 'Spain',
    'FI': 'Finland', 'FR': 'France', 'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland',
    'IT': 'Italy', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'MT': 'Malta',
    'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania', 'SE': 'Sweden',
    'SI': 'Slovenia', 'SK': 'Slovakia'}

    with PdfPages('./PROJECT/figures/long_term_trends.pdf') as pdf:
        plt.figure(figsize=(10,8))
        country_stats = {}
        # Visualize long-term trends for each country
        for country, data in df.groupby('geo'):
            country_name = abbreviation_to_country[country]
            mean_deficit_surplus = data['OBS_VALUE'].mean()
            std_deficit_surplus = data['OBS_VALUE'].std()
            country_stats[country] = {
                'Mean Deficit/Surplus': mean_deficit_surplus,
                'Standard Deviation': std_deficit_surplus
            }
            plt.plot(data['TIME_PERIOD'], data['OBS_VALUE'], label=country_name)

        # Overall dataset lineplot 
        plt.xlabel('Year')
        plt.ylabel('Deficit/Surplus')
        plt.title('Long-term Trends in Government Deficit/Surplus')
        plt.legend(loc='center left', bbox_to_anchor=(1,0.5))
        pdf.savefig(bbox_inches='tight')
        plt.close()

        # Rank the countries based on standard deviation and make a plot
        country_variability = df.groupby('geo')['OBS_VALUE'].std().sort_values(ascending=False)
        # Replace country abbreviations with names
        country_variability.index = [abbreviation_to_country.get(country, country) for country in country_variability.index]

        colors = plt.cm.RdYlGn(np.linspace(0, 1, len(country_variability)))

        plt.figure(figsize=(10, 6))
        plt.bar(country_variability.index, country_variability.values, color=colors)
        plt.xlabel('Country')
        plt.ylabel('Standard Deviation of Deficit/Surplus')
        plt.title('Standard Deviation of Deficit/Surplus Data Across Countries')
        plt.xticks(rotation=45, ha='right')
        pdf.savefig(bbox_inches='tight')
        plt.close()

        # Rank the countries based on mean and make a plot
        country_mean_deficit_surplus = df.groupby('geo')['OBS_VALUE'].mean().sort_values()
        # Replace country abbreviations with names
        country_mean_deficit_surplus.index = [abbreviation_to_country.get(country, country) for country in country_mean_deficit_surplus.index]

        colors = plt.cm.RdYlGn(np.linspace(0, 1, len(country_mean_deficit_surplus)))

        # Plotting the ranking
        plt.figure(figsize=(10, 6))
        plt.bar(country_mean_deficit_surplus.index, country_mean_deficit_surplus.values, color=colors)
        plt.xlabel('Country')
        plt.ylabel('Mean Deficit/Surplus')
        plt.title('Mean Deficit/Surplus Across Countries')
        plt.xticks(rotation=45, ha='right')
        pdf.savefig(bbox_inches='tight')
        plt.close()



        # Combine mean and standard deviation to create a ranking of the countries
        data = pd.DataFrame({
            'Country': country_mean_deficit_surplus.index,
            'MeanDeficitSurplus': country_mean_deficit_surplus.values,
            'StdDev': country_variability.reindex(country_mean_deficit_surplus.index).values
        })

        # Normalize the mean and standard deviation values to be between 0 and 1
        data['NormalizedMean'] = (data['MeanDeficitSurplus'] - min(data['MeanDeficitSurplus'])) / (max(data['MeanDeficitSurplus']) - min(data['MeanDeficitSurplus']))
        data['NormalizedStdDev'] = (data['StdDev'] - min(data['StdDev'])) / (max(data['StdDev']) - min(data['StdDev']))

        # Want lower values to be better (for both stddev and mean) 
        # Best is to have high mean and low standard deviation
        data['Score'] = (1 - data['NormalizedMean']) + data['NormalizedStdDev']

        data['Rank'] = data['Score'].rank(ascending=False)
        ranked_data = data.sort_values('Rank', ascending=True)

        # plot the results
        plt.figure(figsize=(12, 10))
        plt.barh(ranked_data['Country'], ranked_data['Score'], color='steelblue')
        plt.xlabel('Combined Score (Lower is Better)')
        plt.title('Ranking of Countries by Combined Score of Mean Deficit/Surplus and Standard Deviation')
        pdf.savefig(bbox_inches='tight')
        plt.close()


        # Use linear regression to find which countries deficit/surplus is increasing/decreasing
        country_trends = {}
        r_squared_values = {}
        for country, country_data in df.groupby('geo'):
            slope, _, _, _, r_squared = calculate_regression_parameters(country_data)
            country_trends[abbreviation_to_country[country]] = slope
            r_squared_values[abbreviation_to_country[country]] = r_squared

        # Find which countries have increasing/ decreasing slope values
        increasing = {}
        decreasing = {}
        for country, slope in country_trends.items():
            if slope > 0:
                increasing[country] = slope
            else:
                decreasing[country] = slope
        
        # Sort based on slope
        sorted_increasing = sorted(increasing.items(), key=lambda x: x[1])
        sorted_decreasing = sorted(decreasing.items(), key=lambda x: x[1])

        # Plot increasing slopes
        plt.figure(figsize=(10, 6))

        for i, (country, slope) in enumerate(sorted_increasing):
            plt.barh(i, slope, color='green')
            plt.text(slope, i, f"R²={r_squared_values[country]:.2f}", va='center')
    
        plt.yticks(range(len(sorted_increasing)), [country for country, _ in sorted_increasing])
        plt.xlabel('Slope')
        plt.ylabel('Country')
        plt.title('Countries with Increasing Deficit/Surplus Over Time')
        plt.grid(axis='x')
        pdf.savefig(bbox_inches='tight')
        plt.close()

        # Plot decreasing slopes
        plt.figure(figsize=(10, 6))
        
        for i, (country, slope) in enumerate(sorted_decreasing):
            plt.barh(i, -slope, color='red')
            plt.text(-slope, i, f"R²={r_squared_values[country]:.2f}", va='center')
    
        
        #plt.barh(range(len(sorted_decreasing)), [-slope for _, slope in sorted_decreasing], align='center', color='red')
        plt.yticks(range(len(sorted_decreasing)), [country for country, _ in sorted_decreasing])
        plt.xlabel('-Slope')
        plt.ylabel('Country')
        plt.title('Countries with Decreasing Deficit/Surplus Over Time')
        plt.grid(axis='x')
        pdf.savefig(bbox_inches='tight')
        plt.close()

        


analyze_long_term_trends()