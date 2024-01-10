import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import matplotlib.patches as mpatches
import seaborn as sns

"""
https://github.com/tayyabjamil/Infographics-DV-22092067
github Repo
"""

"""
Graph 1 to show geographical districution of top unicorn 
companies in different cities around the world
"""
def show_selected_cities_map(ax,top_companies):

    world_cities_data_with_lat_lng = pd.read_csv("worldcities.csv")
    top_companies_country_city = top_companies[['City', 'Country']]

    # Create a GeoDataFrame for cities
    merged_dataframe = pd.merge(top_companies_country_city, world_cities_data_with_lat_lng, left_on=['City', 'Country'], right_on=['city', 'country'], how='left')

    # Drop duplicate columns (if any) and keep only one set of 'City' and 'Country'
    merged_dataframe = merged_dataframe[['City', 'Country', 'lat', 'lng']]
    result_dataframe = pd.merge(top_companies, merged_dataframe, on=['City', 'Country'], how='left')

    # Remove duplicates based on 'City' and 'Country' columns
    result_dataframe = result_dataframe.drop_duplicates(subset=['City', 'Country'])
    result_dataframe = result_dataframe.dropna(subset=['lat', 'lng'])

    # Set a single color for all circles
    circle_color = 'salmon'  # Adjust the color as needed

    # Load the world map GeoDataFrame from Natural Earth dataset
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Create a plot with a PlateCarree projection
   
    # Add countries to the plot with a stylish color palette
    world.boundary.plot(ax=ax, linewidth=0.8, color='darkslategray', edgecolor='white')

    # Plot cities on the map with stylish marker styles
    ax.scatter(result_dataframe['lng'], result_dataframe['lat'], s=250, c=circle_color, marker='o', label='Top Unicorn Companies', edgecolors='black', linewidths=1, )
    
    ax.set_title('Geographical City distribution of Unicorn countries ', fontsize=30, fontweight='bold', color="red")
  
    # Create a legend with country and count of companies
    country_counts = result_dataframe['Country'].value_counts()
    handles = [mpatches.Patch(color=circle_color, label=f'{country} ({count} companies)') for country, count in country_counts.items()]

    # Add legend outside the plot with increased font size
    legend = ax.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, -0.7),fontsize=22, borderaxespad=0.1,  ncol=3)
    
   
    # Show the plot with a stylish background color
    ax.set_facecolor('whitesmoke')
 


"""
Pie Chart to show the percentage of top 
unicorn companies in different countries
"""
def show_country_pie_chart(ax, unicorn_companies_data):
    sorted_countries = unicorn_companies_data.head(100)

    dataframe = pd.DataFrame(sorted_countries, columns=['Country'])
   
    # Count the occurrences of each country
    country_counts = dataframe['Country'].value_counts()

    # Calculate threshold (5%)
    threshold = 0.01 * country_counts.sum()

    # Identify slices greater than 5%
    large_slices = country_counts[country_counts > threshold]
    small_slices = country_counts[country_counts <= threshold]

    # Create a fancy pie chart with legend on bottom right and increased size
    explode_large = [0.1 if country in large_slices.index else 0 for country in country_counts.index]
   
    wedgeprops = {'linewidth': 3, 'edgecolor': 'grey'}  # Add a shadow effect

    # Set font sizes
    #ax.set_title('Percentage of Top 50 Unicorn Companies in different Countries', fontsize=30, fontweight='bold', color="red")
    
    # Display the percentage only for slices larger than 2%
    def custom_autopct(pct):
        return f'{pct:0.1f}%' if pct > 2 else ''

    # Display the percentage labels for all slices
    ax.pie(country_counts, autopct=custom_autopct,
        startangle=140, colors=plt.cm.Set3.colors, explode=explode_large,
        wedgeprops=wedgeprops, textprops={'fontsize': 30}, labeldistance=1.1)
   
    # Add a legend outside the pie chart
    legend_labels = [f'{country}: {percentage:.1f}%' for country, percentage in zip(country_counts.index, (country_counts / country_counts.sum()) * 100)]
    legend = ax.legend(legend_labels, title='Legend', loc='center left', bbox_to_anchor=(-0.4, 0.5), fontsize=30)

    ax.set_xlabel('Country-Wise-Percentage', fontsize=30,fontweight='bold',color="red")
  
"""
Vertical Bar Graph to show the percentage of top 
unicorn companies in different industries
"""

