import pandas as pd
import os

# load data from computer
feature_race_data = pd.read_csv("~/Documents/Datasets/Formula 2 championship/Feature-Race.csv")
sprint_race_data = pd.read_csv("~/Documents/Datasets/Formula 2 championship/Sprint-Race.csv")
sprint_race_2_data = pd.read_csv("~/Documents/Datasets/Formula 2 championship/Sprint-Race-2.csv")

# dates were out of order
# sort feature & sprint races by date in chronological order from 2017
sorted_feature_races = feature_race_data.sort_values(by=['DATE', 'POS'])
sorted_sprint_races = sprint_race_data.sort_values(by=['DATE', 'POS'])

# merge all races to create one big dataframe for 2017-2023 seasons
sprint_races = pd.concat([sorted_sprint_races, sprint_race_2_data], join='outer')
sprint_races.sort_values(by=['DATE', 'TYPE', 'POS'], inplace=True)
all_races = pd.concat([sorted_feature_races, sprint_races], join='outer').sort_values(by=['DATE', 'TYPE', 'POS'])

# fix the value for gap to first for all the race winners
all_races['GAP'].replace(to_replace='-', value='0.000', inplace=True)

# apply proper index to combined dataframe
all_races.reset_index(drop=True, inplace=True)

# correct erroneous values
all_races.iloc[356, 2] = '0.000'
all_races.iloc[2298, 2] = '0.000'
all_races.iloc[2298, 3] = '0.000'

# check which values have the '-' symbol in the 'INT.' column for the whole dataframe and for race winners
dash_in_int_col = all_races[all_races['INT.'] == '-']
dash_in_int_col_for_winners = all_races[(all_races['INT.'] == '-') & (all_races['POS'] == 1.00000)]

# correct erroneous entries for gap for race winners (from - to 0.000)
all_races.loc[(all_races['INT.'] == '-') & (all_races['POS'] == 1.00000), 'INT.'] = '0.000'

# collect drivers whose 'INT.' value is '-' instead of the actual value
dash = all_races[(all_races['INT.'] == '-') & (all_races['POS'] == 2.00000)]

# correct 'INT.' value for all second-placed drivers to the value of 'GAP'
for x in all_races.index.tolist():
    if all_races.loc[x, 'POS'] == 2.00000:
        all_races.loc[x, 'INT.'] = all_races.loc[x, 'GAP']

# convert to csv for use in Tableau
os.makedirs('folder/subfolder', exist_ok=True)
all_races.to_csv('folder/subfolder/all_races.csv')
