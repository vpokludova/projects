import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

def extract_features(series):
    # used in clustering method 1
    return [np.mean(series), np.std(series), np.min(series), np.max(series)]

# Use elbow method and silhouette method approaches to create graphs 
# from which to find optimal number of clusters
def find_optimal_clusters(X, max_clusters=10):
    wcss = []  
    silhouette_scores = []

    for i in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
        kmeans.fit(X)

        wcss.append(kmeans.inertia_)

        silhouette_scores.append(silhouette_score(X, kmeans.labels_))

    # plot results
    # elbow method
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(range(2, max_clusters + 1), wcss, marker='o')
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')

    # silhouette method
    plt.subplot(1, 2, 2)
    plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o')
    plt.title('Silhouette Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette Score')

    plt.tight_layout()
    plt.show()
    return
    
# Print to output which countries are in each cluster
def print_result(time_series_data, num_clusters):
    abbreviation_to_country = {
    'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CY': 'Cyprus', 'CZ': 'Czech Republic',
    'DE': 'Germany', 'DK': 'Denmark', 'EE': 'Estonia', 'EL': 'Greece', 'ES': 'Spain',
    'FI': 'Finland', 'FR': 'France', 'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland',
    'IT': 'Italy', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'MT': 'Malta',
    'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania', 'SE': 'Sweden',
    'SI': 'Slovenia', 'SK': 'Slovakia'}

    for cluster in range(num_clusters):
        print(f"\nCountries in Cluster {cluster}:")
        countries_in_cluster = time_series_data[time_series_data['Cluster'] == cluster]['geo'].values
        for country_code in countries_in_cluster:
            print(abbreviation_to_country.get(country_code, 'Unknown Country Code'))
 

# Use PCA to reduce dimensionality of data and then plot the data to visualize clusters
def plot_clusters(transformed_data):
    X = transformed_data.drop(columns=['Cluster'])

    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)

    # do pca
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(X_std)

    # Create dataframe with the principal components and cluster labels
    pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    pca_df['Cluster'] = transformed_data['Cluster']
    
    fig, ax = plt.subplots()
    
    # Color map for clusters
    colors = {0: 'r', 1: 'g', 2: 'b', 3: 'c', 4: 'm', 5: 'y', 6: 'k'}
    
    # Group by cluster and plot each cluster with its own color
    for cluster, group in pca_df.groupby('Cluster'):
        group.plot(ax=ax, kind='scatter', x='PC1', y='PC2', label=f'Cluster {cluster}', color=colors[cluster])
    
    plt.title('Cluster Visualization')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend()
    plt.show()

    return

# This method finds the mean, std, min, and max for each series of values 
# (e.g. series of UNEMPL_RATE values for a specific country)
# and then use these values to cluster the countries
def clustering_method1(time_series_data):
    full_data = time_series_data
    clustering_data = full_data[['DEF_SUR', 'GDP', 'INFL_RATE', 'UNEMPLOY_RATE']]

    features = ['DEF_SUR', 'GDP', 'INFL_RATE', 'UNEMPLOY_RATE']
    for feature in features:
        clustering_data[[f"{feature}_mean", f"{feature}_std", f"{feature}_min", f"{feature}_max"]] = \
            clustering_data[feature].apply(lambda x: extract_features(x)).apply(pd.Series)

    X = clustering_data[[f"{feature}_{stat}" for feature in features for stat in ['mean', 'std', 'min', 'max']]]

    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)

    # find optimal number of clusters
    #find_optimal_clusters(X_std)

    num_clusters = 4    # this was concluded from the graphs produced from the above commented out code
    kmeans = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    prediction = kmeans.fit_predict(X_std)
    X['Cluster'] = prediction
    full_data['Cluster'] = prediction

    print("Clusters from method 1:")
    plot_clusters(X)
    print_result(full_data, num_clusters)