def show_categories_vertical_bar_chart(ax, unicorn_companies_data):
    # Create a DataFrame with the 'Industry' column
    dataframe = pd.DataFrame(unicorn_companies_data, columns=['Industry'])

    # Count the occurrences of each category
    category_counts = dataframe['Industry'].value_counts()

    # Calculate percentage for each category
    total_categories = len(dataframe['Industry'])
    percentages = (category_counts / total_categories) * 100

    # Set Seaborn style
    sns.set(style="whitegrid")

    # Create a vertical bar graph using Seaborn
    sns.barplot(x=percentages.index, y=percentages.values, palette="viridis", ax=ax)

    # Display percentage values on top of each bar
    for i, v in enumerate(percentages.values):
        ax.text(i, v + 0.5, f'{v:.2f}%', ha='center', fontsize=24)

    # Set titles and labels
    ax.set_title('Industry Distribution of Top Unicorn Companies Worldwide', fontsize=30, fontweight='bold', color="red")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=24)  # Rotate x-axis labels for better readability
    ax.set_xlabel('Industries', fontsize=30,fontweight='bold',color="red")
    ax.set_ylabel('Percentage', fontsize=30,color="red")

"""
Line Chart  to show the valutions of top 
unicorn companies 
"""


def line_chart(ax, unicorn_companies_data):
    unicorn_companies_data_subset = unicorn_companies_data.head(30)
    unicorn_companies_data_subset['Valuation ($B)'] = unicorn_companies_data_subset['Valuation ($B)'].replace('[\$,]', '', regex=True).astype(float)

    companies = unicorn_companies_data_subset['Company']
    valuations = unicorn_companies_data_subset['Valuation ($B)']

    # Sort data based on valuations
    sorted_indices = valuations.argsort()
    companies = companies.iloc[sorted_indices]
    valuations = valuations.iloc[sorted_indices]

    # Create a line graph

    # Plot with a line and markers, set color and linewidth
    ax.plot( valuations,companies, marker='o', linestyle='-', color='b', linewidth=2, markersize=8, label='Valuation')

    # Set chart title and labels
    ax.set_title('Top 30 Company Valuations in Billions', color='red', fontsize=30)
    ax.set_ylabel('Companies',  fontsize=30,fontweight='bold',color="red")
    ax.set_xlabel('Valuation (in billions)', color='red', fontsize=30)

    # Rotate x-axis labels for better readability

    # Customize grid lines
    ax.axhline(0, color='black', linewidth=0.5)

    # Add a background color to the plot area
    ax.set_facecolor('#F4F4F4')

    # Customize tick parameters
    ax.tick_params(axis='both', which='both', colors='black', labelsize=22)

    # Add a horizontal line at y=0 for better visibility
    ax.axhline(0, color='black', linewidth=0.5)

   
    

# Read data
unicorn_companies_data = pd.read_csv("World_Wide-Unicorn-Company-List.csv")

# Create a 2x2 subplot grid with a larger figsize
fig, axs = plt.subplots(2, 2, figsize=(40, 30))

# Plotting the geographical distribution map in the first grid
show_categories_vertical_bar_chart(axs[0, 0], unicorn_companies_data)

axs[0, 0].set_title('Bar chart showing top unicorn companies percentage in various industries with FinTech and Internet Servcies having almost 40% ratio', fontsize=24, fontweight='bold', color='blue')

# Plotting the geographical distribution map
show_selected_cities_map(axs[0, 1], unicorn_companies_data)
axs[0, 1].set_title('Map graph showing geographical city distribution of top unicorn companies with United States having 126 Companies', fontsize=24, fontweight='bold', color='blue')

# Plotting the line chart - Company Valuations
line_chart(axs[1, 0], unicorn_companies_data)
axs[1, 0].set_title('Line Graph showing Top unicorn companies valutions with Byte Dance having hightes 140 Billion $ value', fontsize=24, fontweight='bold', color='blue')

# Plotting the pie chart - Country-wise Distribution
show_country_pie_chart(axs[1, 1], unicorn_companies_data)
axs[1, 1].set_title('Pie Graph showing Country-wise Distribution with United States having 60% of Top unicorn companies', fontsize=24, fontweight='bold', color='blue')

fig.text(0.75, 0.98, 'Name: Muhammad Tayyab, Reg: 22092067', fontsize=50, ha='center', va='center', color='white', fontweight='bold', bbox=dict(facecolor='red', edgecolor='none', ))
fig.text(0.75, 0.95, 'Infographics of Top Unicorn Companies Analysis', fontsize=50, ha='center', va='center', color='white', fontweight='bold', bbox=dict(facecolor='red', edgecolor='none', ))

# Plotting a pie chart in the fourth grid (dummy data used)
show_country_pie_chart(axs[1, 1], unicorn_companies_data)

# Adjust layout for better appearance
plt.tight_layout()

# Save the figure
plt.savefig('22092067.png',dpi=300)

