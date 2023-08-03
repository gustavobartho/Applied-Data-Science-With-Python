import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

month_number_to_string = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

us_state_to_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC", "American Samoa": "AS", "Guam": "GU", "Northern Mariana Islands": "MP", "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM", "U.S. Virgin Islands": "VI",
}

homelessness_df = pd.read_csv('datasets/Homelessness-USA.csv')
homelessness_df['Count'] = pd.to_numeric(homelessness_df['Count'].replace(',', '', regex=True))
homelessness_df['Year'] = pd.to_numeric(homelessness_df['Year'].replace('^\d+\/\d+\/', '', regex=True))
homelessness_df.rename(columns={'Count': 'Homelessness Count'}, inplace=True)
homelessness_df = homelessness_df[homelessness_df['Measures'] == 'Total Homeless']
homelessness_df = homelessness_df[['Year', 'State', 'CoC Number', 'Homelessness Count']]

unemployment_df = pd.read_csv('datasets/Unemployment-USA.csv')
unemployment_df['State'] = unemployment_df['State'].apply(lambda x: us_state_to_abbrev[x] if x in us_state_to_abbrev.keys() else x)
unemployment_df['Year'] = pd.to_numeric(unemployment_df['Year'])
unemployment_df.rename(columns={'Rate': 'Unemployment Rate'}, inplace=True)

homelessness_per_year = homelessness_df.groupby('Year').agg({'Homelessness Count': np.sum}).reset_index()

unemployment_per_year = unemployment_df.groupby('Year').agg({'Unemployment Rate': np.mean}).reset_index()

joint_df = pd.merge(homelessness_per_year, unemployment_per_year, left_on='Year', right_on='Year', how='inner')
joint_df = joint_df[joint_df['Year'] > 2008]

fig, ax = plt.subplots()

x = [str(i) for i in joint_df['Year']]
y0 = list(joint_df['Homelessness Count'])
y1 = list(joint_df['Unemployment Rate'])

ax.plot(x, y0, color="blue") 
ax.set_ylabel('Homelessness Count', color="blue")
ax.tick_params(axis='y', colors="blue") 
ax1 = ax.twinx()
ax1.plot(x, y1, color="red")    
ax1.set_ylabel('Unemployment Rate', color="red")     
ax1.tick_params(axis='y', colors="red")   

ax.spines[['top', 'left', 'right']].set_visible(False)
ax1.spines[['top', 'left', 'right']].set_visible(False)

plt.title('Relationship between Homelessness and \nUnemployment in U.S.A', fontsize=15, pad=50)
plt.show()

fig.savefig('assignment4.png', bbox_inches = 'tight')