# This method creates a column for each feature_year value so the list of feature values gets
# expanded to as many columns as there are years in the data
# ex. [GDP_2012, GDP_2013, ..., GDP_2022] -> each value gets its own column
# Then these columns are used to cluster
def clustering_method2(time_series_data):
    clustering_data = time_series_data

    features = ['DEF_SUR', 'GDP', 'INFL_RATE', 'UNEMPLOY_RATE']
    years = clustering_data['TIME_PERIOD'].iloc[0]

    for feature in features:
        temp_df = clustering_data[['geo', feature]].explode(feature)
        temp_df['Year'] = temp_df.groupby('geo').cumcount()
        temp_df['Year'] = temp_df['Year'].apply(lambda x: years[x])  # Assign the correct year based on the index
        temp_df_pivot = temp_df.pivot(index='geo', columns='Year', values=feature)
        temp_df_pivot.columns = [f"{feature}_{year}" for year in temp_df_pivot.columns]
        clustering_data = clustering_data.join(temp_df_pivot, on='geo')

    clustering_data = clustering_data.drop(columns=features)

    clustering_features = [col for col in clustering_data.columns if any(feature in col for feature in features)]
    X = clustering_data[clustering_features]

    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)

    # find optimal number of clusters
    #find_optimal_clusters(X_std)

    num_clusters = 3
    kmeans = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    prediction = kmeans.fit_predict(X_std)
    X['Cluster'] = prediction
    clustering_data['Cluster'] = prediction

    print("Clusters from method 2: ")
    plot_clusters(X)
    print_result(clustering_data, num_clusters)


def clustering():
    # LOAD AND PREPROCESS DATA
    defsur = pd.read_csv('PROJECT/data/gov_deficit_surplus.csv')
    exclude_values = ['EA19', 'EA20', 'EU27_2020']
    defsur = defsur[~defsur['geo'].isin(exclude_values)]    
    defsur = defsur[['geo', 'TIME_PERIOD', 'OBS_VALUE']]
    defsur = defsur.rename(columns={'OBS_VALUE': 'DEF_SUR'})

    gdp = pd.read_csv('PROJECT/data/gdp.csv')
    gdp = gdp[gdp['unit'] == 'CP_MEUR']
    gdp = gdp[['geo', 'TIME_PERIOD', 'OBS_VALUE']]
    gdp = gdp.rename(columns={'OBS_VALUE': 'GDP'})
    
    inflrate = pd.read_csv('PROJECT/data/hicp_infl_rate.csv')
    inflrate = inflrate[['geo', 'TIME_PERIOD', 'OBS_VALUE']]
    inflrate = inflrate.rename(columns={'OBS_VALUE': 'INFL_RATE'})

    unemploy_rate = pd.read_csv('PROJECT/data/unemployment_rate.csv')
    unemploy_rate = unemploy_rate[unemploy_rate['unit'] == 'PC_ACT']
    unemploy_rate = unemploy_rate[['geo', 'TIME_PERIOD', 'OBS_VALUE']]
    unemploy_rate = unemploy_rate.rename(columns={'OBS_VALUE': 'UNEMPLOY_RATE'})

    # merge all datasets into one
    merged_df = pd.merge(defsur, gdp, on=['geo', 'TIME_PERIOD'], how='outer')
    merged_df = pd.merge(merged_df, inflrate, on=['geo', 'TIME_PERIOD'], how='outer')
    merged_df = pd.merge(merged_df, unemploy_rate, on=['geo', 'TIME_PERIOD'], how='outer')

    # drop countries that have incomplete data
    merged_df = merged_df.dropna()

    # CLUSTERING

    # group by country and aggregate all values into lists
    time_series_data_with_year = merged_df.groupby('geo').agg(lambda x: x.tolist()).reset_index()

    time_series_data = time_series_data_with_year[['geo', 'DEF_SUR', 'GDP', 'INFL_RATE', 'UNEMPLOY_RATE']]

    clustering_method1(time_series_data)
    clustering_method2(time_series_data_with_year)
    

clustering()